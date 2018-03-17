# coding: utf-8
import time
import logging
import re

logger = logging.getLogger(__name__)

author = "lidongjie"
web_title = u"临沂市公共资源交易网"
data_source = 'http://ggzyjy.linyi.gov.cn'

start_urls = [
    #招标公告
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001001/074001001001/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001001/074001001003/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001001/074001001004/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001001/074001001005/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002002/074002002001/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002002/074002002002/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002002/074002002004/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002002/074002002005/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002002/074002002007/",
    #中标公示
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001003/074001003003/074001003003001/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001003/074001003003/074001003003004/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001003/074001003003/074001003003005/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002004/074002004001/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002004/074002004002/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002004/074002004004/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002004/074002004005/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002004/074002004007/",
    #变更公告
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001002/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002003/",
    #中标候选人
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001003/074001003002/074001003002004/",
    "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001003/074001003002/074001003002005/",

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
    "_list": {'pattern': "//ul[@class='ewb-news-items ewb-build-items']//li",'type':'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[text()='下页 >'and @onclick]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_issue_time":{'pattern': "//span", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''}
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@id='mainContent']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//h1", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},


    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'山东—临沂'
    del item['web_title']
    item['_delay_between_pages'] = 2

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
    if '074001001' in item['_current_start_url'] or'074002002' in item['_current_start_url'] :
        item['bid_type'] = 1
    elif'074001002' in item['_current_start_url'] or'074002003' in item['_current_start_url'] :
        item['bid_type'] = 2
    elif '074001003003' in item['_current_start_url'] or'074002004' in item['_current_start_url'] :
        item['bid_type'] = 0
    elif '074001003002' in item['_current_start_url']:
        item['bid_type'] = 4
    else:
        item['bid_type'] = '-1'
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