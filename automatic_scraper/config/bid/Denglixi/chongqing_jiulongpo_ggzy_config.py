# coding: utf-8
import time
import logging
from bs4 import BeautifulSoup
import hashlib

logger = logging.getLogger(__name__)

author = "Denglixi"
web_title = u"重庆市九龙坡区公共资源"
data_source = 'http://www.cqjlpggzyzhjy.gov.cn'

start_urls = [
    # 招标
    "http://www.cqjlpggzyzhjy.gov.cn/cqjl/jyxx/003001/003001001/003001001001/MoreInfo.aspx?CategoryNum=003001001001",
    "http://www.cqjlpggzyzhjy.gov.cn/cqjl/jyxx/003001/003001001/003001001002/MoreInfo.aspx?CategoryNum=003001001002",
    "http://www.cqjlpggzyzhjy.gov.cn/cqjl/jyxx/003002/003002001/MoreInfo.aspx?CategoryNum=003002001",

    # 中标
    "http://www.cqjlpggzyzhjy.gov.cn/cqjl/jyxx/003002/003002002/MoreInfo.aspx?CategoryNum=003002002",
    "http://www.cqjlpggzyzhjy.gov.cn/cqjl/jyxx/003001/003001002/MoreInfo.aspx?CategoryNum=003001002",

    # 最高限价
    "http://www.cqjlpggzyzhjy.gov.cn/cqjl/jyxx/003001/003001003/MoreInfo.aspx?CategoryNum=003001003",
    # 变更
    "http://www.cqjlpggzyzhjy.gov.cn/cqjl/jyxx/003002/003002003/MoreInfo.aspx?CategoryNum=003002003",
]

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '114514',
    'database': 'bid_data',
    'table': 'zhaotoubiao'
}

# 列表页模板
index_pattern = {
    "_list": {'pattern': "//table[@id='MoreInfoList1_DataGrid1']//tr", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//div[@id='MoreInfoList1_Pager']//img[@src='/cqjl/images/page/nextn.gif']//parent::a", 'type': 'xpath', 'target': 'html',
                   'custom_func_name': ''},
    "issue_time": {'pattern': "//td[@style='border-style:None;width:80px;']/text()", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a/@title", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//table[@style='border:1px solid #bcbcbc']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "title": {'pattern': "//div[@align='center']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']


def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    # 停止翻页
    if 'ReadAttachFile' in item['url']:
        del item['url']
        return
    if '003001001' in item['_current_start_url'] or '003002001' in item['_current_start_url']:
        item['bid_type'] = 1

    elif '003002002' in item['_current_start_url'] or '003001002' in item['_current_start_url']:
        item['bid_type'] = 0
    elif '003001003' in item['_current_start_url']:
        item['bid_type'] = 5
    elif '003002003' in item['_current_start_url']:
        item['bid_type'] = 2
    # logger.debug(u"{} {}".format(item['title'], item['issue_time']))
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "%Y-%m-%d")))
    # if item['_current_page'] == 10:
    #     item['_click_next'] = False


def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    if len(item['sc']) > 100:
        item['is_get'] = 1
    else:
        item['is_get'] = 0


