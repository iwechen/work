# coding: utf-8
import time
import logging
import re
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

author = "lihailin"
web_title = u"广东省洁净技术行业协会"
data_source = 'http://www.gact.org.cn'

start_urls = [
    "http://www.gact.org.cn/EnNews-368-0-0.html",
    "http://www.gact.org.cn/EnNews-369-0-0.html"
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
    "_list": {'pattern': "//td[@colspan='2']//table[@width='1000' and @border='0']//tr[position()>1]//td[@height='37']//div[@align='left']//a", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': ".", 'type': 'xpath', 'target': 'text','custom_func_name': ''},
    "_next_page": {'pattern': u"//a[contains(text(), '下一页')]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
}
# 详情页模板
detail_pattern = {
    "issue_time": {'pattern': "//div[@class='a12hui' and @align='center']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "sc": {'pattern': "//div[@class='wenzi' and @align='left']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'华润纺织集团招标与采购网'
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
    if '368' in item['_current_start_url']:
        item['bid_type'] = 1
    elif '369' in item['_current_start_url']:
        item['bid_type'] = 0
    logging.debug(item['title'])
def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    try:
        item['issue_time'] = re.search(u'(\d+-\d+-\d+ \d+:\d+:\d+)', item['issue_time']).group(1)
        item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], u"%Y-%m-%d %H:%M:%S")))
    except:
        del item['url']
    if len(item['sc']) > 100:
        item['is_get'] = 1
    else:
        item['is_get'] = 0


