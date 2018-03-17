# coding: utf-8
import time
import logging
import re
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

author = "lihailin"
web_title = u"岳阳市建设工程招标投标监管网"
data_source = 'http://bidding.yyjs.gov.cn'

start_urls = [
    #招标
    "http://bidding.yyjs.gov.cn/Portal/PartPage.aspx?PartID=bacef2cc-9f81-4957-b2b0-9526b51ad08b&isorgid=&bidMode=&Page=1",
    "http://bidding.yyjs.gov.cn/Portal/PartPage.aspx?PartID=011e13a4-3a19-4cag-9fb1-e0f18385A001&isorgid=&bidMode=&Page=1",
    #中标
    "http://bidding.yyjs.gov.cn/Portal/PartPage.aspx?PartID=52ee2305-b8f7-41a8-9e15-c0b88667b15a&isorgid=&bidMode=&Page=1",
    "http://bidding.yyjs.gov.cn/Portal/PartPage.aspx?PartID=c202e3d4-a235-426b-b48a-1ed52391b6c3&isorgid=&bidMode=&Page=1"
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
    "_list": {'pattern': "//dd", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[contains(text(), '下一页')]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "issue_time": {'pattern': "//span", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

}

# 详情页模板
detail_pattern = {

    "sc": {'pattern': "//span[@id='ctl_Content']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'湖南省-岳阳市'
    del item['web_title']
    item['_delay_between_pages'] = 3

def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    if 'PartID=bacef2cc-9f81-4957-b2b0-9526b51ad08b' in item['_current_start_url'] or 'PartID=011e13a4-3a19-4cag-9fb1-e0f18385A001' in item['_current_start_url']:
        item['bid_type'] = 1
    elif 'PartID=52ee2305-b8f7-41a8-9e15-c0b88667b15a' in item['_current_start_url'] or 'PartID=c202e3d4-a235-426b-b48a-1ed52391b6c3' in item['_current_start_url']:
        item['bid_type'] = 0
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'],"[%Y-%m-%d]")))
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



