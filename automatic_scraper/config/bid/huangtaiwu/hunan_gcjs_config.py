# coding: utf-8
import time
import logging
from bs4 import BeautifulSoup
import hashlib
import re
import requests
import urlparse

logger = logging.getLogger(__name__)

author = "huangtaiwu"
web_title = u"	湖南省建设工程招标投标网 "
data_source = 'http://www.hnztb.org'

start_urls = [
    "http://www.hnztb.org/Index.aspx?action=ucBiddingList&modelCode=0003&ItemCode=000005001&name=%u5efa%u8bbe%u5de5%u7a0b%u62db%u6807%u4fe1%u606f",#1
    "http://www.hnztb.org/Index.aspx?action=ucBiddingList&modelCode=0004&ItemCode=000009001&name=%u5efa%u7b51%u5de5%u7a0b%u4e2d%u6807%u7ed3%u679c",#4
    "http://www.hnztb.org/Index.aspx?action=ucBiddingList&modelCode=0004&ItemCode=000009001&name=%E5%BB%BA%E7%AD%91%E5%B7%A5%E7%A8%8B%E4%B8%AD%E6%A0%87%E7%BB%93%E6%9E%9C",#0
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
    "_list": {'pattern': "//tr[@class='trStyle']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[@href and text()='后一页']", 'type': 'xpath', 'target': 'html',
                   'custom_func_name': ''},
    "issue_time": {'pattern': "//span", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}
# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//table[@id='Table3']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "title": {'pattern': "//div[@align='center']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'湖南省'
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
    if re.search('%u5efa%u8bbe%u5de5%u7a0b%u62db%u6807%u4fe1%u606f',item['_current_start_url']):
        item['bid_type'] = 1
    elif re.search('%u5efa%u7b51%u5de5%u7a0b%u4e2d%u6807%u7ed3%u679c',item['_current_start_url']):
        item['bid_type'] = 4
    elif re.search('%E5%BB%BA%E7%AD%91%E5%B7%A5%E7%A8%8B%E4%B8%AD%E6%A0%87%E7%BB%93%E6%9E%9C',item['_current_start_url']):
        item['bid_type'] = 0
    else:
        item['bid_type'] = -1

    if re.search('废标|流标',item['title']):
        item['is_liubiao']= 1

    logger.debug(u"{} {}".format(item['title'], item['issue_time']))
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "(%Y-%m-%d)")))
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


