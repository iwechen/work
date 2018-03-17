# coding: utf-8
import time
import logging

logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"淄博市公共资源交易网"
data_source = 'http://www.zbggzyjy.gov.cn'

start_urls = [
    #招标公告
    "http://www.zbggzyjy.gov.cn/TPFront/jyxx/002002/002002001/002002001001/MoreInfo.aspx?CategoryNum=268960257",
    "http://www.zbggzyjy.gov.cn/TPFront/jyxx/002002/002002001/002002001002/MoreInfo.aspx?CategoryNum=268960258",
    "http://www.zbggzyjy.gov.cn/TPFront/jyxx/002002/002002001/002002001004/MoreInfo.aspx?CategoryNum=268960260",
    "http://www.zbggzyjy.gov.cn/TPFront/jyxx/002002/002002001/002002001005/MoreInfo.aspx?CategoryNum=268960261",
    #建设工程招标
    "http://www.zbggzyjy.gov.cn/TPFront/jyxx/002001/002001001/002001001001/MoreInfo.aspx?CategoryNum=268698113",

    #变更公告
    "http://www.zbggzyjy.gov.cn/TPFront/jyxx/002002/002002002/002002002001/MoreInfo.aspx?CategoryNum=268960769",
    "http://www.zbggzyjy.gov.cn/TPFront/jyxx/002002/002002002/002002002002/MoreInfo.aspx?CategoryNum=268960770",
    "http://www.zbggzyjy.gov.cn/TPFront/jyxx/002002/002002002/002002002005/MoreInfo.aspx?CategoryNum=268960773",
    #建设工程变更
    "http://www.zbggzyjy.gov.cn/TPFront/jyxx/002001/002001002/002001002001/MoreInfo.aspx?CategoryNum=268698625",
    #结果公告
    "http://www.zbggzyjy.gov.cn/TPFront/jyxx/002002/002002003/002002003001/MoreInfo.aspx?CategoryNum=268961281",
    "http://www.zbggzyjy.gov.cn/TPFront/jyxx/002002/002002003/002002003002/MoreInfo.aspx?CategoryNum=268961282",
    "http://www.zbggzyjy.gov.cn/TPFront/jyxx/002002/002002003/002002003004/MoreInfo.aspx?CategoryNum=268961284",
    "http://www.zbggzyjy.gov.cn/TPFront/jyxx/002002/002002003/002002003005/MoreInfo.aspx?CategoryNum=268961285",
    #建设工程结果公告
    "http://www.zbggzyjy.gov.cn/TPFront/jyxx/002001/002001003/002001003001/MoreInfo.aspx?CategoryNum=268699137",

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
    "_next_page": {'pattern': "//img[@src='/TPFront/images/page/nextn.gif']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
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
    item['region']=u'山东-淄博市'


def process_list_item(list_element, item):
    """处理列表页元素

    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    logging.debug(item['_current_start_url'][55:56])
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "%Y-%m-%d")))
    if item['_current_start_url'][55:56]=='1':
        item['bid_type']=1
    elif item['_current_start_url'][55:56]=='2':
        item['bid_type']=2
    elif item['_current_start_url'][55:56]=='3':
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

