# coding=utf-8
import time
import logging
import re

logger = logging.getLogger(__name__)

author = "WangWei"
web_title = u"江西方正工程监理造价咨询有限公司"
data_source = 'http://www.jxfzjl.com'

start_urls = [
    "http://www.jxfzjl.com/temp.hbml?pid=116&dir=116"
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
    "_list": {'pattern': "//div[@class='news2']//li", 'type': 'xpath', 'target': 'html','custom_func_name': ''},
    "_next_page": {'pattern': u"//a[@href and text()='下一页']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "issue_time": {'pattern': "//span[@class='time']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''}

}
# 详情页模板
detail_pattern = {
    "title": {'pattern': "//div[@class='newscont']/h2", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "sc": {'pattern': "//div[@style='margin-top:20px;']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''}
}

data_list=[
    r'\d{4}-\d-\d',
    r'\d{4}-\d-\d{2}',
    r'\d{4}-\d{2}-\d',
    r'\d{4}-\d{2}-\d{2}'
]

def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'江西省'
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
    for data_item in data_list:
        match_data_result=re.search(data_item,item['issue_time'])
        if match_data_result is not None:
            item['issue_time']=match_data_result.group(0)
            item['issue_time'] = int(time.mktime(time.strptime(str(item['issue_time']), u"%Y-%m-%d")))
            break

def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
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
    if len(item['sc']) > 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0
