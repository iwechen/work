# coding: utf-8
import time
import logging
import re
from  bs4 import BeautifulSoup
import re
logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"测绘信息网"
data_source = 'http://www.othermap.com'

start_urls = [

     #政府采购
    "http://www.othermap.com/art_list.asp?cat_id=4",
    "http://www.othermap.com/art_list.asp?cat_id=6",
    "http://www.othermap.com/art_list.asp?cat_id=8",
    "http://www.othermap.com/art_list.asp?cat_id=31",
    "http://www.othermap.com/art_list.asp?cat_id=36",

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
    "_list": {'pattern': "//table[@border='1']//tr[position()>2 and position()<last()]/td[2]/a[2]",'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[contains(text(),'下一页') and @href]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@id='ArtBody']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "/html//font[@style='font-size:16px']/b", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "_issue_time": {'pattern': "/html//table[@class='table-top']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region'] = u'测绘'
    item['_delay_between_pages'] = 3


def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """


    item['bid_type'] = 1


        # 停止翻页
    # if item['_current_page'] == 192:
    #     item['_click_next'] = False


def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    if re.search(ur'流标|终止|废标', item['title']):
        item['is_liubiao'] = 1
    logger.debug(item['_issue_time'])
    time_data=re.search(r'(\d+)-(\d+)-(\d+)',item['_issue_time'],re.S).group()
    item['issue_time'] = int(time.mktime(time.strptime(time_data.strip(), u"%Y-%m-%d")))
    if len(item['sc']) > 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0

