# coding: utf-8

import copy
import importlib
import inspect
import logging
import os
import json
import selenium
import re
import time
import hashlib
import traceback
import urlparse
from datetime import datetime, timedelta
import pymysql
import requests
import tldextract
import default_config
from pyquery import PyQuery as pq
from default_config import SERVER_FLAG
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from util import downloader
from util.parser import build_parser
from util.exceptions import SeleniumException, TaskFinishSignal
from util.exceptions import SeleniumException
from util.mailbox import send_alert_email_to

try:
    import cchardet as chardet
except ImportError:
    import chardet

BASE_DIR = os.path.dirname(os.path.realpath(__name__))

PROJ_REGX_PAT = re.compile(r'(config.[^.]+.)')



logger = logging.getLogger(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}

class Browser(object):

    def __init__(self):
        # TODO: author:xNathan, date: 2017/09/28 15:35,自定义浏览器driver
        # TODO: author:xNathan, date: 2017/09/28 15:35,新增IE webdriver

        # For Firefox
        _desired_cap = webdriver.DesiredCapabilities.FIREFOX
        _desired_cap['pageLoadStrategy'] = 'eager'
        _profile = webdriver.FirefoxProfile()
        _profile.set_preference('permissions.default.image', 2)

        # self._browser = webdriver.Remote('http://localhost:4444/wd/hub',
        #                                  desired_capabilities=_desired_cap)
        self._browser = webdriver.Firefox(capabilities=_desired_cap, firefox_profile=_profile)

        # For Chrome
        # _chromeOptions = webdriver.ChromeOptions()
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # _chromeOptions.add_experimental_option("prefs", prefs)
        # self._browser = webdriver.Chrome(chrome_options=_chromeOptions)
        #
        self._browser.implicitly_wait(10)

        logger.debug('start webdriver, name=%s, session_id=%s',
                     self._browser.name, self._browser.session_id)

    def get_start_url(self, url):
        """
        selenium获取页面
        :param url:
        :return:
        """
        logger.debug('browser get url: %s', url)
        for i in range(10):
            try:
                self._browser.get(url)
                break
            except selenium.common.exceptions.WebDriverException:
                pass
        else:
            raise SeleniumException(url)

    def click_next(self, next_pattern):
        """根据pattern"""

        pat_type = next_pattern['type']
        pattern = next_pattern['pattern']

        # 根据不同的模式调用相应函数
        func = getattr(self._browser, 'find_element_by_{}'.format(pat_type))
        try:
            next_link = func(pattern)
            next_link.click()
            logger.debug('browser click next page')
            return True
        except NoSuchElementException:
            logger.debug('no such element: %s - %s', pat_type, pattern)
            return False

    def quit(self):
        try:
            self._browser.quit()
        except:
            pass

    @property
    def page_source(self):
        return self._browser.page_source

    @property
    def current_url(self):
        return self._browser.current_url


