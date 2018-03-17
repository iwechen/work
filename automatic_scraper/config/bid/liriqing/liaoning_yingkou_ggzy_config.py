# coding: utf-8
import time
import logging
import re
logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"营口市公共资源交易网"
data_source = 'http://www.ccgp-yingkou.gov.cn'

start_urls = [
    #招标公告
    "http://www.ccgp-yingkou.gov.cn/Html/NewsList.asp?SortID=155&SortPath=0,98,121,155,",
    "http://www.ccgp-yingkou.gov.cn/Html/NewsList.asp?SortID=152&SortPath=0,98,120,152,",
    #中标候选人
    "http://www.ccgp-yingkou.gov.cn/Html/NewsList.asp?SortID=153&SortPath=0,98,120,153,",
    #变更公告
    "http://www.ccgp-yingkou.gov.cn/Html/NewsList.asp?SortID=156&SortPath=0,98,121,156,",
    #中标
    "http://www.ccgp-yingkou.gov.cn/Html/NewsList.asp?SortID=154&SortPath=0,98,120,154,",
    "http://www.ccgp-yingkou.gov.cn/Html/NewsList.asp?SortID=157&SortPath=0,98,121,157,",

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
    "_list": {'pattern': "//table[@width='100%']//tr[position()<last()]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//td[@height='30' and @align='center']//font[@color='#ff6600'][last()]//following-sibling::a[1]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "issue_time": {'pattern': "//td[@width='79']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//td[@align='left']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region']=u'辽宁-营口市'
    item['_delay_between_pages'] = 3


def process_list_item(list_element, item):
    """处理列表页元素

    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    logger.debug(item['issue_time'])
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "%Y-%m-%d")))
    if '0,98,121,155,' in item['_current_start_url'] or '0,98,120,152' in item['_current_start_url']:
        item['bid_type'] = 1
    elif '153' in item['_current_start_url']:
        item['bid_type']= 4
    elif '156' in item['_current_start_url']:
        item['bid_type'] = 2
    elif '154' in item['_current_start_url'] or '157' in item['_current_start_url']:
        item['bid_type'] = 0
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

