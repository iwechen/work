# coding: utf-8
import time
import logging
from bs4 import BeautifulSoup
import hashlib
import re
import requests
import urlparse

logger = logging.getLogger(__name__)

author = "huangtaiwu"
web_title = u"长沙公共资源交易监管网"
data_source = 'https://csggzy.gov.cn'

start_urls = [
    "https://csggzy.gov.cn/NoticeFile.aspx/Index/1?type=201&Ptype=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE&Sm=%E4%BA%A4%E9%80%9A%E5%B7%A5%E7%A8%8B&Sm2=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A",#1
    "https://csggzy.gov.cn/NoticeFile/Index?type=201&Sm=%E4%BA%A4%E9%80%9A%E5%B7%A5%E7%A8%8B&Ptype=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE&Sm2=%E4%B8%AD%E6%A0%87%E5%80%99%E9%80%89%E4%BA%BA%E5%85%AC%E7%A4%BA",#4
    "https://csggzy.gov.cn/NoticeFile.aspx/Index/1?type=301&Ptype=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE&Sm=%E6%B0%B4%E5%88%A9%E5%B7%A5%E7%A8%8B&Sm2=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A",#1
    "https://csggzy.gov.cn/NoticeFile/Index?type=301&Sm=%E6%B0%B4%E5%88%A9%E5%B7%A5%E7%A8%8B&Ptype=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE&Sm2=%E4%B8%AD%E6%A0%87%E5%80%99%E9%80%89%E4%BA%BA%E5%85%AC%E7%A4%BA",#4
    "https://csggzy.gov.cn/NoticeFile.aspx/Index/1?type=102&Ptype=%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD&Sm=%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD&Sm2=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A",#1
    "https://csggzy.gov.cn/NoticeFile/Index?type=102&Sm=%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD&Ptype=%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD&Sm2=%E7%BB%93%E6%9E%9C%E5%85%AC%E5%91%8A",#0
    "https://csggzy.gov.cn/NoticeFile.aspx/Index/1?type=104&Ptype=%E5%8C%BB%E8%8D%AF%E9%87%87%E8%B4%AD&Sm=%E5%8C%BB%E8%8D%AF%E9%87%87%E8%B4%AD&Sm2=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A",#1
    "https://csggzy.gov.cn/NoticeFile/Index?type=104&Sm=%E5%8C%BB%E8%8D%AF%E9%87%87%E8%B4%AD&Ptype=%E5%8C%BB%E8%8D%AF%E9%87%87%E8%B4%AD&Sm2=%E7%BB%93%E6%9E%9C%E5%85%AC%E5%91%8A",#0
]

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'huang960428',
    'database': 'bid_data',
    'table': 'zhaotoubiao'
}

# 列表页模板
index_pattern = {
    "_list": {'pattern': "//table[@width='94%']//tr[position()<last() and position()>1][position()=1 or position()=3 or position()=5 or position()=7 or  position()=9 or position()=11 or position()=13 or  position()=15 or position()=17 or position()=19]", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': "//a[@href]/img[@src='/yzweb/images/page/nextn.gif']", 'type': 'xpath', 'target': 'html',
                   'custom_func_name': ''},
    "issue_time": {'pattern': "//td[@align='right']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}
# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='detail']", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
    # "title": {'pattern': "//div[@align='center']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'湖南省-长沙市'
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
    if re.search('%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A',item['_current_start_url']):
        item['bid_type'] = 1
    elif re.search('%E7%BB%93%E6%9E%9C%E5%85%AC%E5%91%8A',item['_current_start_url']):
        item['bid_type'] = 0
    else:
        item['bid_type'] = 4

    soup = BeautifulSoup(list_element, 'html.parser')
    href = soup.find('a').attrs['href']
    detail_url = urlparse.urljoin(item['_current_start_url'], href)
    res = requests.get(detail_url, stream=True)
    if int(res.headers['content-length']) < 500:
        del item['url']

    logger.debug(u"{} {}".format(item['title'], item['issue_time']))
    item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], "%Y-%m-%d")))
    # if item['_current_page'] == 10:
    #     item['_click_next'] = False


def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    if len(item['sc']) > 100:
        item['is_get'] = 1
    else:
        item['is_get'] = 0


