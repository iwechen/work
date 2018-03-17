# coding: utf-8
import time
import logging
from bs4 import BeautifulSoup
import hashlib
import re

logger = logging.getLogger(__name__)

author = "huangtaiwu"
web_title = u"南平市公共资源交易中心"
data_source = 'http://www.npggzy.gov.cn'

start_urls = [
    # "http://www.npggzy.gov.cn/npztb/jsgc/010001/",#1
    # "http://www.npggzy.gov.cn/npztb/jsgc/010002/",#2
    # "http://www.npggzy.gov.cn/npztb/jsgc/010004/",#4
    # "http://www.npggzy.gov.cn/npztb/jsgc/010005/",#0
    "http://www.npggzy.gov.cn/npztb/zfjzcg/009001/",  # 1
    "http://www.npggzy.gov.cn/npztb/zfjzcg/009003/",  # 0
    "http://www.npggzy.gov.cn/npztb/zfjzcg/009004/",  # 2
]

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'huang960428',
    'database': 'bid_data',
    'table': 'zhaotoubiao'
}

# 列表页模板
index_pattern = {
    "_list": {'pattern': "//ul[@class='content-list clearfix']/li", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[@onclick and text()='下页 >']", 'type': 'xpath', 'target': 'html',
                   'custom_func_name': ''},
    "issue_time": {'pattern': "//span[@class='time']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//span[@class='link-content']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//table[@style='table-layout:fixed']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "title": {'pattern': "//div[@align='center']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'福建省-南平市'
    del item['web_title']


def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    # 停止翻页
    if re.search('/010001/|/009001/',item['_current_start_url']):
        item['bid_type'] = 1
    elif re.search('/010005/|/009003/',item['_current_start_url']):
        item['bid_type'] = 0
    elif re.search('/010002/|/009004/',item['_current_start_url']):
        item['bid_type'] = 2
    else:
        item['bid_type'] = 4
    if item['url']=='http://www.npzbtb.gov.cn/infolist.asp?id=21135':
        del item['url']
    logger.debug(u"{} {}".format(item['title'], item['issue_time']))
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "%Y-%m-%d")))
    # if item['_current_page'] == 10:
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


