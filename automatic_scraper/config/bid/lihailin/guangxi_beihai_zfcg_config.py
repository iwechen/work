# coding: utf-8
import time
import logging
import re
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

author = "lihailin"
web_title = u"北海市公共资源交易中心"
data_source = 'http://www.beihaizc.com.cn'

start_urls = [
    #采购预公告
    "http://www.beihaizc.com.cn/g_info_list_1.asp?page=1&checkindate=&checkoutdate=&keyw=&cata1_id=11&cata2_id=12&id=12",
    #采购公告
    "http://www.beihaizc.com.cn/g_info_list_1.asp?page=1&checkindate=&checkoutdate=&keyw=&cata1_id=11&cata2_id=4&id=4",
    #中标公告
    "http://www.beihaizc.com.cn/g_info_list_1.asp?page=1&checkindate=&checkoutdate=&keyw=&cata1_id=11&cata2_id=5&id=5",
    #更正公告
    "http://www.beihaizc.com.cn/g_info_list_1.asp?page=1&checkindate=&checkoutdate=&keyw=&cata1_id=11&cata2_id=14&id=14",
    #废标公告
    "http://www.beihaizc.com.cn/g_info_list_1.asp?page=1&checkindate=&checkoutdate=&keyw=&cata1_id=11&cata2_id=13&id=13"
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
    "_list": {'pattern': "//td[@align='left']/a", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[contains(text(), '下页')]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    # "issue_time": {'pattern': "//tr[@align='center']//td[@align='center'][2]", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {

    "sc": {'pattern': "//td[@style='line-height:30px;']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    "title": {'pattern': "//td[@class='STYLE2']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "issue_time": {'pattern': "//td[@bgcolor='#E6E6E6']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'广西壮族自治区-北海市'
    del item['web_title']
    item['_delay_between_pages'] = 1

def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    # 停止翻页
    if 'id=12' in item['_current_start_url'] or 'id=4' in item['_current_start_url']:
        item['bid_type'] = 1
    elif 'id=5' in item['_current_start_url']:
        item['bid_type'] = 0
    elif 'id=14' in item['_current_start_url']:
        item['bid_type'] = 2
    if 'id=13' in item['_current_start_url']:
        item['is_liubiao'] = 1
    else:
        item['is_liubiao'] =0
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
    try:
        item['issue_time'] = re.search(u'(20.*)浏览',item['issue_time']).group(1).strip()
        # print item['issue_time']
        item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], u"%Y-%m-%d　%H:%M:%S")))
    except:
        return



