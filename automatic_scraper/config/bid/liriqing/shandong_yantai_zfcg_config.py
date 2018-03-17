# coding: utf-8
import time
import logging
import re
logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"烟台市政府采购网"
data_source = 'http://cgb.yantai.gov.cn'

start_urls = [
    #市级招标公告
    "http://cgb.yantai.gov.cn/col/col2704/index.html",
    #县市区级采购公告
    "http://cgb.yantai.gov.cn/col/col2698/index.html",
    #县市区级成交公告
    "http://cgb.yantai.gov.cn/col/col7206/index.html",
    #县市区级更正公告
    "http://cgb.yantai.gov.cn/col/col7207/index.html",
    #县市区级采购合同
    "http://cgb.yantai.gov.cn/col/col7211/index.html",
    #县市区级验收公告
    "http://cgb.yantai.gov.cn/col/col7212/index.html",
    #芝罘区采购公告
    "http://cgb.yantai.gov.cn/col/col2717/index.html",
    #莱山区采购公告
    "http://cgb.yantai.gov.cn/col/col2725/index.html",
    #福山区采购公告
    "http://cgb.yantai.gov.cn/col/col2716/index.html",
    #牟平区采购公告
    "http://cgb.yantai.gov.cn/col/col2724/index.html",
    #开发区采购公告
    "http://cgb.yantai.gov.cn/col/col2723/index.html",
    #高新区采购公告
    "http://cgb.yantai.gov.cn/col/col2722/index.html",
    #蓬莱市采购公告
    "http://cgb.yantai.gov.cn/col/col2721/index.html",
    #龙口市采购公告
    "http://cgb.yantai.gov.cn/col/col2720/index.html",
    #莱州市采购公告
    "http://cgb.yantai.gov.cn/col/col2719/index.html",
    #招远市采购公告
    "http://cgb.yantai.gov.cn/col/col2706/index.html",
    #栖霞市采购公告
    "http://cgb.yantai.gov.cn/col/col2710/index.html",
    #莱阳市采购公告
    "http://cgb.yantai.gov.cn/col/col2711/index.html",
    #海阳市采购公告
    "http://cgb.yantai.gov.cn/col/col2712/index.html",
    #长岛县采购公告
    "http://cgb.yantai.gov.cn/col/col2713/index.html",
    #保税港区采购公告
    "http://cgb.yantai.gov.cn/col/col2718/index.html"
    #昆嵛山采购公告
    "http://cgb.yantai.gov.cn/col/col5899/index.html",
    #东部新区采购公告
    "http://cgb.yantai.gov.cn/col/col5900/index.html"
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
    "_list": {'pattern': "//div[@class='default_pgContainer']/ul/li", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//div[@class='default_pgBtn default_pgNext']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "issue_time": {'pattern': "//span[@class='bt_time']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a[@target='_blank']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    #"title_type": {'pattern': "//a[@class='bt_link']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='con03']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region']=u'山东-烟台市'
    #item['_delay_between_pages'] = 3


def process_list_item(list_element, item):
    """处理列表页元素

    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    logging.debug(list_element)
    item['title_type']=re.search(r'\[(.*?)\]',list_element,re.S).group(1)
    logging.debug(item['title_type'])
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "%Y-%m-%d")))
    if u'采购公告' in item['title_type']:
        item['bid_type'] = 1
    elif u'成交公告' in item['title_type']:
        item['bid_type'] = 0
    elif u'更正公告' in item['title_type']:
        item['bid_type'] = 2
    elif u'采购合同' in item['title_type']:
        item['bid_type'] = 0
    elif u'验收公告' in item['title_type']:
        item['bid_type'] = 0
    del item['title_type']
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

