# coding: utf-8
import time
import logging
import re
logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"吉林省公共资源交易网"
data_source = 'http://ggzyjy.jl.gov.cn'

start_urls = [
    #招标公告
    "http://ggzyjy.jl.gov.cn/JiLinZtb//Template/Default/ZBGGMoreInfoJYXX.aspx?CategoryNum=004001",
    #预中标
    "http://ggzyjy.jl.gov.cn/JiLinZtb//Template/Default/MoreInfoJYXX.aspx?CategoryNum=004002",
    #变更公告
    "http://ggzyjy.jl.gov.cn/JiLinZtb//Template/Default/MoreInfoJYXX.aspx?CategoryNum=004003",
    #合同公告
    "http://ggzyjy.jl.gov.cn/JiLinZtb//Template/Default/MoreInfoJYXX.aspx?CategoryNum=004005",

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
    "_list": {'pattern': "//td[@width='260']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//img[@src='/JiLinZtb/Images/page/nextn.gif']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//a[@target='_blank']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//table[@id='tblInfo']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "issue_time": {'pattern': "//font[@color='#888888']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region']=u'山东-东营市'
    item['_delay_between_pages'] = 3


def process_list_item(list_element, item):
    """处理列表页元素

    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """

    #item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "%Y-%m-%d")))
    if '004001' in item['_current_start_url']:
        item['bid_type']=1
    elif '004002' in item['_current_start_url']:
        item['bid_type']=4
    elif '004003' in item['_current_start_url']:
        item['bid_type'] = 2
    elif '004005' in item['_current_start_url']:
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
    time_data=re.search(r'(\d+)/(\d+)/(\d+)',item['issue_time'].strip(),re.S).group()
    item['issue_time'] = int(time.mktime(time.strptime(time_data, "%Y/%m/%d")))
    if len(item['sc']) > 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0

