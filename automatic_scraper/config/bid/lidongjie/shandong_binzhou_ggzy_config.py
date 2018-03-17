# coding: utf-8
import time
import logging
import re

logger = logging.getLogger(__name__)

author = "lidongjie"
web_title = u"滨州公共资源交易网"
data_source = 'http://www.bzggzyjy.gov.cn'

start_urls = [
    #招标公告
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004001/002004001001/MoreInfo.aspx?CategoryNum=002004001001",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004001/002004001002/MoreInfo.aspx?CategoryNum=002004001002",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004001/002004001003/MoreInfo.aspx?CategoryNum=002004001003",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004001/002004001004/MoreInfo.aspx?CategoryNum=002004001004",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004001/002004001005/MoreInfo.aspx?CategoryNum=002004001005",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004001/002004001006/MoreInfo.aspx?CategoryNum=002004001006",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004001/002004001007/MoreInfo.aspx?CategoryNum=002004001007",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004001/002004001008/MoreInfo.aspx?CategoryNum=002004001008",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004001/002004001009/MoreInfo.aspx?CategoryNum=002004001009",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004001/002004001010/MoreInfo.aspx?CategoryNum=002004001010",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004001/002004001011/MoreInfo.aspx?CategoryNum=002004001011",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/002005001001/002005001001001/MoreInfo.aspx?CategoryNum=002005001001001",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/002005001001/002005001001002/MoreInfo.aspx?CategoryNum=002005001001002",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/002005001001/002005001001003/MoreInfo.aspx?CategoryNum=002005001001003",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/002005001001/002005001001004/MoreInfo.aspx?CategoryNum=002005001001004",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/002005001001/002005001001005/MoreInfo.aspx?CategoryNum=002005001001005",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/002005001001/002005001001006/MoreInfo.aspx?CategoryNum=002005001001006",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/002005001001/002005001001007/MoreInfo.aspx?CategoryNum=002005001001007",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/002005001001/002005001001008/MoreInfo.aspx?CategoryNum=002005001001008",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/002005001001/002005001001009/MoreInfo.aspx?CategoryNum=002005001001009",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/002005001001/002005001001010/MoreInfo.aspx?CategoryNum=002005001001010",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/002005001001/002005001001011/MoreInfo.aspx?CategoryNum=002005001001011",
    #中标公示
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004002/002004002001/MoreInfo.aspx?CategoryNum=002004002001",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004002/002004002002/MoreInfo.aspx?CategoryNum=002004002002",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004002/002004002003/MoreInfo.aspx?CategoryNum=002004002003",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004002/002004002004/MoreInfo.aspx?CategoryNum=002004002004",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004002/002004002005/MoreInfo.aspx?CategoryNum=002004002005",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004002/002004002006/MoreInfo.aspx?CategoryNum=002004002006",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004002/002004002007/MoreInfo.aspx?CategoryNum=002004002007",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004002/002004002008/MoreInfo.aspx?CategoryNum=002004002008",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004002/002004002009/MoreInfo.aspx?CategoryNum=002004002009",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004002/002004002010/MoreInfo.aspx?CategoryNum=002004002010",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004002/002004002011/MoreInfo.aspx?CategoryNum=002004002011",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005003/002005003001/MoreInfo.aspx?CategoryNum=002005003001",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005003/002005003002/MoreInfo.aspx?CategoryNum=002005003002",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005003/002005003003/MoreInfo.aspx?CategoryNum=002005003003",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005003/002005003004/MoreInfo.aspx?CategoryNum=002005003004",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005003/002005003005/MoreInfo.aspx?CategoryNum=002005003005",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005003/002005003006/MoreInfo.aspx?CategoryNum=002005003006",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005003/002005003007/MoreInfo.aspx?CategoryNum=002005003007",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005003/002005003008/MoreInfo.aspx?CategoryNum=002005003008",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005003/002005003009/MoreInfo.aspx?CategoryNum=002005003009",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005003/002005003010/MoreInfo.aspx?CategoryNum=002005003010",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005003/002005003011/MoreInfo.aspx?CategoryNum=002005003011",
    #变更公告
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004003/002004003001/MoreInfo.aspx?CategoryNum=002004003001"
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004003/002004003002/MoreInfo.aspx?CategoryNum=002004003002",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004003/002004003003/MoreInfo.aspx?CategoryNum=002004003003",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004003/002004003004/MoreInfo.aspx?CategoryNum=002004003004",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004003/002004003005/MoreInfo.aspx?CategoryNum=002004003005",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004003/002004003006/MoreInfo.aspx?CategoryNum=002004003006",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004003/002004003007/MoreInfo.aspx?CategoryNum=002004003007",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004003/002004003008/MoreInfo.aspx?CategoryNum=002004003008",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004003/002004003009/MoreInfo.aspx?CategoryNum=002004003009",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004003/002004003010/MoreInfo.aspx?CategoryNum=002004003010",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004003/002004003011/MoreInfo.aspx?CategoryNum=002004003011",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005002/002005002001/MoreInfo.aspx?CategoryNum=002005002001",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005002/002005001002/MoreInfo.aspx?CategoryNum=002005002002",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005002/002005001003/MoreInfo.aspx?CategoryNum=002005002003",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005002/002005001004/MoreInfo.aspx?CategoryNum=002005002004",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005002/002005001005/MoreInfo.aspx?CategoryNum=002005002005",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005002/002005001006/MoreInfo.aspx?CategoryNum=002005002006",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005002/002005001007/MoreInfo.aspx?CategoryNum=002005002007",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005002/002005001008/MoreInfo.aspx?CategoryNum=002005002008",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005002/002005001009/MoreInfo.aspx?CategoryNum=002005002009",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005002/002005001010/MoreInfo.aspx?CategoryNum=002005002010",
    "http://www.bzggzyjy.gov.cn/bzweb/002/002004/002005002/002005001011/MoreInfo.aspx?CategoryNum=002005002011",

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
    "_list": {'pattern': "//table[@id='MoreInfoList1_DataGrid1']//tr",'type':'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//a[text()='下一页' and@href]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_issue_time":{'pattern': "//td[3]", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''}
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//td[@id='TDContent']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//td[@id='tdTitle']//h2", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},


    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'山东—滨州'
    del item['web_title']
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
    if '002004001' in item['_current_start_url'] or'002005001' in item['_current_start_url'] :
        item['bid_type'] = 1
    elif '002004002' in item['_current_start_url'] or'002005003' in item['_current_start_url'] :
        item['bid_type'] = 0
    elif '002004003' in item['_current_start_url'] or'002005002' in item['_current_start_url'] :
        item['bid_type'] = 2

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