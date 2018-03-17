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
web_title = u"湘潭市公共资源交易中心"
data_source = 'http://ggzy.xiangtan.gov.cn'

start_urls = [
    "http://ggzy.xiangtan.gov.cn/cggg/index.jhtml",#1
    "http://ggzy.xiangtan.gov.cn/gzgg/index.jhtml",#2
    "http://ggzy.xiangtan.gov.cn/jggg/index.jhtml",#0
    "http://ggzy.xiangtan.gov.cn/zbgg/index.jhtml",#1
    "http://ggzy.xiangtan.gov.cn/zbhxrgs/index.jhtml",#4
    "http://ggzy.xiangtan.gov.cn/zbxx/index.jhtml",#0
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
    "_list": {'pattern': "//div[@class='gngjList']//li", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[@onclick and text()='下一页']", 'type': 'xpath', 'target': 'html',
                   'custom_func_name': ''},
    "issue_time": {'pattern': "//span", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}
# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='newsCon']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "title": {'pattern': "//div[@align='center']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'湖南省-湘潭市'
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
    if re.search('/cggg/|/zbgg/',item['_current_start_url']):
        item['bid_type'] = 1
    elif re.search('/gzgg/',item['_current_start_url']):
        item['bid_type'] = 2
    elif re.search('/jggg/|/zbxx/',item['_current_start_url']):
        item['bid_type'] = 0
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


