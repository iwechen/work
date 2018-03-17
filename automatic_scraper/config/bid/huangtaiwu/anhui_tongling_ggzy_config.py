# coding: utf-8
import time
import logging
from bs4 import BeautifulSoup
import hashlib
import re

logger = logging.getLogger(__name__)

author = "huangtaiwu"
web_title = u"铜陵市公共资源交易"
data_source = 'http://www.tlzbcg.com'

start_urls = [
    "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007001001",#1
    "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007001002",#2
    "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007001004",#0
    "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006001001",#1
    "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006001002",#2
    "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006001003",#4
    "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006001004",#0
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
    "_list": {'pattern': "//table[@id='DataGrid1']//tr", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//div[text()='下页 >' and @onclick]", 'type': 'xpath', 'target': 'html',
                   'custom_func_name': ''},
    "issue_time": {'pattern': "//span", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a[@class='zhaobiao']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='container clearfix']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "title": {'pattern': "//div[@align='center']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'安徽省-铜陵市'
    del item['web_title']
    item['_delay_between_pages'] = 1.5


def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    # 停止翻页
    if re.search('007001001|006001001',item['_current_start_url']):
        item['bid_type'] = 1
    elif re.search('007001002|006001002',item['_current_start_url']):
        item['bid_type'] = 2
    elif re.search('007001004|006001004',item['_current_start_url']):
        item['bid_type'] = 0
    else:
        item['bid_type'] = 4
    item['issue_time'] = "20"+item['issue_time']
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


