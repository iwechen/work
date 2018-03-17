# coding: utf-8
import time
import logging
import re
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

author = "lihailin"
web_title = u"张掖市公共资源交易中心高台县分中心"
data_source = 'http://ggzy.gaotai.gov.cn'

start_urls = [
    #招标中标变更公告
    "http://ggzy.gaotai.gov.cn/Category_635/Index.aspx",
    "http://ggzy.gaotai.gov.cn/Category_636/Index.aspx",
    "http://ggzy.gaotai.gov.cn/Category_637/Index.aspx",

    "http://ggzy.gaotai.gov.cn/Category_630/Index.aspx",
    "http://ggzy.gaotai.gov.cn/Category_645/Index.aspx",
    "http://ggzy.gaotai.gov.cn/Category_631/Index.aspx"
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
    "_list": {'pattern': "//div[@class='tlist']//li//a[@target='_blank']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': ".", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[contains(text(), '下一页')]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "issue_time": {'pattern': "//div[@class='baseinfo']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "sc": {'pattern': "//div[@class='content mycontent']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'甘肃省-张掖市'
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
    if '635' in item['_current_start_url'] or '630' in item['_current_start_url']:
        item['bid_type'] = 1
    elif '636' in item['_current_start_url'] or '645' in item['_current_start_url']:
        item['bid_type'] = 0
    elif '637' in item['_current_start_url'] or '631' in item['_current_start_url']:
        item['bid_type'] = 2
    logging.debug(item['title'])
def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    item['issue_time'] = re.search(u'(\d+年\d+月\d+日)', item['issue_time']).group(1)
    try:
        item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], u"%Y年%m月%d日")))
    except:
        del item['url']
    if len(item['sc']) > 100:
        item['is_get'] = 1
    else:
        item['is_get'] = 0


