# coding: utf-8
import time
import logging


logger = logging.getLogger(__name__)

author = "lidongjie"
web_title = u"运城市工程建设信息网"
data_source = 'http://www.ycggzy.com'

start_urls = [
    # 招标
    "http://www.ycggzy.com/TPFront/jyxx/005001/005001001/",
    "http://www.ycggzy.com/TPFront/jyxx/005002/005002001/",

    # 中标候选人
    "http://www.ycggzy.com/TPFront/jyxx/005001/005001003/",

    # 中标
    "http://www.ycggzy.com/TPFront/jyxx/005001/005001004/",
    "http://www.ycggzy.com/TPFront/jyxx/005002/005002003/",


    # 变更
    "http://www.ycggzy.com/TPFront/jyxx/005001/005001002/",
    "http://www.ycggzy.com/TPFront/jyxx/005002/005002002/",




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
    "_list": {'pattern': "//div[@id='categorypagingcontent']//li", 'type': 'xpath','target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//td[text()='下页 >'and@onclick]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_issue_time": {'pattern': "//span", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='article-block']",'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    "title": {'pattern': "//h2[@class='article-title']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region'] = u'山西—运城'
    item['_delay_between_pages'] = 3

def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    if item['url']=='http://www.ycggzy.com/TPFront/infodetail/?infoid=547c9c97-0835-45f6-a25b-7c0090bd775b&categoryNum=005001001':
        del item['url']
    if item['url']=='http://www.ycggzy.com/TPFront/%e7%bb%b4%e6%8a%a4%e4%b8%ad.htm?aspxerrorpath=/TPFront/infodetail/default.aspx':
        del item['url']
        return
    # 停止翻页
    logger.debug(item['url'])


def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    if not item.get('url'):
        return
    if '005001001' in item['_current_start_url'] or '005002001' in item['_current_start_url']:
        item['bid_type'] = 1
    elif '005001004' in item['_current_start_url'] or '005002003' in item['_current_start_url']:
        item['bid_type'] = 0
    elif '005001002' in item['_current_start_url'] or '005002002' in item['_current_start_url']:
        item['bid_type'] = 2
    elif '005001003' in item['_current_start_url'] :
        item['bid_type'] = 4



    logger.debug('%s   %s', item['title'], item['_issue_time'])
    item['issue_time'] = int(time.mktime(time.strptime(item['_issue_time'], "%Y-%m-%d")))

    if len(item['sc']) != 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0
