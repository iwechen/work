# coding: utf-8
import time
import logging
import re
logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"锦州市公共资源交易网"
data_source = 'http://www.jztb.gov.cn'

start_urls = [
    #招标公告
    "http://www.jztb.gov.cn/jyxx/077001/077001001/listMore.html",
    "http://www.jztb.gov.cn/jyxx/077002/077002001/listMore.html",
    #中标候选人
    "http://www.jztb.gov.cn/jyxx/077002/077002002/listMore.html",
    #中标
    "http://www.jztb.gov.cn/jyxx/077001/077001002/listMore.html",
    "http://www.jztb.gov.cn/jyxx/077002/077002003/listMore.html",

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
    "_list": {'pattern': "//ul[@id='showList']/li", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//a[text()='下页  >']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_issue_time": {'pattern': "//span", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='ewb-info-bd']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region']=u'辽宁-锦州市'
    item['_delay_between_pages'] = 3


def process_list_item(list_element, item):
    """处理列表页元素

    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    #href="javascript:redirectpage("e797638b-c3b3-44ad-bf47-ed98ea9f1c7d","077002003")">
    url_data=re.search(r'redirectpage\((.*?)\)',list_element,re.S).group(1)
    id=re.search(r'\"(.*?)\"',url_data,re.S).group(1)
    url_type1=re.search(r',(.*)',url_data,re.S).group(1)
    url_type=url_type1[1:-4]
    #http://www.jztb.gov.cn/jyxx/077002/077002003/20170616/e797638b-c3b3-44ad-bf47-ed98ea9f1c7d.html
    url_date=item['_issue_time'][:4]+item['_issue_time'][5:7]+item['_issue_time'][8:]
    item['url']="http://www.jztb.gov.cn/jyxx/%s/%s/%s/%s.html"%(url_type,url_type1[1:-1],url_date,id)
    item['issue_time'] = int(time.mktime(time.strptime(item['_issue_time'], "%Y-%m-%d")))
    if '077001001' in item['_current_start_url'] or '077002001' in item['_current_start_url']:
        item['bid_type'] = 1
    elif '077002002' in item['_current_start_url']:
        item['bid_type']= 4
    elif '077001002' in item['_current_start_url'] or '077002003' in item['_current_start_url']:
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

