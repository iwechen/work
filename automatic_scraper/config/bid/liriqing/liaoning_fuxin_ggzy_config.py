# coding: utf-8
import time
import logging
import re
logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"阜新公共资源交易网"
data_source = 'http://www.fxggzy.com'

start_urls = [
    #招标公告
    "http://www.fxggzy.com/fx_front/jyxx/069001/069001001/MoreInfo.aspx?CategoryNum=069001001",
    "http://www.fxggzy.com/fx_front/jyxx/069002/069002001/MoreInfo.aspx?CategoryNum=069002001",
    #中标候选人
    "http://www.fxggzy.com/fx_front/jyxx/069001/069001002/MoreInfo.aspx?CategoryNum=069001002",
    #变更公告
    "http://www.fxggzy.com/fx_front/jyxx/069002/069002002/MoreInfo.aspx?CategoryNum=069002002",
    #中标
    "http://www.fxggzy.com/fx_front/jyxx/069001/069001003/MoreInfo.aspx?CategoryNum=069001003",
    "http://www.fxggzy.com/fx_front/jyxx/069002/069002003/MoreInfo.aspx?CategoryNum=069002003",

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
    "_list": {'pattern': "//tr[@style='height:22px;']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//a/img[@src='/fx_front/images/page/nextn.gif']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "issue_time": {'pattern': "//td[@style='border-style:None;width:80px;']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//table[@class='tab topd']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region']=u'辽宁-阜新市'
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
    if '069001001' in item['_current_start_url'] or '069002001' in item['_current_start_url']:
        item['bid_type'] = 1
    elif '069001002' in item['_current_start_url']:
        item['bid_type']= 4
    elif '069002002' in item['_current_start_url']:
        item['bid_type'] = 2
    elif '069001003' in item['_current_start_url'] or '069002003' in item['_current_start_url']:
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

