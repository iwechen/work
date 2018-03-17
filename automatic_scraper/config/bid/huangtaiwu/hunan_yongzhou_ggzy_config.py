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
web_title = u"永州市公共资源交易中心"
data_source = 'http://ggzy.yzcity.gov.cn'

start_urls = [
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004001/004001001/004001001001/",#1
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004001/004001001/004001001002/",#1
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004001/004001001/004001001003/",#1
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004001/004001001/004001001004/",#1
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004001/004001002/004001002001/",#2
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004001/004001002/004001002002/",#2
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004001/004001002/004001002003/",#2
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004001/004001004/004001004001/",#0
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004001/004001004/004001004002/",#0
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004001/004001004/004001004003/",#0
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004001/004001004/004001004004/",#0
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004002/004002001/004002001001/",#1
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004002/004002001/004002001002/",#1
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004002/004002001/004002001003/",#1
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004002/004002002/004002002001/",#2
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004002/004002002/004002002002/",#2
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004002/004002002/004002002003/",#2
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004002/004002004/004002004001/",#0
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004002/004002004/004002004002/",#0
    "http://ggzy.yzcity.gov.cn/yzweb/jyxx/004002/004002004/004002004003/",#0
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
    "_list": {'pattern': "//tr[@height='21']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//a[@href]/img[@src='/yzweb/images/page/nextn.gif']", 'type': 'xpath', 'target': 'html',
                   'custom_func_name': ''},
    "issue_time": {'pattern': "//td[4]", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}
# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//td[@id='TDContent']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "title": {'pattern': "//div[@align='center']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'湖南省-永州市'
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
    if re.search('004001001|004002001',item['_current_start_url']):
        item['bid_type'] = 1
    elif re.search('004001004|004002004',item['_current_start_url']):
        item['bid_type'] = 0
    elif re.search('004001002|004002002',item['_current_start_url']):
        item['bid_type'] = 2
    else:
        item['bid_type'] = 4

    soup = BeautifulSoup(list_element, 'html.parser')
    href = soup.find('a').attrs['href']
    detail_url = urlparse.urljoin(item['_current_start_url'], href)
    res = requests.get(detail_url, stream=True)
    if int(res.headers['content-length']) < 500:
        del item['url']

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


