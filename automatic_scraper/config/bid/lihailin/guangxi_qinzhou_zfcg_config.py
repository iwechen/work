# coding: utf-8
import time
import logging
import re
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

author = "lihailin"
web_title = u"钦州市政府采购中心"
data_source = 'http://www.qzzfcg.cn'

start_urls = [
    #采购公告
    "http://www.qzzfcg.cn/xl/?l=%E9%87%87%E8%B4%AD%E4%BF%A1%E6%81%AF%2C%E9%87%87%E8%B4%AD%E5%85%AC%E5%91%8A",
    #变更公告
    "http://www.qzzfcg.cn/xl/?l=%E9%87%87%E8%B4%AD%E4%BF%A1%E6%81%AF%2C%E5%8F%98%E6%9B%B4%E5%85%AC%E5%91%8A",
    #中标公告
    "http://www.qzzfcg.cn/xl/?l=%E9%87%87%E8%B4%AD%E4%BF%A1%E6%81%AF%2C%E4%B8%AD%E6%A0%87%E5%85%AC%E5%91%8A"
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
    "_list": {'pattern': "//ol[@class='list']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//a[(text()='>')]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "issue_time": {'pattern': "//li[@class='xd']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {

    "sc": {'pattern': "//div[@class='qzsz_nav']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},

    # "issue_time": {'pattern': "//td[@bgcolor='#E6E6E6']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'广西壮族自治区-钦州市'
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
    if re.search(u'招标|谈判|竞争|询价|采购|延期', item['title']):
        item['bid_type'] = 1
    elif re.search(u'结果|中标|流标', item['title']):
        item['bid_type'] = 0
    elif re.search(u'更正|更改', item['title']):
        item['bid_type'] = 2
    elif re.search(u'澄清', item['title']):
        item['bid_type'] = 4
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "[%Y-%m-%d]")))
def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    # print item
    if len(item['sc']) > 100:
        item['is_get'] = 1
    else:
        item['is_get'] = 0



