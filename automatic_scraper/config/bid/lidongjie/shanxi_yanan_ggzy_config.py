# coding: utf-8
import time
import logging
import re

logger = logging.getLogger(__name__)

author = "lidongjie"
web_title = u"延安公共资源交易网"
data_source = 'http://www.yaggzyjy.cn'

start_urls = [
    #招标公告
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001001/004001001001/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001002/004001002001/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001007/004001007001/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001008/004001008001/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001011/004001011001/",
    # 资格预审公告
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001001/004001001002/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001002/004001002002/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001003/004001003002/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001007/004001007002/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001008/004001008002/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001011/004001011002/",
    # 变更公告
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001001/004001001003/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001002/004001002003/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001003/004001003003/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001008/004001008003/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001011/004001011003/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004007/004007001/004007001002/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004007/004007002/004007002002/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004007/004007003/004007003002/",
    # 中标公告
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001001/004001001004/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001002/004001002004/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001003/004001003004/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001007/004001007004/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001008/004001008004/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004001/004001011/004001011004/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004007/004007001/004007001003/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004007/004007002/004007002003/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004007/004007003/004007003003/",

    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004007/004007001/004007001001/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004007/004007002/004007002001/",
    "http://www.yaggzyjy.cn/Front_YanAn/jyxx/004007/004007003/004007003001/",

]

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'bid_data',
    'table': 'zhaotoubiao_copy'
}

# 列表页模板
index_pattern = {
    "_list": {'pattern': "//ul//li[@class='ewb-right-item clearfix']", 'type': 'xpath','target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"下页 >", 'type': 'partial_link_text', 'target': 'html', 'custom_func_name': ''},
    "_issue_time": {'pattern': "//span", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@id='mainContent']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//h2[@class='article-title']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S"
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'陕西—延安'
    del item['web_title']
    item['_delay_between_pages'] = 5


def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    if item['url']=='http://www.yaggzyjy.cn/Front_YanAn/%e7%bb%b4%e6%8a%a4%e4%b8%ad.htm?aspxerrorpath=/Front_YanAn/InfoDetail/default.aspx':
        del item['url']
        return
    logger.debug(item['url'])
    # 停止翻页


def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    if not item.get('url'):
        return

    if '004001001001' in item['_current_start_url'] or '004001002001' in item['_current_start_url']  or '004001003001' in item[
        '_current_start_url'] or '004001007001' in item[
        '_current_start_url'] or '004001008001' in item['_current_start_url'] or '004001011001' in item[
        '_current_start_url']:
        item['bid_type'] = 1
    elif '004001001002' in item['_current_start_url'] or '004001002002' in item['_current_start_url'] or '004001003002' in item[
        '_current_start_url'] or '004001007002' in item['_current_start_url'] or '004001008002' in item[
        '_current_start_url'] or '004001011002' in item['_current_start_url'] :
        item['bid_type'] = 7
    elif '004001001002' in item['_current_start_url'] or '004001002002' in item['_current_start_url'] or '004001003002' in item[
        '_current_start_url'] or '004001007002' in item['_current_start_url'] or '004001008002' in item[
        '_current_start_url'] or '004001011002' in item['_current_start_url'] or '004007001002' in item[
        '_current_start_url'] or '004007002002' in item[
        '_current_start_url'] or '004007003002' in item['_current_start_url'] :
        item['bid_type'] = 2
    elif '004001001004' in item['_current_start_url'] or '004001002004' in item[
        '_current_start_url'] or '004001003004' in item[
        '_current_start_url'] or '004001007004' in item['_current_start_url'] or '004001008004' in item[
        '_current_start_url'] or '004001011004' in item['_current_start_url'] or '004007001003' in item[
        '_current_start_url'] or '004007002003' in item[
        '_current_start_url'] or '004007003003' in item['_current_start_url']:
        item['bid_type'] = 0
    else:
        item['bid_type'] = '-1'
    if re.search(u'(废标)|(流标)|(失败)|(终止)', item['sc']):
        item['is_liubiao'] = 1
    else:
        item['is_liubiao'] = 0
    logger.debug('%s   %s', item['title'], item['_issue_time'])
    item['issue_time'] = int(time.mktime(time.strptime(item['_issue_time'], '%Y-%m-%d')))
    if len(item['sc']) != 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0
