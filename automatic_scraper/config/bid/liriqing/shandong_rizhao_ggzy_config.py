# coding: utf-8
import time
import logging
import re
logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"日照公共资源交易网"
data_source = 'http://www.rzggzyjy.gov.cn'

start_urls = [
    ##政府
    #招标
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002001/071002001001/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002001/071002001002/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002001/071002001003/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002001/071002001004/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002002/071002002001/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002002/071002002002/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002002/071002002003/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002002/071002002004/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002002/071002002005/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002002/071002002006/"
    #更正
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002003/071002003001/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002003/071002003002/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002003/071002003003/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002003/071002003004/",
    #中标
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002004/071002004001/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002004/071002004002/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002004/071002004003/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002004/071002004004/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002004/071002004005/",
    "http://www.rzggzyjy.gov.cn/rzwz/jyxx/071002/071002004/071002004006/"

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
    "_list": {'pattern': "//div[@class='list-con-news']/ul/li", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//a[text() = '下页 >' and @onclick]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//div[@class='news-txt l']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "issue_time": {'pattern': "//div[@class='news-date r']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='detail-content']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},

}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region']=u'山东-日照市'
    item['_delay_between_pages'] = 3


def process_list_item(list_element, item):
    """处理列表页元素

    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """

    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "%Y.%m.%d")))
    if '071002001'in item['_current_start_url'] or '071002002'in item['_current_start_url'] :
        item['bid_type']= 1
    elif '071002003'in item['_current_start_url']:
        item['bid_type']= 2
    elif '071002004'in item['_current_start_url']:
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

