#coding=utf-8
import time
import requests
import re
from lxml import etree


def process_request():

    cookies = {
        'SINAGLOBAL': '1531888812599.662.1514185346553',
        'login_sid_t': '5d0c3df20df6969cd559a9f9b1107118',
        'cross_origin_proto': 'SSL',
        '_s_tentry': 'www.baidu.com',
        'Apache': '9879396964238.555.1517276163701',
        'ULV': '1517276163713:6:3:1:9879396964238.555.1517276163701:1515465112553',
        'SWBSSL': 'usrmdinst_6',
        'SWB': 'usrmdinst_7',
        'UOR': ',,login.sina.com.cn',
        'un': '15389378206',
        'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W58fek8FHHKdj_WcXuPOfxA5JpX5K2hUgL.Fo-NSK.X1K-XS0q2dJLoI0eLxK-L12qL12eLxK.LBo2LB.eLxK-LBo5L12qLxK-LBKBLB-2LxK.L1KnLBoSkeoBESh.t',
        'ALF': '1548832322',
        'SSOLoginState': '1517296322',
        'SCF': 'AjXlxvkVQwWjkRYO13oa5v9O0HiO8bSJV8MbmXcObCKHQv4at8FA_bl4v-2OC_hY4jx25lXYm6lJ36x3c-UnPjk.',
        'SUB': '_2A253dGqTDeRhGeNJ7lsV-SvIzDqIHXVUANtbrDV8PUNbmtANLW2skW9NS6YrshECuDmton0Pb2MA0YuTEpirjnER',
        'SUHB': '0k1CYDXqJYiCmM',
        'wvr': '6',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Referer': 'http://s.weibo.com/weibo/^%^25E5^%^2593^%^2588^%^25E5^%^25AF^%^2586',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }
    timetamp = str(int((time.time())*1000))
    params = {'page':'2','key':'哈密','hasvideo':'','xsort':'social','type':'shishi','_t':'0','__rnd':timetamp}

    url = "http://s.weibo.com/ajax/morestatus?"
    proxies = { "http":'http://120.77.35.48:8899'}
    response = requests.get(url = url,proxies = proxies,params = params,headers=headers,cookies=cookies).content.decode('utf-8')
    response = re.search(r'(<div .*/div>)',response,re.S).group(1)
    response = re.findall(r'<div class=\\"con\\">(.*?)\\n\s+<\\/div>\\n\s+<\\/div>\\n<\\/div>\\n',response,re.S)
    for i in response:
        p = re.findall(r'<p.*?>(.*?)<\\/p>',i,re.S)
        ret = re.sub(r'\\n\s+|<a.*?>.*<\\/a>','',p[0])
        res = bytes(ret, encoding = "utf8")
        name = res.decode('unicode_escape')
        print(name)


    # html = etree.HTML(response)
    # ret = html.xpath('//<div lass=\"clearfix\">')

    # print(ret)

    # print(type(response))
    # a = response.encode('unicode')
    # print(a)
    # res = b'%s'%res
    # res = bytes(response, encoding = "utf8")
    # print(type(res))
    # print(res.decode('unicode_escape'))



    
def main():
    process_request()


if __name__ == '__main__':
    main()

