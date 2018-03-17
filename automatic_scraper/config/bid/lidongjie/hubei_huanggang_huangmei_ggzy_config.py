# coding: utf-8
import time
import logging
import re
logger = logging.getLogger(__name__)

author = "lidongjie"
web_title = u"黄梅县公共资源交易中心"
data_source = 'http://www.hmxggzyjy.com'

start_urls = [
    "http://www.hmxggzyjy.com/News/JyxxList.aspx?ntype=11", #1
    "http://www.hmxggzyjy.com/News/JyxxList.aspx?ntype=12", #2
    "http://www.hmxggzyjy.com/News/JyxxList.aspx?ntype=13",#0
    "http://www.hmxggzyjy.com/News/JyxxList.aspx?ntype=21",#1
    "http://www.hmxggzyjy.com/News/JyxxList.aspx?ntype=22", #2
    "http://www.hmxggzyjy.com/News/JyxxList.aspx?ntype=23", #0

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
    "_list": {'pattern': "//div[@class='newslist_info']//ul//li",'type':'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"下一页", 'type': 'partial_link_text', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    #"issue_time": {'pattern': "//small", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''}
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//td[@id='content']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "issue_time": {'pattern': "//p[@class='p1']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'湖北—黄冈—黄梅'
    del item['web_title']
    item['_delay_between_pages'] = 1.5

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


    if'11'in item['_current_start_url']or'21' in item['_current_start_url']:
        item['bid_type'] = 1
    elif '12' in item['_current_start_url']or'22' in item['_current_start_url']:
            item['bid_type'] = 2
    elif '13' in item['_current_start_url'] or '23' in item['_current_start_url']:
        item['bid_type'] = 0
    else:
        item['bid_type'] = '-1'
    if re.search(u'(废标)|(流标)|(失败)|(终止)', item['title']):
        item['is_liubiao'] = 1
    else:
        item['is_liubiao'] = 0
    logger.debug('%s   %s', item['title'], item['issue_time'])
    time_data = re.search(r'(\d+)-(\d+)-(\d+)', item['issue_time'].strip(), re.S).group()
    item['issue_time'] = int(time.mktime(time.strptime(time_data, "%Y-%m-%d")))
    if len(item['sc']) != 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0
