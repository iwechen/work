# coding: utf-8
import time
import logging
import re
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

author = "lihailin"
web_title = u"中邦国际(招标、变更)"
data_source = 'http://www.cobo91.com'

start_urls = [
    #中标变更
   "http://www.cobo91.com/project/affiche.aspx?typeId=3",
    "http://www.cobo91.com/project/affiche.aspx?typeId=4"
]

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'bid_data',
    'table': 'zhaotoubiao'
}

# 列表页模板
index_pattern = {
    "_list": {'pattern': "//table[@id='StaffList']//tr//a/parent::td/parent::tr", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "issue_time": {'pattern': "//td[3]", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[contains(text(), '下一页') ]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//td[@class='text']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'中邦国际'
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
    if '3' in item['_current_start_url']:
        item['bid_type'] = 0
    elif '4' in item['_current_start_url']:
        item['bid_type'] = 2
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], u"%Y-%m-%d")))
    # print item['issue_time']
    logging.debug(item['title'])
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

