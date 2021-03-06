# coding: utf-8
import time
import logging
from bs4 import BeautifulSoup
import hashlib

logger = logging.getLogger(__name__)

author = "Denglixi"
web_title = u"亳州市公共资源交易网"
data_source = 'http://www.bzztb.gov.cn'

start_urls = [
    # 招标
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001001/003001001001/003001001001001/MoreInfo.aspx?CategoryNum=206292910593",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001001/003001001001/003001001001002/MoreInfo.aspx?CategoryNum=206292910594",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001001/003001001002/MoreInfo.aspx?CategoryNum=402915842",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001001/003001001003/MoreInfo.aspx?CategoryNum=402915843",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001001/003001001004/MoreInfo.aspx?CategoryNum=402915844",

    "http://www.bzztb.gov.cn/BZWZ/jyxx/003002/003002001/003002001001/003002001001001/MoreInfo.aspx?CategoryNum=206427128321",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003002/003002001/003002001001/003002001001002/MoreInfo.aspx?CategoryNum=206427128322",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003002/003002001/003002001002/MoreInfo.aspx?CategoryNum=403177986",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003002/003002001/003002001003/MoreInfo.aspx?CategoryNum=403177987",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003002/003002001/003002001004/MoreInfo.aspx?CategoryNum=403177988",

    # 中标
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001004/003001004001/003001004001001/MoreInfo.aspx?CategoryNum=206293697025",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001004/003001004001/003001004001002/MoreInfo.aspx?CategoryNum=206293697026",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001004/003001004002/MoreInfo.aspx?CategoryNum=402917378",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001004/003001004003/MoreInfo.aspx?CategoryNum=402917379",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001004/003001004004/MoreInfo.aspx?CategoryNum=402917380",

    "http://www.bzztb.gov.cn/BZWZ/jyxx/003002/003002002/003002002001/003002002001001/MoreInfo.aspx?CategoryNum=206427390465",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003002/003002002/003002002001/003002002001002/MoreInfo.aspx?CategoryNum=206427390466",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003002/003002002/003002002002/MoreInfo.aspx?CategoryNum=403178498",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003002/003002002/003002002003/MoreInfo.aspx?CategoryNum=403178499",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003002/003002002/003002002004/MoreInfo.aspx?CategoryNum=403178500",

    # 变更

    # 预中标
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001002/003001002001/003001002001001/MoreInfo.aspx?CategoryNum=206293172737",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001002/003001002001/003001002001002/MoreInfo.aspx?CategoryNum=206293172738",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001002/003001002002/MoreInfo.aspx?CategoryNum=402916354",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001002/003001002003/MoreInfo.aspx?CategoryNum=402916355",
    "http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001002/003001002004/MoreInfo.aspx?CategoryNum=402916356",

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
    "_list": {'pattern': "//table[@id='MoreInfoList1_moreinfo']//tr//tr//tr[@height='30px']", 'type': 'xpath',
              'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//div[@class='pagemargin']//td[text()='下页 >' and @onclick]", 'type': 'xpath', 'target': 'html',
                   'custom_func_name': ''},
    "issue_time": {'pattern': "//td[@width='80px']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a/@title", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//table[@id='tblInfo']",
           'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
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
    if '003001001' in item['_current_start_url'] or '003002001' in item[
        '_current_start_url']:
        item['bid_type'] = 1

    elif '003001004' in item['_current_start_url'] or '003002002' in item[
        '_current_start_url']:
        item['bid_type'] = 0
    elif '003001002' in item['_current_start_url']:
        item['bid_type'] = 4
    # logger.debug(u"{} {}".format(item['title'], item['issue_time']))
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "%Y-%m-%d")))
    # if item['_current_page'] == 2:
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
