# coding: utf-8
import time
import logging
import re
logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"滨州市建设工程招投标信息网"
data_source = 'http://www.bzpm.cn'

start_urls = [
    ##政府

    #招标
    "http://www.bzpm.cn/ZTBBZ/ZtbGGListMoreBZ.aspx?areaCode=12&appid=&zbflag=-1&classId=5021",
    #预中标
    "http://www.bzpm.cn/ZTBBZ/ZtbGSListMoreBZ.aspx?areaCode=12&appid=&zbflag=0&classId=5070",
    #中标
    "http://www.bzpm.cn/ZTBBZ/ZtbZBTZSListMoreBZ.aspx?areaCode=12&appid=&zbflag=0&classId=5080",


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
    "_list": {'pattern': "//table[@id='ctl00_MainContent_ListGG_ctl00']/tbody/tr", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//input[@class='rgPageNext' and @onclick='javascript:__doPostBack('ctl00$MainContent$ListGG$ctl00$ctl03$ctl01$ctl28','')']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//a[@target='_blank']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "issue_time": {'pattern': "//tr[@style='height:40px;']/td[6]", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='detail']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},

}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region']=u'山东-滨州市'
    #item['_delay_between_pages'] = 3


def process_list_item(list_element, item):
    """处理列表页元素

    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """

    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "%Y-%m-%d")))
    if '5021'in item['_current_start_url'] :
        item['bid_type']= 1
    elif '5080'in item['_current_start_url']:
        item['bid_type']= 4
    elif '5070'in item['_current_start_url']:
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

