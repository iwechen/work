# coding: utf-8
import time
import logging
import re
from  bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"安阳市政府采购"
data_source = 'http://www.anyang.gov.cn'

start_urls = [
    # 招标公告

     #政府采购
    #http://www.anyang.gov.cn/viewCmsCac.do?cacId=ff8080812b8b328f012b8e9b897f00ad&offset=25&
    "http://www.anyang.gov.cn/viewCmsCac.do?cacId=ff8080812fe8fa9f013007e751a021b6",
    #中标
    "http://www.anyang.gov.cn/viewCmsCac.do?cacId=ff8080812fe8fa9f013007e751ac21b7",
    #更正
    "http://www.anyang.gov.cn/viewCmsCac.do?cacId=5a9c10a5528179e8015286565c901255",


]

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'asd123',
    'database': 'bid_data',
    'table': 'zhaotoubiao'
}

# 列表页模板
index_pattern = {
    "_list": {'pattern': "//tr[@height='20']",'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//a[text()='下一页' and @href]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_issue_time": {'pattern': "//td[@width='120']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='newpg_son' or @style='FONT-SIZE: 20px']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},

    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region'] = u'河南省-安阳市'
    item['_delay_between_pages'] = 5


def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    # href="javascript:redirectpage("e797638b-c3b3-44ad-bf47-ed98ea9f1c7d","077002003")">


    item['issue_time'] = int(time.mktime(time.strptime(item['_issue_time'].strip(), u"[%Y-%m-%d]")))

    if 'ff8080812fe8fa9f013007e751a021b6' in item['_current_start_url'] :
        item['bid_type'] = 1

    elif 'ff8080812fe8fa9f013007e751ac21b7' in item['_current_start_url']:
        item['bid_type'] = 0
    elif '5a9c10a5528179e8015286565c901255' in item['_current_start_url']:
        item['bid_type'] = 2
        # 停止翻页
        # if item['_current_page'] == 10:
        #     item['_click_next'] = False


def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """

    if len(item['sc']) > 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0

