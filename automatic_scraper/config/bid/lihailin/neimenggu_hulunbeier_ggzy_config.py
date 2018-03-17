# coding: utf-8
import time
import logging
import re
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

author = "lihailin"
web_title = u"呼伦贝尔市公共资源交易中心"
data_source = 'http://www.hlbeggzyjy.org.cn'

start_urls = [
    #招标
    "http://www.hlbeggzyjy.org.cn/gcjs/subpage-jyxx.html",
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
    "_list": {'pattern': "//ul[@id='showList']//li", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[@class='next' and text()='下页 >']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "issue_time": {'pattern': "//span", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

}

# 详情页模板
detail_pattern = {

    "sc": {'pattern': "//div[@class='news-article-para']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'内蒙古自治区-呼伦贝尔市'
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
    data = requests.get(item['url'])
    if u'404 Not Found' in data.text:
        del item['url']
        return
    if(item['url'])=="http://www.hlbeggzyjy.org.cn/gcjs/subpage-jyxx.html":
        del item['url']
    if re.search(u'中标|竞争性谈判公示|结果|候选人', item['title']):
        item['bid_type'] = '0'
    elif re.search(u'招标|竞争性谈判公告|延期', item['title']):
        item['bid_type'] = '1'
    elif re.search(u'变更|情况|补遗', item['title']):
        item['bid_type'] = '2'
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'],"[%Y-%m-%d]")))
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



