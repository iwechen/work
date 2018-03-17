# coding: utf-8
import time
import logging
import re
logger = logging.getLogger(__name__)

author = "lidongjie"
web_title = u"佛山公共资源交易网"
data_source = 'http://www.fsggzy.cn'

start_urls = [
    "http://www.fsggzy.cn/zfcg/zf_cggsgg/zf_ggsz/",  #采购公告
    "http://www.fsggzy.cn/zfcg/zf_cggsgg/zcgg_gq/zcgg_cc/",  #采购公告
    "http://www.fsggzy.cn/zfcg/zf_cggsgg/zcgg_gq/zcgg_nh/",  #采购公告
    "http://www.fsggzy.cn/zfcg/zf_cggsgg/zcgg_gq/zcgg_ss/",  #采购公告
    "http://www.fsggzy.cn/zfcg/zf_cggsgg/zcgg_gq/zcgg_gm/",  #采购公告
    "http://www.fsggzy.cn/zfcg/zf_cggsgg/zcgg_gq/zcgg_sd/",  #采购公告
    "http://www.fsggzy.cn/zfcg/zf_cggsgg/zc_zjjg/",  #采购公告
    "http://www.fsggzy.cn/zfcg/zf_gzgg/zf_gzsz/",  #更正公告
    "http://www.fsggzy.cn/zfcg/zf_gzgg/zcgz_gq/zggz_cc/",  #更正公告
    "http://www.fsggzy.cn/zfcg/zf_gzgg/zcgz_gq/zggz_nh/",  #更正公告
    "http://www.fsggzy.cn/zfcg/zf_gzgg/zcgz_gq/zggz_ss/",  #更正公告
    "http://www.fsggzy.cn/zfcg/zf_gzgg/zcgz_gq/zggz_gm/",  #更正公告
    "http://www.fsggzy.cn/zfcg/zf_gzgg/zcgz_gq/zggz_sd/",  #更正公告
    "http://www.fsggzy.cn/zfcg/zf_gzgg/zcgz_zjjg/",  #更正公告
    "http://www.fsggzy.cn/zfcg/zf_jggg/zf_jgsz/", #结果公示
    "http://www.fsggzy.cn/zfcg/zf_jggg/zcgz_gq/zgjg_cc/",  #结果公示
    "http://www.fsggzy.cn/zfcg/zf_jggg/zcgz_gq/zgjg_nh/",  #结果公示
    "http://www.fsggzy.cn/zfcg/zf_jggg/zcgz_gq/zgjg_ss/",  #结果公示
    #"http://www.fsggzy.cn/zfcg/zf_jggg/zcgz_gq/zgjg_gm/",  #结果公示
    "http://www.fsggzy.cn/zfcg/zf_jggg/zcgz_gq/zgjg_sd/",  #结果公示
    "http://www.fsggzy.cn/zfcg/zf_jggg/zcgz_zjjg/",  #结果公示
    "http://www.fsggzy.cn/zfcg/zf_zbxx/zf_zbsz/",  #中标信息
    "http://www.fsggzy.cn/zfcg/zf_zbxx/zfzbgq/zbxxcc/",  #中标信息
    "http://www.fsggzy.cn/zfcg/zf_zbxx/zfzbgq/zbxxnh/",  #中标信息
    "http://www.fsggzy.cn/zfcg/zf_zbxx/zfzbgq/zbxxss/",  #中标信息
    "http://www.fsggzy.cn/zfcg/zf_zbxx/zfzbgq/zbxxgm/",  #中标信息
    "http://www.fsggzy.cn/zfcg/zf_zbxx/zfzbgq/zbxxsd/",  #中标信息
    "http://www.fsggzy.cn/zfcg/zf_zbxx/zfzbxxzj/",  #中标信息
    "http://www.fsggzy.cn/gcjy/gc_zbxx/gc_zbsz/",  #招标公告
    "http://www.fsggzy.cn/gcjy/gc_zbxx/jygg_gq/gc_zbcc/",  #招标公告
    "http://www.fsggzy.cn/gcjy/gc_zbxx/jygg_gq/gc_zbnh/",  #招标公告
    "http://www.fsggzy.cn/gcjy/gc_zbxx/jygg_gq/gc_zbss/",  #招标公告
    "http://www.fsggzy.cn/gcjy/gc_zbxx/jygg_gq/gc_zbgm/",  #招标公告
    "http://www.fsggzy.cn/gcjy/gc_zbxx/jygg_gq/gc_zbsd/",  #招标公告
    "http://www.fsggzy.cn/gcjy/gc_zbxx1/gc_1zbsz/", #中标
    "http://www.fsggzy.cn/gcjy/gc_zbxx1/gczbgq/gc_1zbcc/",  #中标
    "http://www.fsggzy.cn/gcjy/gc_zbxx1/gczbgq/gc_1zbnh/",  #中标
    "http://www.fsggzy.cn/gcjy/gc_zbxx1/gczbgq/gc_1zbss/",  #中标
    "http://www.fsggzy.cn/gcjy/gc_zbxx1/gczbgq/gc_1zbgm/",  #中标
    "http://www.fsggzy.cn/gcjy/gc_zbxx1/gczbgq/gc_1zbsd/",  #中标
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
    "_list": {'pattern': "//div[@class='secondrightlistbox']//li",'type':'xpath', 'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"下一页", 'type': 'link_text', 'target': 'html', 'custom_func_name': ''},
    "_issue_time":{'pattern': "//span[@style='float:right']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

}

# 详情页模板
detail_pattern = {
    "sc": {'pattern': "//div[@class='contentrightlistbox2']", 'type': 'xpath', 'target': 'html', 'custom_func_name': ''},
    "title": {'pattern': "//div[@class='contenttitle2']//h3", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},

    # "pub_date": "//td/font[@color='#666666']/text()",
    # "pub_date_fmt": "%Y-%m-%d %H:%M:%S",
}


def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    item['region'] = u'广东-佛山'
    del item['web_title']


def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
    logger.debug(item['url'])
    # 停止翻页




def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
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
    logger.debug('%s   %s', item['title'], item['_issue_time'])
    item['issue_time'] = int(time.mktime(time.strptime(item['_issue_time'], '[%Y-%m-%d]')))
    if len(item['sc']) != 0:
        item['is_get'] = 1
    else:
        item['is_get'] = 0