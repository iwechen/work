# coding: utf-8
import time
import logging
from bs4 import BeautifulSoup
import hashlib

logger = logging.getLogger(__name__)

author = "Denglixi"
web_title = u"池州公共资源交易平台"
data_source = 'http://www.czztbj.cn'

start_urls = [
    # 招标
    "http://www.czztbj.cn/chiztpfront/jyxx/002001/002001001/",
    "http://www.czztbj.cn/chiztpfront/jyxx/002002/002002001/",

    # 中标
    "http://www.czztbj.cn/chiztpfront/jyxx/002001/002001003/",
    "http://www.czztbj.cn/chiztpfront/jyxx/002002/002002003/",

    # 变更
    "http://www.czztbj.cn/chiztpfront/jyxx/002001/002001005/",
    "http://www.czztbj.cn/chiztpfront/jyxx/002002/002002004/",

    # 预中标
    "http://www.czztbj.cn/chiztpfront/jyxx/002001/002001002/",
    "http://www.czztbj.cn/chiztpfront/jyxx/002002/002002002/",
]

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '114514',
    'database': 'bid_data',
    'table': 'zhaotoubiao'
}

# 列表页模板
index_pattern = {
    "_list": {'pattern': "//div[@style='width:980px; margin:10px;']//tr[@height='30']", 'type': 'xpath',
              'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//td[text() = '下页 >' and @onclick]", 'type': 'xpath', 'target': 'html',
                   'custom_func_name': ''},
    "issue_time": {'pattern': "//td[@width='80']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a/@title", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//table[@id='tblInfo']",
           'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "title": {'pattern': "//div[@align='center']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['_delay_between_pages'] = 2

def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    # 停止翻页
    if '002001001' in item['_current_start_url'] or '002002001' in item[
        '_current_start_url']:
        item['bid_type'] = 1

    elif '002001003' in item['_current_start_url'] or '002002003' in item[
        '_current_start_url']:
        item['bid_type'] = 0
    elif '002001005' in item['_current_start_url'] or '002002004' in item[
        '_current_start_url']:
        item['bid_type'] = 2
    elif '002001002' in item['_current_start_url'] or '002002002' in item[
        '_current_start_url']:
        item['bid_type'] = 4
    # logger.debug(u"{} {}".format(item['title'], item['issue_time']))
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "[%Y-%m-%d]")))
    # if item['_current_page'] == 2:
    #     item['_click_next'] = False


def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    if len(item['sc']) > 100:
        item['is_get'] = 1
    else:
        item['is_get'] = 0
