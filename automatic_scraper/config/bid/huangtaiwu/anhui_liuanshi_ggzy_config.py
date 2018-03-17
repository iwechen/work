# coding: utf-8
import time
import logging
from bs4 import BeautifulSoup
import hashlib
import re

logger = logging.getLogger(__name__)

author = "huangtaiwu"
web_title = u"六安市公共资源交易网"
data_source = 'http://www.laztb.gov.cn'

start_urls = [
    "http://www.laztb.gov.cn/lazbb/jyxx/003001/003001001/003001001001/",#1
    "http://www.laztb.gov.cn/lazbb/jyxx/003001/003001001/003001001002/",#1
    "http://www.laztb.gov.cn/lazbb/jyxx/003001/003001001/003001001003/",#1
    "http://www.laztb.gov.cn/lazbb/jyxx/003001/003001001/003001001004/",#1
    "http://www.laztb.gov.cn/lazbb/jyxx/003001/003001002/003001002001/",#2
    "http://www.laztb.gov.cn/lazbb/jyxx/003001/003001002/003001002002/",#2
    "http://www.laztb.gov.cn/lazbb/jyxx/003001/003001002/003001002003/",#2
    "http://www.laztb.gov.cn/lazbb/jyxx/003001/003001006/003001006001/",#4
    "http://www.laztb.gov.cn/lazbb/jyxx/003001/003001006/003001006002/",#4
    "http://www.laztb.gov.cn/lazbb/jyxx/003001/003001006/003001006003/",#4
    "http://www.laztb.gov.cn/lazbb/jyxx/003001/003001003/003001003001/",#0
    "http://www.laztb.gov.cn/lazbb/jyxx/003001/003001003/003001003002/",#0
    "http://www.laztb.gov.cn/lazbb/jyxx/003001/003001003/003001003003/",#0
    "http://www.laztb.gov.cn/lazbb/jyxx/003002/003002001/003002001001/",#1
    "http://www.laztb.gov.cn/lazbb/jyxx/003002/003002001/003002001002/",#1
    "http://www.laztb.gov.cn/lazbb/jyxx/003002/003002001/003002001003/",#1
    "http://www.laztb.gov.cn/lazbb/jyxx/003002/003002002/003002002001/",#2
    "http://www.laztb.gov.cn/lazbb/jyxx/003002/003002002/003002002002/",#2
    "http://www.laztb.gov.cn/lazbb/jyxx/003002/003002002/003002002003/",#2
    "http://www.laztb.gov.cn/lazbb/jyxx/003002/003002004/003002004001/",#0
    "http://www.laztb.gov.cn/lazbb/jyxx/003002/003002004/003002004002/",#0
    "http://www.laztb.gov.cn/lazbb/jyxx/003002/003002004/003002004003/",#0

]

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "huang960428",
    "database": "bid_data",
    "port": 3306,
    'table': 'zhaotoubiao'
}

# 列表页模板
index_pattern = {
    "_list": {'pattern': "//tr[@height='30']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//td[text()='下页 >' and @onclick]", 'type': 'xpath', 'target': 'html',
                   'custom_func_name': ''},
    "issue_time": {'pattern': "//td [@style='text-align:right' and @width='80']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@id='jsgc_bcgg1_cont']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "title": {'pattern': "//div[@align='center']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'安徽省-六安市'
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
    if re.search('003001001|003002001',item['_current_start_url']):
        item['bid_type'] = 1
    elif re.search('003001003|003002004',item['_current_start_url']):
        item['bid_type'] = 0
    elif re.search('003001002|003002002',item['_current_start_url']):
        item['bid_type'] = 2
    else:
        item['bid_type'] = 4

    if item['url']=='http://www.szzbtb.cn/szzb/InfoDetail/?infoid=4b6fca13-54ab-43f2-8efe-34d06f787b58&categoryNum=021002&siteid=1':
        del item['url']
        return
    logger.debug(u"{} {}".format(item['title'], item['issue_time']))
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "[%Y-%m-%d]")))
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


