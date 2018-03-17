# coding: utf-8
import logging
import time
import re
logger = logging.getLogger(__name__)

author = "lidongjie"
web_title = u"潜江市公共资源交易网"
data_source = 'http://www.qjggzy.cn'

start_urls = [
    #招标公告
    "http://www.qjggzy.cn/qjztb/gy_news_list.do?newCatid=10",
    "http://www.qjggzy.cn/qjztb/gy_news_list.do?newCatid=7",
    #变更公告
    "http://www.qjggzy.cn/qjztb/gy_news_list.do?newCatid=11",
    "http://www.qjggzy.cn/qjztb/gy_news_list.do?newCatid=8",

    #中标成交公告
     "http://www.qjggzy.cn/qjztb/gy_news_list.do?newCatid=12",
     "http://www.qjggzy.cn/qjztb/gy_news_list.do?newCatid=9",

    #中标公告
    "http://www.qjggzy.cn/qjztb/gy_news_list.do?newCatid=24",
    "http://www.qjggzy.cn/qjztb/gy_news_list.do?newCatid=23",


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
    "_list": {'pattern': "//div[@id='noHasChildContent']/div", 'type': 'xpath', 'target': 'html','custom_func_name': ''},
    "_next_page": {'pattern': u"//li[text()='下一页' and @class='pgNext']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@id='content']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    "title": {'pattern': "//div[@class='news_tit']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "issue_time": {'pattern': "//div[@class='news_time']/span", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region'] = u'湖北—潜江'
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
    # if 'newId=12821' in item['url']:
    #     print 111111
        # item['title'] = ''
        # del item['url']
    if item['url']=='http://www.qjggzy.cn/qjztb/gy_news_info.do?newId=15668':
        del item['url']
    elif item['url']=='http://www.qjggzy.cn/qjztb/gy_news_info.do?newId=14965':
        del item['url']
def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    if not item.get('url'):
        return

    if '10'in item ['_current_start_url'] or '7'in item['_current_start_url']:
        item['bid_type'] = 1
    elif '11'in item ['_current_start_url'] or '8'in item['_current_start_url']:
        item['bid_type'] = 2
    elif '24'in item ['_current_start_url'] or '723'in item['_current_start_url']:
        item['bid_type'] = 0
    elif '12'in item ['_current_start_url'] or '9'in item['_current_start_url']:
        item['bid_type'] = 4
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