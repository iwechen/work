# coding: utf-8
import time
import logging
import re
from  bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"衡水高新技术产业开发区行政审批局"
data_source = 'http://spj.hsgyxq.gov.cn'

start_urls = [

    # 政府采购
    "http://spj.hsgyxq.gov.cn/index.do?cid=95&templet=ejggzymy",
    "http://spj.hsgyxq.gov.cn/index.do?cid=97&templet=ejggzymy",
    "http://spj.hsgyxq.gov.cn/index.do?cid=192&templet=ejggzymy",
    #更正
    "http://spj.hsgyxq.gov.cn/index.do?cid=211&templet=ejggzymy",
    #预中标
    "http://spj.hsgyxq.gov.cn/index.do?cid=212&templet=ejggzymy",
    #中标
    "http://spj.hsgyxq.gov.cn/index.do?cid=96&templet=ejggzymy",
    "http://spj.hsgyxq.gov.cn/index.do?cid=98&templet=ejggzymy",
    "http://spj.hsgyxq.gov.cn/index.do?cid=193&templet=ejggzymy",

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
    "_list": {'pattern': "//table[@width='100%'][1]//tr", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[contains(text(),'后页') and @href]", 'type': 'xpath', 'target': 'html',  'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "_issue_time": {'pattern': "//td[@class='l_gslist']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='nr_con']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region'] = u'河北省-衡水市'
    item['_delay_between_pages'] = 3


def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """

    item['issue_time'] = int(time.mktime(time.strptime(item['_issue_time'].strip(), u"%Y-%m-%d")))
    if '95'in item['_current_start_url'] or '97'in item['_current_start_url'] or '192'in item['_current_start_url']:
        item['bid_type']= 1
    elif '96'in item['_current_start_url'] or '98'in item['_current_start_url'] or '193'in item['_current_start_url']:
        item['bid_type']= 0
    elif '211' in item['_current_start_url']:
        item['bid_type'] = 2
    elif '212' in item['_current_start_url']:
        item['bid_type'] = 4
    if re.search(ur'流标|失败|废标', item['title']):
        item['is_liubiao'] = 1





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

