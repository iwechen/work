# coding: utf-8
import logging
import time
import re
logger = logging.getLogger(__name__)

author = "lidongjie"
web_title = u"株洲公共资源交易网"
data_source = 'http://www.zzzyjy.cn'

start_urls = [
    #中标公告
    "http://www.zzzyjy.cn/017/017003/secondPage.html",


    #招标公告
    "http://www.zzzyjy.cn/016/016001/016001001/secondPage2.html",
    "http://www.zzzyjy.cn/016/016002/016002001/secondPage2.html",
    "http://www.zzzyjy.cn/016/016003/016003001/secondPage2.html",
    "http://www.zzzyjy.cn/016/016004/016004001/secondPage2.html",
    "http://www.zzzyjy.cn/017/017001/secondPage.html",

    #变更公告
    "http://www.zzzyjy.cn/016/016002/016002002/secondPage2.html",
    "http://www.zzzyjy.cn/017/017002/secondPage.html",

    #中标候选人
    "http://www.zzzyjy.cn/016/016001/016001004/secondPage2.html",
    "http://www.zzzyjy.cn/016/016002/016002004/secondPage2.html",
    "http://www.zzzyjy.cn/016/016003/016003004/secondPage2.html",
    "http://www.zzzyjy.cn/016/016004/016004004/secondPage2.html",
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
    "_list": {'pattern': "//ul[@class='ewb-info-list']//li", 'type': 'xpath', 'target': 'html','custom_func_name': ''},
    "_next_page": {'pattern': u"下页>", 'type': 'partial_link_text', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='ewb-article']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    "issue_time": {'pattern': "//div[@class='ewb-source']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region'] = u'湖南—株洲'
    item['_delay_between_pages'] = 3

def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    if item['url']=='http://www.zzzyjy.cn/016/016001/016001001/20170620/815be9e2-042c-417d-aef0-7956f53e2548.html':
        del item['url']
        return
    logger.debug(item['url'])


    # 停止翻页




def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    if not item.get('url'):
        return

    if '016001001'in item['_current_start_url'] or'016002001'in item[
        '_current_start_url']or'016003001'in item['_current_start_url'] or'016004001'in item[
        '_current_start_url'] or'016002001'in item['_current_start_url']:
        item['bid_type'] = 1
    elif '017003'in item['_current_start_url']:
        item['bid_type'] = 0
    elif '017001'in item['_current_start_url']:
        item['bid_type'] = 2
    if '016001004' in item['_current_start_url'] or '016002004' in item['_current_start_url'] or '016003004' in item[
        '_current_start_url'] or '016004004' in item['_current_start_url']:
        item['bid_type'] = 4

    logger.debug('%s   %s', item['title'], item['issue_time'])
    time_data = re.search(r'(\d+)-(\d+)-(\d+)', item['issue_time'].strip(), re.S).group()
    item['issue_time'] = int(time.mktime(time.strptime(time_data, "%Y-%m-%d")))
    if len(item['sc']) != 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0