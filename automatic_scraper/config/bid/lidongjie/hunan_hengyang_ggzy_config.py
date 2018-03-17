# coding: utf-8
import logging
import time
import re
logger = logging.getLogger(__name__)

author = "lidongjie"
web_title = u"衡阳公共资源交易网"
data_source = 'http://hyggzyjy.hengyang.gov.cn'

start_urls = [
    #中标公告
    "http://hyggzyjy.hengyang.gov.cn/hyggzy/jyxx/004002/004002002/list.html",

    #招标公告
    "http://hyggzyjy.hengyang.gov.cn/hyggzy/jyxx/004001/004001001/list.html",
    "http://hyggzyjy.hengyang.gov.cn/hyggzy/jyxx/004002/004002001/list.html",


    #中标候选人
    "http://hyggzyjy.hengyang.gov.cn/hyggzy/jyxx/004001/004001003/list.html",

    "http://hyggzyjy.hengyang.gov.cn/hyggzy/jyxx/004002/004002003/list.html",
    "http://hyggzyjy.hengyang.gov.cn/hyggzy/jyxx/004001/004001004/list.html",
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
    "_list": {'pattern': "//ul[@class='ewb-info-items']//li", 'type': 'xpath', 'target': 'html','custom_func_name': ''},
    "_next_page": {'pattern': u"//a[text()='下一页' and@href]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_issue_time": {'pattern': "//span", 'type': 'xpath', 'target': 'text','custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@id='mainContent']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    "title": {'pattern': "//h3[@class='article-title']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region'] = u'湖南—衡阳'
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



def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    if '004001001'in item['_current_start_url'] or'004002001'in item['_current_start_url']:
        item['bid_type'] = 1
    elif '004002002'in item['_current_start_url']:
        item['bid_type'] = 0
    elif '004001003'in item['_current_start_url']:
        item['bid_type'] = 4
    if re.search(u'(废标)|(流标)|(失败)|(终止)', item['title']):
        item['is_liubiao'] = 1
    else:
        item['is_liubiao'] = 0
    logger.debug('%s   %s', item['title'], item['_issue_time'])
    item['issue_time'] = int(time.mktime(time.strptime(item['_issue_time'], '%Y-%m-%d')))

    if len(item['sc']) != 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0