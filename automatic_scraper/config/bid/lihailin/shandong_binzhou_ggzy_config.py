# coding: utf-8
import time
import logging
import re
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

author = "lihailin"
web_title = u"北海开发区公共资源交易中心"
data_source = 'http://www.bzbhggzyjy.gov.cn'

start_urls = [
    #建设工程
    "http://www.bzbhggzyjy.gov.cn/bhweb/002/002004/002004001/002004001009/MoreInfo.aspx?CategoryNum=002004001009",#招标
    "http://www.bzbhggzyjy.gov.cn/bhweb/002/002004/002004003/002004003009/MoreInfo.aspx?CategoryNum=002004003009",#变更
    "http://www.bzbhggzyjy.gov.cn/bhweb/002/002004/002004002/002004002009/MoreInfo.aspx?CategoryNum=002004002009",#中标
    #政府采购
    "http://www.bzbhggzyjy.gov.cn/bhweb/002/002005/002005001/002005001001/002005001001009/MoreInfo.aspx?CategoryNum=002005001001009",#招标
    "http://www.bzbhggzyjy.gov.cn/bhweb/002/002005/002005003/002005003009/MoreInfo.aspx?CategoryNum=002005003009",#中标
    "http://www.bzbhggzyjy.gov.cn/bhweb/002/002005/002005007/002005007009/MoreInfo.aspx?CategoryNum=002005007009"#废标
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
    "_list": {'pattern': "//tr[@class='tdstyle']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[@href and text()='下一页']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "issue_time": {'pattern': "//td[@style='border-style:None;width:80px;']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

}

# 详情页模板
detail_pattern = {

    "sc": {'pattern': "//td[@class='infodetail']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'山东省-滨州市'
    del item['web_title']
    item['_delay_between_pages'] = 3

def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    if '002004001009' in item['_current_start_url'] or '002005001001009' in item['_current_start_url']:
        item['bid_type'] = 1
    elif '002004002009' in item['_current_start_url'] or '002005003009' in item['_current_start_url']:
        item['bid_type'] = 0
    elif '002004003009' in item['_current_start_url']:
        item['bid_type'] = 2
    if '002005007009' in item['_current_start_url']:
        item['is_liubiao'] = 1
    else:
        item['is_liubiao'] = 0
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'],"%Y-%m-%d")))
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