class Task(object):
    """任务类"""

    def __init__(self):
        # 单独config module
        self._module = None
        # 项目default module
        self._proj_module = None

        self._immutable_item = None
        self._click_next = True

        self._conn = None
        self._cur = None

        self._db_cnt = 0
        self._crawl_status = 0
        self.original_date_in_db = None  # 数据库中最新抓取时间（原始值）
        self.last_date_in_db = None  # 数据库中最新抓取时间（减去threshold后的值）
        self.latest_issue_time_in_page = None  # 网页上最新数据发布时间
        self.threshold = 2  # 允许多抓取的时间阈值

        # 列表页部分hash，防止翻页不停止
        self._last_li_hash = ''

    def load(self, module):
        """装载导入模块"""
        if isinstance(module, str):
            self._module = importlib.import_module(module)
        elif inspect.ismodule(module):
            self._module = module

        logger.info('Load module=%s', self._module.__name__)

        # 加载项目默认module
        proj_file = PROJ_REGX_PAT.search(
            self._module.__name__).group(1) + 'default'
        proj_mod = importlib.import_module(proj_file)
        self._proj_module = proj_mod

    def _check_specs(self):
        """检查模块是否符合命名规范"""
        # 检查作者名
        assert self._module.author.lower() in self._module.__name__.lower()
        # 检查网站名是否为unicode
        assert isinstance(self._module.web_title, unicode)
        # 检查data_source
        url_struct = urlparse.urlparse(self._module.data_source)
        assert url_struct.path == ''
        # 检查data_souce是否与start_urls匹配
        domain_detail = tldextract.extract(url_struct.netloc)
        if domain_detail.suffix:
            tld = '.'.join((domain_detail.domain, domain_detail.suffix))
        else:
            tld = domain_detail.domain
        for url in self._module.start_urls:
            assert tld in url
        assert self._module.detail_pattern['sc']['target'] in ['html', 'clean_html']

    def _init(self):
        """初始化模块数据"""
        item = {}
        self.item = item
        # 基本信息
        item['author'] = self._module.author
        web_title = self._module.web_title
        item['web_title'] = web_title
        item['data_source'] = self._module.data_source

        # 列表页及详情页pattern
        patterns = {
            'index_pattern': self._module.index_pattern,
            'detail_pattern': self._module.detail_pattern
        }
        item['_patterns'] = patterns

        if SERVER_FLAG:
            # 服务器环境使用默认配置
            db_config = getattr(self._proj_module, 'db_config', None)
        else:
            # 本地测试使用各自config中配置
            db_config = getattr(self._module, 'db_config', None)

        item['_db_config'] = db_config
        self._connect_db()

        item['_start_urls'] = self._module.start_urls
        item['_task_urls'] = self._gen_task_urls()

    def _gen_task_urls(self):
        """生成start_url"""
        default_task_urls = {i: [i, 1] for i in self._module.start_urls}
        if not (self._conn and SERVER_FLAG):
            return default_task_urls

        sql = (
            'SELECT start_urls, crawl_status FROM crawl_log '
            'WHERE data_source=%s ORDER BY id DESC '
            'LIMIT 1'
        )
        self._cur.execute(sql, self.item['data_source'])
        row_set = self._cur.fetchone()
        if row_set:
            task_urls = {i[0]: i for i in json.loads(row_set[0])}
            # DEBUG ONLY
            # author xNathan, date: 2017/9/29 09:41
            # 增量抓取，如果上次正常退出，则task_urls 为默认源task_urls
            if row_set[1] == 0:
                task_urls = default_task_urls
        else:
            task_urls = default_task_urls
        return task_urls

    def _connect_db(self):
        """连接数据库"""
        if self.item['_db_config'] is None:
            return
        try:
            db_config = self.item['_db_config'].copy()
            del db_config['table']
            if 'charset' not in db_config:
                db_config['charset'] = 'utf8'
            if 'autocommit' not in db_config:
                db_config['autocommit'] = True
            self._conn = pymysql.connect(**db_config)
            self._cur = self._conn.cursor()
        except (pymysql.OperationalError, pymysql.InternalError) as e:
            logger.error("Can't connect to database: %s, %s",
                         self.item['_db_config'], e, exc_info=True)
            exit(1)
        except Exception as e:
            logger.error(e, exc_info=True)
            exit(1)

    def _get_item_link(self, base_url, element):
        """从列表页元素中获取a标签绝对路径"""
        d = pq(element)
        if d.is_('a'):
            href = d.attr('href')
        else:
            href = d.find('a').attr('href')

        if not href.startswith('http'):
            detail_url = urlparse.urljoin(base_url, href)
        else:
            detail_url = href

        return detail_url

    def _clean_item(self, item):
        """删除item中无需保存的值"""
        _item = item.copy()
        for each_key in _item.keys():
            if each_key.startswith('_'):
                del _item[each_key]
        return _item

    def _save_item(self, item):
        """保存item"""
        # 设置最新数据时间
        if self.latest_issue_time_in_page is None:
            self.latest_issue_time_in_page = item['issue_time']
        else:
            # 若页面发布时间比当前时间早一个月，则认为是错误时间
            if not item['issue_time'] or  (item['issue_time'] - self._start_time) > 3600 * 24 * 30:
                item['issue_time'] = -1
            if item['issue_time'] > self._start_time:
                self.latest_issue_time_in_page = self._start_time - 1
            if item['issue_time'] > self.latest_issue_time_in_page:
                self.latest_issue_time_in_page = item['issue_time']

        _item = self._clean_item(item)
        if 'url' not in _item:
            return

        db_config = self._immutable_item.get('_db_config')
        if not db_config:
            return
        if self.last_date_in_db is not None and \
                        item['issue_time'] != -1 and \
                        item['issue_time'] <= self.last_date_in_db:
            raise TaskFinishSignal
        table = db_config['table']
        qmarks = ', '.join(['%s'] * len(_item))
        columns = ', '.join(_item.keys())
        qry = "INSERT INTO %s (%s) VALUES (%s)" % (table, columns, qmarks)
        try:
            self._cur.execute(qry, _item.values())
            self._db_cnt += 1
        except pymysql.IntegrityError:
            # 有重复键值
            # TODO: 增量处理
            pass
        except Exception as e:
            logger.error("save_item error, item=%s, error=%s",
                         _item, e, exc_info=True)
            self._conn.rollback()

    def _parse_detail_page(self, item):
        url = item.get('url')
        if not url:
            if 'sc' not in item:
                item['sc'] = ''
            item['issue_time'] = ''
            item['title'] = ''
            return

        detail_pattern = item['_patterns']['detail_pattern']
        logger.info('parse detail: %s', url)

        try:
            res = downloader.get(url, headers=headers)
            if res.status_code == 404:
                logger.debug('skip 404 url: %s', item['url'])
                del item['url']
                return
            page = res.content
            encoding = chardet.detect(page)['encoding']
            if encoding == 'GB2312':
                encoding = 'gb18030'
            elif encoding is None:
                encoding = 'utf-8'
            page = page.decode(encoding, 'ignore')

            for key, pattern in detail_pattern.items():
                _parser = build_parser(pattern)
                _parser.parse(page)

                item[key] = _parser.result
        except Exception, e:
            logger.error("parse detail page error: %s", url, exc_info=True)
            raise

    def process_page(self, item_, base_url, page, index_pattern):
        """处理列表页"""
        list_pattern = index_pattern['_list']
        _parser = build_parser(list_pattern)
        _parser.parse(page)
        cur_li_hash = hashlib.md5(json.dumps(_parser.result)).hexdigest()
        if cur_li_hash == self._last_li_hash:
            # 两次请求列表页元素一致
            # 可能在最后一页，直接跳出
            logger.debug('break click loop')
            self._click_next = False
            return
        self._last_li_hash = cur_li_hash
        # 处理列表页详情链接
        for element in _parser.source:
            # 获取详情时，清空每个item
            item = copy.deepcopy(item_)
            item['url'] = self._get_item_link(base_url, element)

            for key, pattern in index_pattern.items():
                if key in ['_list', '_next_page']:
                    continue
                if pattern['pattern'].startswith('/html'):
                    _element = page
                else:
                    _element = element
                _parser = build_parser(pattern)
                _parser.parse(_element)
                item[key] = _parser.result
            # 执行自定义函数，处理列表页元素及item
            self._module.process_list_item(element, item)
            # 解析详情页
            self._parse_detail_page(item)
            if item.get('url'):
                # 执行自定义函数，处理获取详情页后的item
                self._module.process_detail_item(item)
                # 执行项目默认函数
                self._proj_module.process_item(item)
                # 保存item
                self._save_item(item)

            self._click_next = item.get('_click_next', True)

    def get_last_record_date(self):
        """
        :return None
        """
        # Database Version
        self._cur.execute(
            "SELECT last_date,latest_issue_time_in_page FROM {} WHERE data_source=%s ORDER BY id DESC LIMIT 1".format(
                'crawl_log'),
            (self._module.data_source,))
        rowset = self._cur.fetchone()
        logger.debug(self._cur._last_executed)
        if rowset:
            self.original_date_in_db,self.latest_issue_time_in_page = rowset[0],rowset[1]
            if self.original_date_in_db == -1:
                self.last_date_in_db = -1
                return
            finish_datetime = datetime.fromtimestamp(
                self.original_date_in_db) - timedelta(days=self.threshold)
            finish_timestamp = int(time.mktime(
                finish_datetime.date().timetuple()))
            self.last_date_in_db = finish_timestamp

        else:
            self.last_date_in_db = -1  # 2017-07-20 00:00:00  时间戳
            self.original_date_in_db = self.last_date_in_db

    def update_log(self):
        """存抓取日志"""
        last_date = self.latest_issue_time_in_page
        if self.last_date_in_db < 0:
            last_date = -1
        if self.latest_issue_time_in_page is None or self._crawl_status != 0:
            last_date = self.original_date_in_db
        if self._conn is None:
            return
        sql = (
            'INSERT INTO crawl_log(data_source, web_title,'
            'author, start_urls, start_time, insert_time,'
            'last_date, cnt, crawl_status, latest_issue_time_in_page) '
            'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        )
        data_source = self._module.data_source
        web_title = self._module.web_title
        author = self._module.author
        start_urls = json.dumps(self._immutable_item['_task_urls'].values())
        self._cur.execute(sql, (data_source, web_title, author, start_urls,
                                self._start_time, int(time.time()), last_date,
                                self._db_cnt, self._crawl_status, self.latest_issue_time_in_page))

    def handle_error(self, e):
        """处理所有错误"""
        logger.debug('handling error: %s', e)
        if isinstance(e, KeyboardInterrupt):
            return
        # TODO: 发邮件
        logger.error(e.message, exc_info=True)
        try:
            url = downloader.History._last_url
            request_body = downloader.History._last_response.request.body
            response_content = downloader.History._last_response.text.encode('utf-8')
        except:
            url = ''
            request_body = ''
            response_content = ''
        err_msg = 'url:\n{}\n\n=================\n'
        err_msg += 'err_msg:\n{}\n=================\n'
        err_msg += 'request_data:\n{}\n=================\n'
        err_msg += 'content:\n{}'
        if isinstance(e, SeleniumException):
            url = e.message
            request_body = None
            content = None
        err_msg = err_msg.format(url, traceback.format_exc(), request_body, response_content)
        self._crawl_status = 100
        author = self._module.author
        author_addr = default_config.author_mails.get(author, 'bug_cc@sequee.com')
        mod_name = self._module.__class__.__name__.split('.')[-1]
        mail_title = "【automatic_scraper】[{} - {}] {}".format(mod_name, author, type(e).__name__)
        if SERVER_FLAG:
            send_alert_email_to([author_addr], default_config.cc_addr, err_msg, mail_title)
        logger.debug('send email to author: %s', author_addr)
    
    def run(self):
        try:
            self.start()
            self.last_date_in_db = self.latest_issue_time_in_page
        except Exception as e:
            self.handle_error(e)
        finally:
            if SERVER_FLAG:
                self.update_log()
            # 关闭数据库
            if self._conn:
                self._conn.commit()
                self._cur.close()
                self._conn.close()
            try:
                self._browser.quit()
            except:
                pass

    def start(self):
        """启动任务"""
        self._start_time = int(time.time())
        # 检查模块规范
        self._check_specs()

        self._init()

        # 调用每个配置文件中的init
        self._module.init(self.item)

        # 初始化不可变item，深拷贝所有item对象
        self._immutable_item = copy.deepcopy(self.item)
        del self.item
        self.get_last_record_date()
        if not self._click_next:
            return
        self._browser = browser = Browser()
        for url, page_idx in self._immutable_item['_task_urls'].values():
            item = copy.deepcopy(self._immutable_item)
            cur_page_index = page_idx
            logger.info('processing start url: %s', url)
            item['_current_start_url'] = url  # 当前start_url
            item['_current_page'] = cur_page_index  # 当前页码
            logger.info('current page: %s', cur_page_index)

            index_pattern = item['_patterns']['index_pattern']
            next_page_pattern = index_pattern['_next_page']

            # 处理第一页
            browser.get_start_url(url)
            time.sleep(int(item.get('_delay_between_pages', 0)))
            page_source = browser.page_source
            self._immutable_item['_task_urls'][url] = [browser.current_url, cur_page_index]
            try:
                self.process_page(item, url, page_source, index_pattern)
            except TaskFinishSignal:
                logger.info('Task [{}] finished !'.format(url))

            # 翻页处理
            while self._click_next and browser.click_next(next_page_pattern):
                cur_page_index += 1
                item['_current_page'] = cur_page_index
                logger.info('current page: %s', cur_page_index)
                time.sleep(int(item.get('_delay_between_pages', 0)))
                self._immutable_item['_task_urls'][url] = [browser.current_url, cur_page_index]
                page_source = browser.page_source
                try:
                    self.process_page(item, url, page_source, index_pattern)
                except TaskFinishSignal:
                    logger.info('Task [{}] finished !'.format(url) )
                    break


        browser.quit()
        logger.info(u"%s 抓取完成", self._module.web_title)


def start(module):
    task = Task()
    task.load(module)
    task.run()
