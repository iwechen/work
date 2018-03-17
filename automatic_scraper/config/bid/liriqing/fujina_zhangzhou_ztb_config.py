# coding: utf-8
import time
import logging
import re
logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"漳州城乡和住房建设网"
data_source = 'http://www.zzjs.gov.cn'

start_urls = [
    #招标公告
    "http://www.zzjs.gov.cn/Industry/Industry1.asp?lmid=11",
    #中标
    "http://www.zzjs.gov.cn/Industry/Industry1.asp?lmid=10",
    #答疑
    "http://www.zzjs.gov.cn/Industry/Industry1.asp?lmid=129"
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
    "_list": {'pattern': "//div[@id='pub_tip']/ul/li", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[contains(text(),'>>') and @href]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_issue_time": {'pattern': "//font", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@id='text_main']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region']=u'福建省-漳州市'
    item['_delay_between_pages'] = 3


def process_list_item(list_element, item):
    """处理列表页元素

    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    time_data=re.search(ur'(\d+)年(\d+)月(\d+)日',item['_issue_time'],re.S).group()
    item['issue_time'] = int(time.mktime(time.strptime(time_data.strip(), u"%Y年%m月%d日")))
    if '11' in item['_current_start_url']:
        item['bid_type'] = 1
    elif '10' in item['_current_start_url']:
        item['bid_type'] = 0
    elif '129' in item['_current_start_url']:
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

