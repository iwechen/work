# coding: utf-8
import time
import logging
import re
logger = logging.getLogger(__name__)

author = "lidongjie"
web_title = u"茂名公共资源交易网"
data_source = 'http://jyzx.maoming.gov.cn'

start_urls = [
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001001/033001001001/033001001001001/",  #招标公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001001/033001001001/033001001001002/",  #招标公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001001/033001001001/033001001001003/",  #招标公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001001/033001001001/033001001001004/",  #招标公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001001/033001001002/033001001002001/",  #变更公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001001/033001001002/033001001002002/",  #变更公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001001/033001001002/033001001002003/",  #变更公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001001/033001001002/033001001002004/",  #变更公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001001/033001001003/033001001003001/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001001/033001001003/033001001003002/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001001/033001001003/033001001003003/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001001/033001001003/033001001003004/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001002/033001002001/033001002001001/",  #招标公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001002/033001002001/033001002001002/",  #招标公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001002/033001002001/033001002001003/",  #招标公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001002/033001002001/033001002001004/",  #招标公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001002/033001002002/033001002002001/",  #变更公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001002/033001002002/033001002002002/",  #变更公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001002/033001002002/033001002002003/",  #变更公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001002/033001002002/033001002002004/",  #变更公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001002/033001002003/033001002003001/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001002/033001002003/033001002003002/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001002/033001002003/033001002003003/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033001/033001002/033001002003/033001002003004/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001001/033002001001001/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001001/033002001001002/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001001/033002001001003/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001001/033002001001004/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001001/033002001001005/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001001/033002001001006/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001002/033002001002001/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001002/033002001002002/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001002/033002001002003/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001002/033002001002004/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001002/033002001002005/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001002/033002001002006/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001003/033002001003001/",  #变更公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001003/033002001003002/",  #变更公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001003/033002001003003/",  #变更公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001003/033002001003004/",  #变更公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001003/033002001003005/",  #变更公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001003/033002001003006/",  #变更公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001003/033002001003001/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001004/033002001004002/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001004/033002001004003/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001004/033002001004004/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001004/033002001004005/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002001/033002001004/033002001004006/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002001/033002002001001/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002001/033002002001003/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002001/033002002001004/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002001/033002002001005/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002001/033002002001006/",  #采购公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002002/033002002002001/",  #变更公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002002/033002002002002/",  #变更公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002002/033002002002003/",  #变更公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002002/033002002002004/",  #变更公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002002/033002002002005/",  #变更公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002002/033002002002006/",  #变更公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002003/033002002003001/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002003/033002002003002/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002003/033002002003003/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002003/033002002003004/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002003/033002002003005/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002003/033002002003006/",  #中标公示
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002004/033002002004001/",  #招标失败公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002004/033002002004003/",  #招标失败公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002004/033002002004004/",  #招标失败公告
    "http://jyzx.maoming.gov.cn/mmzbtb/jyxx/033002/033002002/033002002004/033002002004005/",  #招标失败公告


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
    "_list": {'pattern': "//tr[@height='22']",'type':'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//img[@src='/mmzbtb/images/page/nextn.gif']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_issue_time":{'pattern': "//td[3]", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''}
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//table[@id='Table4']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//td[@id='tdTitle']//b", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region']=u'广东—茂名'
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
    if re.search(u'(中标)|(竞争性谈判公示)', item['title']):
        item['bid_type'] = '0'
    elif re.search(u'(招标)|(竞争性谈判公告)|(延期)', item['title']):
        item['bid_type'] = '1'
    elif re.search(u'更正', item['title']):
        item['bid_type'] = '2'
    elif re.search(u'未入围', item['title']):
        item['bid_type'] = '3'
    elif re.search(u'(预中标)|(中标预告)|(中标候选人)|(询价)', item['title']):
        item['bid_type'] = '4'
    elif re.search(u'(限价公告)|(最后限价)', item['title']):
        item['bid_type'] = '5'
    elif re.search(u'成交', item['title']):
        item['bid_type'] = '6'
    elif re.search(u'(资格预审)|(审查)', item['title']):
        item['bid_type'] = '7'
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
