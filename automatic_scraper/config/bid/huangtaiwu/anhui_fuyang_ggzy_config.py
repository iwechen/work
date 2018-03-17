# coding: utf-8
import time
import logging
from bs4 import BeautifulSoup
import hashlib
import re

logger = logging.getLogger(__name__)

author = "huangtaiwu"
web_title = u"阜阳市公共资源交易网"
data_source = 'http://jyzx.fy.gov.cn'

start_urls = [
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011001/011001001/",#1
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011001/011001002/",#1
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011001/011001003/",#1
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011001/011001004/",#1
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011001/011001005/",#1
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011001/011001006/",#1
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011002/011002001/",#0
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011002/011002002/",#0
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011002/011002003/",#0
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011002/011002004/",#0
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011002/011002005/",#0
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011002/011002006/",#0
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011004/011004001/",#2
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011004/011004002/",#2
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011004/011004003/",#2
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011004/011004004/",#2
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011004/011004005/",#2
    "http://jyzx.fy.gov.cn/FuYang/zfcg/011004/011004006/",#2
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012001/012001001/",#1
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012001/012001002/",#1
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012001/012001003/",#1
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012001/012001004/",#1
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012001/012001005/",#1
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012001/012001006/",#1
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012002/012002001/",#0
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012002/012002002/",  # 0
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012002/012002003/",  # 0
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012002/012002004/",  # 0
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012002/012002005/",  # 0
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012002/012002006/",  # 0
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012003/012003001/",  # 2
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012003/012003002/",  # 2
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012003/012003003/",  # 2
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012003/012003004/",  # 2
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012003/012003005/",  # 2
    "http://jyzx.fy.gov.cn/FuYang/jsgc/012003/012003006/",  # 2

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
    "_list": {'pattern': "//ul[@class='wb-data-item']//li", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[text()='下页 >' and @onclick]", 'type': 'xpath', 'target': 'html',
                   'custom_func_name': ''},
    "issue_time": {'pattern': "//span[@class='wb-data-date']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='article-block']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "title": {'pattern': "//div[@align='center']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'安徽省-阜阳市'
    del item['web_title']
    item['_delay_between_pages'] = 1.5


def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    # 停止翻页
    if re.search('011001|012001',item['_current_start_url']):
        item['bid_type'] = 1
    elif re.search('011004|012003',item['_current_start_url']):
        item['bid_type'] = 2
    elif re.search('011002|012002',item['_current_start_url']):
        item['bid_type'] = 0
    else:
        item['bid_type'] = -1
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


