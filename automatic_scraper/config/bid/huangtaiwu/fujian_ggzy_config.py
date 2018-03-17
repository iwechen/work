# coding: utf-8
import time
import logging
from bs4 import BeautifulSoup
import hashlib
import re

logger = logging.getLogger(__name__)

author = "huangtaiwu"
web_title = u"福建省公共资源交易网"
data_source = 'http://www.fjggzyjy.cn'

start_urls = [
    "http://www.fjggzyjy.cn/news/category/10/",#1
    "http://www.fjggzyjy.cn/news/category/11/",#2
    "http://www.fjggzyjy.cn/news/category/12/",#0
    "http://www.fjggzyjy.cn/news/category/52/",#1
    "http://www.fjggzyjy.cn/news/category/53/",#2
    "http://www.fjggzyjy.cn/news/category/55/",#4
    "http://www.fjggzyjy.cn/news/category/56/",#0

]

db_config = {
    "host": "rm-2zemi93gd355084beo.mysql.rds.aliyuncs.com",
    "user": "bid_base",
    "password": "Bid_Base_2017",
    "database": "bid_base",
    "port": 3306,
    'table': 'zhaotoubiao_max'
}

# 列表页模板
index_pattern = {
    "_list": {'pattern': "//a[@class='btn btn-default article-list-single']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[@href]//span[text()='下一页 »' ]", 'type': 'xpath', 'target': 'html',
                   'custom_func_name': ''},
    "issue_time": {'pattern': "//span[@class='article-list-date']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//span[@class='article-list-text']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='layout-article']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "title": {'pattern': "//div[@align='center']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'福建省'
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
    if re.search('/10/|/52/',item['_current_start_url']):
        item['bid_type'] = 1
    elif re.search('/12/|/56/',item['_current_start_url']):
        item['bid_type'] = 0
    elif re.search('/11/|/53/',item['_current_start_url']):
        item['bid_type'] = 2
    else:
        item['bid_type'] = 4

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


