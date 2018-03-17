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
web_title = u"广东元正招标采购有限公司"
data_source = 'http://www.gdbidding.com'

start_urls = [
    "http://www.gdbidding.com/zbxx_list.asp?sys_classid=1",#1
    "http://www.gdbidding.com/zbxx_list.asp?sys_classid=3",#2
    "http://www.gdbidding.com/zbxx_list.asp?sys_classid=4",#4
    "http://www.gdbidding.com/zbxx_list.asp?sys_classid=2",#0
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
    "_list": {'pattern': "//div[@class='YYR1b']//li", 'type': 'xpath', 'target': 'html','custom_func_name': ''},
    "_next_page": {'pattern': u"//a[@href]//strong[text()='>>']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "issue_time": {'pattern': "//span", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

}
# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='YY013c']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    "title": {'pattern': "//div[@class='YY013b']/p", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    # "title": {'pattern': "//div[@align='center']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'广东省'
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
    if re.search('sys_classid=1', item['_current_start_url']):
        item['bid_type'] = 1
    elif re.search('sys_classid=3', item['_current_start_url']):
        item['bid_type'] = 2
    elif re.search('sys_classid=4', item['_current_start_url']):
        item['bid_type'] = 4
    elif re.search('sys_classid=2', item['_current_start_url']):
        item['bid_type'] = 0
    else:
        item['bid_type'] = -1

        # if item['_current_page'] == 10:
        #     item['_click_next'] = False
    item['issue_time'] = re.search('(\d+-\d+-\d+)', item['issue_time']).group(1)
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "%Y-%m-%d")))

def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    logger.debug(u"{} {}".format(item['title'], item['issue_time']))
    if len(item['sc']) > 100:
        item['is_get'] = 1
    else:
        item['is_get'] = 0
