# coding: utf-8
import time
import logging
import re
from  bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"中国装修采购网"
data_source = 'http://www.zxzbcg.com'

start_urls = [

     #政府采购
    "http://www.zxzbcg.com/nr.jsp",












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
    "_list": {'pattern': "//a[@class='fk-newsListTitle']",'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern':u"//a/span[contains(text(),'下一页')]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='newsDetail']/div[6]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_issue_time": {'pattern': "/html//span[@class='sourceInfoContent'][1]", 'type': 'xpath', 'target': 'text','custom_func_name': ''},

    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region']=u'中国-装修'
    item['_delay_between_pages'] = 3


def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """



    if re.search(ur'招标|采购',item['title']):
        item['bid_type'] = 1
    elif re.search(ur'中标公告',item['title']):
        item['bid_type'] = 0
    elif re.search(ur'候选人', item['title']):
        item['bid_type'] = 4
    elif re.search(ur'变更|更正', item['title']):
        item['bid_type'] = 2
        #停止翻页



def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """

    time_data = re.search(r'(\d+)-(\d+)-(\d+) (\d+):(\d+)', item['_issue_time'], re.S).group()
    item['issue_time'] = int(time.mktime(time.strptime(time_data.strip(), u"%Y-%m-%d %H:%M")))
    if len(item['sc']) > 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0

