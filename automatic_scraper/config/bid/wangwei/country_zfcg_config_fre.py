# coding: utf-8
import logging
import time
import re
import requests

logger = logging.getLogger(__name__)

author = "WangWei"
web_title = u"中国政府采购网"
data_source = 'http://www.ccgp.gov.cn'

start_urls = [
    "http://www.ccgp.gov.cn/cggg/zygg/gkzb/",
    "http://www.ccgp.gov.cn/cggg/zygg/zbgg/",
    "http://www.ccgp.gov.cn/cggg/zygg/gzgg/",
    "http://www.ccgp.gov.cn/cggg/zygg/qtgg/",
    "http://www.ccgp.gov.cn/cggg/zygg/xjgg/",
    "http://www.ccgp.gov.cn/cggg/zygg/yqzbgg/",
    "http://www.ccgp.gov.cn/cggg/zygg/dylygg/",
    "http://www.ccgp.gov.cn/cggg/zygg/zgysgg/",
    "http://www.ccgp.gov.cn/cggg/zygg/cjgg/",
    "http://www.ccgp.gov.cn/cggg/zygg/jzxtpgg/",
    "http://www.ccgp.gov.cn/cggg/zygg/jzxcs/",
    "http://www.ccgp.gov.cn/cggg/zygg/fblbgg/",
    "http://www.ccgp.gov.cn/cggg/dfgg/gkzb/",
    "http://www.ccgp.gov.cn/cggg/dfgg/zbgg/",
    "http://www.ccgp.gov.cn/cggg/dfgg/gzgg/",
    "http://www.ccgp.gov.cn/cggg/dfgg/qtgg/",
    "http://www.ccgp.gov.cn/cggg/dfgg/xjgg/",
    "http://www.ccgp.gov.cn/cggg/dfgg/yqzbgg/",
    "http://www.ccgp.gov.cn/cggg/dfgg/dylygg/",
    "http://www.ccgp.gov.cn/cggg/dfgg/zgysgg/",
    "http://www.ccgp.gov.cn/cggg/dfgg/cjgg/",
    "http://www.ccgp.gov.cn/cggg/dfgg/jzxtpgg/",
    "http://www.ccgp.gov.cn/cggg/dfgg/jzxcs/",
    "http://www.ccgp.gov.cn/cggg/dfgg/fblbgg/"
]

_db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'ww7841250',
    'database': 'zhinengpachong',
    'table': 'zhaotoubiao'
}

# 列表页模板
index_pattern = {
    "_list": {'pattern': "//li[@style='height:60px']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"下一页", 'type': 'partial_link_text', 'target': 'html', 'custom_func_name': ''},
    "issue_time":{'pattern': "//span[1]", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "region":{'pattern': "//span[2]", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "tenderee":{'pattern': "//span[3]", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''}
}

# 详情页模板
detail_pattern = {
    "title": {'pattern': "//div[@class='vT_detail_header']//h2", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "sc": {'pattern': "//div[@class='vT_z w760'][last()]", 'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''}
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']


def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    data=requests.get(item['url'])
    if u'对不起，您所访问的页面不存在。可能原因：' in data.text:
        del item['url']
        return
    if item['tenderee'] is None:
        del item['tenderee']
        return
    # 停止翻页


def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
    if item.get('url') or item.get('tenderee'):
        logger.debug('%s   %s', item['title'], item['issue_time'])
        if re.search(u'(中标)|(竞争性谈判公示)', item['title']):
            item['bid_type'] = '0'
        elif re.search(u'(招标)|(竞争性谈判公告)|(延期)', item['title']):
            item['bid_type'] = '1'
        elif re.search(u'更正', item['title']):
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
        item['issue_time'] = int(time.mktime(time.strptime(item['issue_time'], u"%Y-%m-%d %H:%M:%S")))
        if len(item['sc'])!=0:
            item['is_get']=1
        else:
            item['is_get']=0