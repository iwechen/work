# coding: utf-8
import time
import logging
import re
from  bs4 import BeautifulSoup
import re
logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"科杰声屏障"
data_source = 'http://www.anpingkejie.com'

start_urls = [
    # 招标公告

     #政府采购
    "http://www.anpingkejie.com/news",





]

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'asd123',
    'database': 'bid_data',
    'table': 'zhaotoubiao'
}

# 列表页模板
index_pattern = {
    "_list": {'pattern': "//div[@class='xz']//dt/a[2]",'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[contains(text(),'尾页') and @href]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//strong", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='news-neirong ']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},

    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region'] = u'科杰声'
    item['_delay_between_pages'] = 3


def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """


    item['bid_type'] = 1
    item['issue_time'] = int(time.mktime(time.strptime('2017-11-14', u"%Y-%m-%d")))
    if re.search(ur'流标|终止|废标', item['title']):
        item['is_liubiao'] = 1
        # 停止翻页
    # if item['_current_page'] == int(page_count):
    #     item['_click_next'] = False


def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    if u'招标|公告' not in item['title']:
        return


    if len(item['sc']) > 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0

