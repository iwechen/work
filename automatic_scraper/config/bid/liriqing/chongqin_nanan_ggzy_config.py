# coding: utf-8
import time
import logging
import re
import requests
from bs4 import BeautifulSoup
logger = logging.getLogger(__name__)

author = "liriqing"
web_title = u"南岸区公共资源"
data_source = 'http://www.naggzy.gov.cn'

start_urls = [
    #招标公告
    "http://www.naggzy.gov.cn/articleWeb!list.action?resourceCode=jszbgg",
    "http://www.naggzy.gov.cn/articleWeb!list.action?resourceCode=cqzbgg",
    "http://www.naggzy.gov.cn/articleWeb!list.action?resourceCode=cgzbgg",

    #中标
    "http://www.naggzy.gov.cn/articleWeb!list.action?resourceCode=jszbgs",
    "http://www.naggzy.gov.cn/articleWeb!list.action?resourceCode=cqzbgs",
    "http://www.naggzy.gov.cn/articleWeb!list.action?resourceCode=cgzbgs"

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
    "_list": {'pattern': "//table[@class='in_ullist']//tr", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//a[text()='后一页' and @onclick] ", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "issue_time": {'pattern': "//td[@width='160']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "/html", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    item['region']=u'重庆-南岸区'
    item['_delay_between_pages'] = 10


def process_list_item(list_element, item):
    """处理列表页元素

    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    logger.debug(item['issue_time'])


    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], u"%Y-%m-%d")))
    if 'jszbgg' in item['_current_start_url'] or 'cqzbgg' in item['_current_start_url'] or 'cgzbgg' in item['_current_start_url']:
        item['bid_type'] = 1

    elif 'jszbgs' in item['_current_start_url'] or 'cqzbgs' in item['_current_start_url'] or 'cgzbgs' in item['_current_start_url']:
        item['bid_type'] = 0
    #yd_cookie=aa95899f-fabc-45b74508b870e34b0f879106be5c645856c0; path=/
    #yd_cookie=aa95899f-fabc-45b74508b870e34b0f879106be5c645856c0; path=/
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
    data = requests.get(item['url']).headers
    # cookie = re.search(r'yd_cookie=(.*?);', str(data), re.S).group(1)
    item['_cookie'] = data['Set-Cookie']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Content-Type': 'text/html;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Cookie': 'yd_cookie=0575dce4-0b06-48fe267dfbd4745db2d7668d5347358a0d38; _ydclearance=338283371f12165115ff80bd-3819-45c3-ba02-f850b9dc56be-1507808392; JSESSIONID=3D6C108C40408D15281596EEEC563187; _gscu_1555280000=07801195dqe8i417; _gscs_1555280000=0780119566js8l17|pv:1; _gscbrs_1555280000=1'
    }
    sc_requests=requests.get(item['url'],headers=headers)
    sc_requests.encoding='utf-8'
    sc_node=BeautifulSoup(sc_requests.content,'html.parser')
    sc=sc_node.find('td',class_="sub_content")
    item['sc']=str(sc)
    if len(item['sc']) > 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0

