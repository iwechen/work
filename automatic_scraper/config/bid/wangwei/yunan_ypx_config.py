# coding=utf-8
import time
import logging
import re

logger = logging.getLogger(__name__)

author = "WangWei"
web_title = u"永平县人民政府"
data_source = 'http://www.ypx.gov.cn'

start_urls = [
    "http://www.ypx.gov.cn/ypgov/1514058302068097024/index.html",
    "http://www.ypx.gov.cn/ypgov/1514058306363064320/index.html"
]

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'ww7841250',
    'database': 'autometic_spider',
    'table': 'zhaotoubiao'
}

# 列表页模板
index_pattern = {
    "_list": {'pattern': "//table[@width='98%']//td[@width='100%']", 'type': 'xpath', 'target': 'html','custom_func_name': ''},
    "_next_page": {'pattern': u"//a[@href and text()='下一页']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//a//font", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''}

}
# 详情页模板
detail_pattern = {
    "issue_time": {'pattern': "//font[@style='font-size: 14px']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "sc": {'pattern': "//table[@style=' BORDER-RIGHT: #B6C5D2 1px solid;  BORDER-LEFT: #B6C5D2 1px solid; BORDER-BOTTOM: #B6C5D2 1px solid;']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''}
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'云南省-大理州'
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
    logger.debug('%s',item['url'])
    if re.search(u'(中标)|(竞争性谈判公示)',item['title']):
        item['bid_type'] = '0'
    elif re.search(u'(招标)|(竞争性谈判公告)|(延期)', item['title']):
        item['bid_type'] = '1'
    elif re.search(u'(更正)|(变更)', item['title']):
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
    logger.debug('%s', item['title'])

def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    item['issue_time']=re.search(r'\d{4}-\d{2}-\d{2}',item['issue_time']).group(0)
    try:
        item['issue_time'] = int(time.mktime(time.strptime(str(item['issue_time']), u"%Y-%m-%d")))
    except ValueError,e:
        item['issue_time']=0
    if len(item['sc']) > 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0
