# coding: utf-8
import logging
import time
import re
logger = logging.getLogger(__name__)

author = "lidongjie"
web_title = u"渭南政府采购网"
data_source = 'http://www.wnggzy.com'

start_urls = [
    #招标公告
    "http://www.wnggzy.com/wnggzyweb/jyxx/002001/002001006/002001006001/",
    "http://www.wnggzy.com/wnggzyweb/jyxx/002001/002001007/002001007001/",
    "http://www.wnggzy.com/wnggzyweb/jyxx/002001/002001008/002001008001/",
    "http://www.wnggzy.com/wnggzyweb/jyxx/002001/002001009/002001009001/",



    #变更公告
    "http://www.wnggzy.com/wnggzyweb/jyxx/002001/002001006/002001006002/",
    "http://www.wnggzy.com/wnggzyweb/jyxx/002001/002001007/002001007002/",
    "http://www.wnggzy.com/wnggzyweb/jyxx/002001/002001008/002001008002/",

    #中标公示
    "http://www.wnggzy.com/wnggzyweb/jyxx/002001/002001006/002001006003/",
    "http://www.wnggzy.com/wnggzyweb/jyxx/002001/002001007/002001007003/",
    "http://www.wnggzy.com/wnggzyweb/jyxx/002001/002001008/002001008003/",
    "http://www.wnggzy.com/wnggzyweb/jyxx/002001/002001009/002001009003/",
    "http://www.wnggzy.com/wnggzyweb/jyxx/002002/002002003/",
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
    "_list": {'pattern': "//table[@class='moreinfocon']//tr", 'type': 'xpath', 'target': 'html','custom_func_name': ''},
    "_next_page": {'pattern': u"//td[text()='下页 >'and @onclick]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_issue_time": {'pattern': "//span", 'type': 'xpath', 'target': 'text','custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text','custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='row']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    #"title": {'pattern': "//td[@height='76']", 'type': 'xpath', 'target': 'text','custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region'] = u'陕西-渭南'
    item['_delay_between_pages'] = 3

def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """

    if item['url']=='http://www.wnggzy.com/wnggzyweb/infodetail/?infoid=85c142ef-a412-42a8-87d2-5c2484915126&categoryNum=002001006003':
        del item['url']
    elif item['url']=='http://www.wnggzy.com/wnggzyweb/%e7%bb%b4%e6%8a%a4%e4%b8%ad.htm?aspxerrorpath=/wnggzyweb/infodetail/default.aspx':
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
    if '002001006001' in item['_current_start_url'] or '002001007001' in item[
        '_current_start_url'] or '002001008001' in item['_current_start_url']or '002001009001' in item[
        '_current_start_url'] or '002002001' in item['_current_start_url']:
        item['bid_type'] = 1
    elif '002001006003' in item['_current_start_url'] or '002001007003' in item[
        '_current_start_url'] or '002001008003' in item['_current_start_url'] or '002001009003' in item[
        '_current_start_url'] or '002002001' in item['_current_start_url']:
        item['bid_type'] = 0
    elif '002001006002' in item['_current_start_url'] or '002001007002' in item['_current_start_url'] or '002001008002' in item['_current_start_url']:
        item['bid_type'] = 2
    else:
        item['bid_type'] = '-1'


    logger.debug('%s   %s', item['title'], item['_issue_time'])
    item['issue_time'] = int(time.mktime(time.strptime(item['_issue_time'], '%Y-%m-%d')))
    if len(item['sc']) != 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0