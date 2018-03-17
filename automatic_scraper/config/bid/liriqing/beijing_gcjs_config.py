# coding: utf-8
import time
import logging
import re
from  bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"北京工程建设交易信息网"
data_source = 'http://www.bcactc.com'

start_urls = [

     #政府采购
    "http://www.bcactc.com/home/gcxx/now_kcsjzbgg.aspx",
    "http://www.bcactc.com/home/gcxx/now_sgzbgg.aspx",
    "http://www.bcactc.com/home/gcxx/now_jlzbgg.aspx",
    "http://www.bcactc.com/home/gcxx/now_zyzbgg.aspx",
    "http://www.bcactc.com/home/gcxx/now_clsbzbgg.aspx",
    "http://www.bcactc.com/home/gcxx/now_tdzbgg.aspx",
    "http://www.bcactc.com/home/gcxx/now_ylzbgg.aspx",
    "http://www.bcactc.com/home/gcxx/now_mhzbgg.aspx",
    "http://www.bcactc.com/home/gcxx/now_jdzbgg.aspx",
    #中标
    "http://www.bcactc.com/home/gcxx/now_kcsjzbgs.aspx",
    "http://www.bcactc.com/home/gcxx/now_sgzbgs.aspx",
    "http://www.bcactc.com/home/gcxx/now_jlzbgs.aspx",
    "http://www.bcactc.com/home/gcxx/now_zyzbgs.aspx",
    "http://www.bcactc.com/home/gcxx/now_clsbzbgs.aspx",
    "http://www.bcactc.com/home/gcxx/now_lwzbgs.aspx",
    "http://www.bcactc.com/home/gcxx/now_tdzbgs.aspx",
    "http://www.bcactc.com/home/gcxx/now_ylzbgs.aspx",
    "http://www.bcactc.com/home/gcxx/now_mhzbgs.aspx",
    "http://www.bcactc.com/home/gcxx/now_jdzbgs.aspx",





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
    "_list": {'pattern': "//table[@id='DataGrid1']//tr",'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//input[@src='../images/table_buttom_next.gif']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "_issue_time": {'pattern': "//td[@style='width:21%;']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "_page_data": {'pattern': "/html//span[@id='lblPageCount']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//td[@class='context']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},


    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region']=u'北京市'
    item['_delay_between_pages'] = 5


def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    if 'gg' in item['_current_start_url']:
        item['issue_time'] = int(time.mktime(time.strptime(item['_issue_time'].strip(), u"%Y-%m-%d %H:%M")))
    else:
        item['issue_time'] = int(time.mktime(time.strptime(item['_issue_time'].strip(), u"%Y-%m-%d")))
    if 'gg' in item['_current_start_url']:
        item['bid_type'] = 1

    elif 'gs' in item['_current_start_url']:
        item['bid_type'] = 0


        #停止翻页
    if item['_current_page'] == int(item['_page_data']):
        item['_click_next'] = False


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

