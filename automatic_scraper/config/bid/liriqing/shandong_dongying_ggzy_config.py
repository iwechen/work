# coding: utf-8
import time
import logging

logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"东营市公共资源交易网"
data_source = 'http://www.dyggzyjy.gov.cn'

start_urls = [
    #招标公告
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002001/004002001001/MoreInfo.aspx?CategoryNum=004002001001",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002001/004002001002/MoreInfo.aspx?CategoryNum=004002001002",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002001/004002001003/MoreInfo.aspx?CategoryNum=004002001003",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002001/004002001004/MoreInfo.aspx?CategoryNum=004002001004",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002001/004002001005/MoreInfo.aspx?CategoryNum=004002001005",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002001/004002001006/MoreInfo.aspx?CategoryNum=004002001006",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002001/004002001007/MoreInfo.aspx?CategoryNum=004002001007",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002001/004002001008/MoreInfo.aspx?CategoryNum=004002001008"
    #变更公告
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002002/004002002001/MoreInfo.aspx?CategoryNum=004002002001",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002002/004002002002/MoreInfo.aspx?CategoryNum=004002002002",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002002/004002002003/MoreInfo.aspx?CategoryNum=004002002003",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002002/004002002004/MoreInfo.aspx?CategoryNum=004002002004",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002002/004002002005/MoreInfo.aspx?CategoryNum=004002002005",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002002/004002002006/MoreInfo.aspx?CategoryNum=004002002006",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002002/004002002007/MoreInfo.aspx?CategoryNum=004002002007",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002002/004002002008/MoreInfo.aspx?CategoryNum=004002002008"
    #结果公告
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002003/004002003001/MoreInfo.aspx?CategoryNum=004002003001",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002003/004002003002/MoreInfo.aspx?CategoryNum=004002003002",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002003/004002003003/MoreInfo.aspx?CategoryNum=004002003003",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002003/004002003004/MoreInfo.aspx?CategoryNum=004002003004",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002003/004002003005/MoreInfo.aspx?CategoryNum=004002003005",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002003/004002003006/MoreInfo.aspx?CategoryNum=004002003006",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002003/004002003007/MoreInfo.aspx?CategoryNum=004002003007",
    "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002003/004002003008/MoreInfo.aspx?CategoryNum=004002003008"
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
    "_list": {'pattern': "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//img[@src='/dysite/images/page/nextn.gif']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "issue_time": {'pattern': "//td[@style='border-style:None;width:80px;']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a[@target='_blank']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//table[@id='tblInfo']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region']=u'山东-东营市'


def process_list_item(list_element, item):
    """处理列表页元素

    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "%Y-%m-%d")))
    if item['_current_start_url'][-4:-3]=='1':
        item['bid_type']=1
    elif item['_current_start_url'][-4:-3]=='2':
        item['bid_type']=2
    elif item['_current_start_url'][-4:-3]=='3':
        item['bid_type']=0
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

