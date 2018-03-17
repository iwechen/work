# coding: utf-8
import time
import logging
from bs4 import BeautifulSoup
import hashlib
import re

logger = logging.getLogger(__name__)

author = "huangtaiwu"
web_title = u"宣城市公共资源交易服务网"
data_source = 'http://www.xcsztb.com'

start_urls = [
    "http://www.xcsztb.com/XCTPFront/zfcg/012001/012001001/",#1
    "http://www.xcsztb.com/XCTPFront/zfcg/012002/012002001/",#1
    "http://www.xcsztb.com/XCTPFront/zfcg/012003/012003001/",#1
    "http://www.xcsztb.com/XCTPFront/zfcg/012004/012004001/",#1
    "http://www.xcsztb.com/XCTPFront/zfcg/012005/012005001/",#1
    "http://www.xcsztb.com/XCTPFront/zfcg/012006/012006001/",#1
    "http://www.xcsztb.com/XCTPFront/zfcg/012007/012007001/",#1
    "http://www.xcsztb.com/XCTPFront/zfcg/012008/012008001/",#1
    "http://www.xcsztb.com/XCTPFront/zfcg/012001/012001003/",#2
    "http://www.xcsztb.com/XCTPFront/zfcg/012002/012002003/",#2
    "http://www.xcsztb.com/XCTPFront/zfcg/012003/012003003/",#2
    "http://www.xcsztb.com/XCTPFront/zfcg/012004/012004003/",#2
    "http://www.xcsztb.com/XCTPFront/zfcg/012005/012005003/",#2
    "http://www.xcsztb.com/XCTPFront/zfcg/012006/012006003/",#2
    "http://www.xcsztb.com/XCTPFront/zfcg/012007/012007003/",#2
    "http://www.xcsztb.com/XCTPFront/zfcg/012008/012008003/",#2
    "http://www.xcsztb.com/XCTPFront/zfcg/012001/012001004/",#0
    "http://www.xcsztb.com/XCTPFront/zfcg/012002/012002004/",#0
    "http://www.xcsztb.com/XCTPFront/zfcg/012003/012003004/",#0
    "http://www.xcsztb.com/XCTPFront/zfcg/012004/012004004/",#0
    "http://www.xcsztb.com/XCTPFront/zfcg/012005/012005004/",#0
    "http://www.xcsztb.com/XCTPFront/zfcg/012006/012006004/",#0
    "http://www.xcsztb.com/XCTPFront/zfcg/012007/012007004/",#0
    "http://www.xcsztb.com/XCTPFront/zfcg/012008/012008004/",#0
    "http://www.xcsztb.com/XCTPFront/jsgc/011001/011001001/",#1
    "http://www.xcsztb.com/XCTPFront/jsgc/011002/011002001/",#1
    "http://www.xcsztb.com/XCTPFront/jsgc/011003/011003001/",#1
    "http://www.xcsztb.com/XCTPFront/jsgc/011004/011004001/",#1
    "http://www.xcsztb.com/XCTPFront/jsgc/011005/011005001/",#1
    "http://www.xcsztb.com/XCTPFront/jsgc/011006/011006001/",#1
    "http://www.xcsztb.com/XCTPFront/jsgc/011007/011007001/",#1
    "http://www.xcsztb.com/XCTPFront/jsgc/011008/011008001/",#1
    "http://www.xcsztb.com/XCTPFront/jsgc/011001/011001002/",#2
    "http://www.xcsztb.com/XCTPFront/jsgc/011002/011002002/",  # 2
    "http://www.xcsztb.com/XCTPFront/jsgc/011003/011003002/",  # 2
    "http://www.xcsztb.com/XCTPFront/jsgc/011004/011004002/",  # 2
    "http://www.xcsztb.com/XCTPFront/jsgc/011005/011005002/",  # 2
    "http://www.xcsztb.com/XCTPFront/jsgc/011006/011006002/",  # 2
    "http://www.xcsztb.com/XCTPFront/jsgc/011007/011007002/",  # 2
    "http://www.xcsztb.com/XCTPFront/jsgc/011008/011008002/",  # 2
    "http://www.xcsztb.com/XCTPFront/jsgc/011001/011001003/",#4
    "http://www.xcsztb.com/XCTPFront/jsgc/011002/011002003/",  # 4
    "http://www.xcsztb.com/XCTPFront/jsgc/011003/011003003/",  # 4
    "http://www.xcsztb.com/XCTPFront/jsgc/011004/011004003/",  # 4
    "http://www.xcsztb.com/XCTPFront/jsgc/011005/011005003/",  # 4
    "http://www.xcsztb.com/XCTPFront/jsgc/011006/011006003/",  # 4
    "http://www.xcsztb.com/XCTPFront/jsgc/011007/011007003/",  # 4
    "http://www.xcsztb.com/XCTPFront/jsgc/011008/011008003/",  # 4
    "http://www.xcsztb.com/XCTPFront/jsgc/011001/011001004/",#0
    "http://www.xcsztb.com/XCTPFront/jsgc/011002/011002004/",  # 0
    "http://www.xcsztb.com/XCTPFront/jsgc/011003/011003004/",  # 0
    "http://www.xcsztb.com/XCTPFront/jsgc/011004/011004004/",  # 0
    "http://www.xcsztb.com/XCTPFront/jsgc/011005/011005004/",  # 0
    "http://www.xcsztb.com/XCTPFront/jsgc/011006/011006004/",  # 0
    "http://www.xcsztb.com/XCTPFront/jsgc/011007/011007004/",  # 0
    "http://www.xcsztb.com/XCTPFront/jsgc/011008/011008004/",  # 0


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
    "_list": {'pattern': "//tr[@height='28']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//td[text()='下页 >' and @onclick]", 'type': 'xpath', 'target': 'html',
                   'custom_func_name': ''},
    "issue_time": {'pattern': "//td[@align='right']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='article-content']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "title": {'pattern': "//div[@align='center']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'安徽省-宣城市'
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
    if re.search('01200\d001|01100\d001',item['_current_start_url']):
        item['bid_type'] = 1
    elif re.search('01200\d004|01100\d004',item['_current_start_url']):
        item['bid_type'] = 0
    elif re.search('01200\d003|01100\d002',item['_current_start_url']):
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


