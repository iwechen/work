# coding: utf-8
import logging
import time
import re
logger = logging.getLogger(__name__)

author = "lidongjie"
web_title = u"抚州公共资源交易网"
data_source = 'http://www.fzztb.gov.cn'

start_urls = [
    # #zbgg
    # "http://www.fzztb.gov.cn/jsgc/zbgg/",
    # "http://www.fzztb.gov.cn/zfcg/zbgg/gkzb/",
    # "http://www.fzztb.gov.cn/zfcg/zbgg/jzxtp/",
    # "http://www.fzztb.gov.cn/zfcg/zbgg/yqzb/",
    # "http://www.fzztb.gov.cn/zfcg/zbgg/dyxly/",
    # "http://www.fzztb.gov.cn/zfcg/zbgg/jzxcs/",

    #zbgs
    "http://www.fzztb.gov.cn/jsgc/zbgs/gkzb/index_14.htm",
    # "http://www.fzztb.gov.cn/jsgc/zbgs/yqzb/",
    # "http://www.fzztb.gov.cn/zfcg/zbgs/",
 ]

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'bid_data',
    'table': 'zhaotoubiao_copy'
}

# 列表页模板
index_pattern = {
    "_list": {'pattern': "//table[@class='bg']", 'type': 'xpath', 'target': 'html','custom_func_name': ''},
    "_next_page": {'pattern': u"下一页", 'type': 'partial_link_text', 'target': 'html', 'custom_func_name': ''},
    "_issue_time": {'pattern': "//td[2]", 'type': 'xpath', 'target': 'text','custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//td[@id='Zoom2']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},


    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region'] = u'江西-抚顺'
    item['_delay_between_pages'] = 3

def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    logger.debug(item['url'])
    # 停止翻页
    if item['url']=='http://www.fzztb.gov.cn/jsgc/zbgs/gkzb/201109/P020110920389308675689.rar':
        del item['url']


def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    if 'zbgg'in item['_current_start_url']:
        item['bid_type'] = 1
    elif 'zbgs'in item['_current_start_url']:
        item['bid_type'] = 0
    logger.debug('%s   %s', item['title'], item['_issue_time'])
    item['issue_time'] = int(time.mktime(time.strptime(item['_issue_time'], '%Y-%m-%d')))

    if len(item['sc']) != 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0