# coding: utf-8
import time
import logging
import re
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

author = "lihailin"
web_title = u"广东广招招标采购有限公司"
data_source = 'http://www.gztpc.com'

start_urls = [
    #招标公告
    "http://www.gztpc.com/tender/list?pid=4028e68133f22e130133f2a837750000&pageNo=1",
    #中标
    "http://www.gztpc.com/tender/list?pid=4028e68133f22e130133f2aa5a780003&pageNo=1",
    #中标候选人
    "http://www.gztpc.com/tender/list?pid=4028e68133f22e130133f2aa297a0002&pageNo=1",
    #变更澄清
    "http://www.gztpc.com/tender/list?pid=4028e68133f22e130133f2a893490001&pageNo=1"
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
    "_list": {'pattern': "//ul[@class='list']//li", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "issue_time": {'pattern': "//span", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[contains(text(), '下一页')]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
}
# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//td[@class='content']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'广东省'
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
    if '837750000' in item['_current_start_url']:
        item['bid_type'] = 1
    if '5a780003' in item['_current_start_url']:
        item['bid_type'] = 0
    if '893490001' in item['_current_start_url']:
        item['bid_type'] = 2
    if '297a0002' in item['_current_start_url']:
        item['bid_type'] = 4
    item['issue_time'] = re.search(r'\((.*)\)', item['issue_time']).group(1).strip()
    try:
        item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], u"%Y-%m-%d")))
    except:
        del item['url']
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


