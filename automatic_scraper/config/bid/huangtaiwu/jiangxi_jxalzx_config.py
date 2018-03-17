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
web_title = u"江西省安澜工程咨询有限公司"
data_source = 'http://www.jxalzx.com'

start_urls = [
    "http://www.jxalzx.com/article_list.asp?type=5&parentid=5",  # 1
    "http://www.jxalzx.com/article_list.asp?type=6&parentid=6", # 2
    "http://www.jxalzx.com/article_list.asp?type=8&parentid=8", # 0,4

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
    "_list": {'pattern': "//div[@class='page_content']/table[1]//tr", 'type': 'xpath', 'target': 'html','custom_func_name': ''},
    "_next_page": {'pattern': u"//a[@href and text()='下一页']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "issue_time": {'pattern': "//td[4]", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

}
# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='article_show_content']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'江西省'
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
    if re.search('parentid=5', item['_current_start_url']):
        item['bid_type'] = 1
    elif re.search('parentid=6', item['_current_start_url']):
        item['bid_type'] = 2
    elif re.search('parentid=8', item['_current_start_url']):
        item['bid_type'] = 0
    else:
        item['bid_type'] = -1
    if re.search(u'中标候选人|中标候选', item['title']):
        item['bid_type'] = 4
    if re.search(u'更正|更改', item['title']):
        item['bid_type'] = 2

    logger.debug(u"{} {}".format(item['title'], item['issue_time']))
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "[%Y/%m/%d]")))

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
