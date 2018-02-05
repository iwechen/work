#coding=utf-8
import time
import requests
import re
from lxml import etree


def process_request():

    cookies = {
        'SINAGLOBAL': '1531888812599.662.1514185346553',
        'un': '15389378206',
        'wvr': '6',
        'ALF': '1548899582',
        'SSOLoginState': '1517363582',
        'SCF': 'AjXlxvkVQwWjkRYO13oa5v9O0HiO8bSJV8MbmXcObCKHDrYVcphwYeP1IQJNAfxLp7gIbj-1fN-HMR06fQZvbCg.',
        'SUB': '_2A253dVEuDeRhGeNJ7lsV-SvIzDqIHXVUA8XmrDV8PUNbmtANLRDmkW9NS6YrshW6xZnXBqkLhENhw2R-fp8KobCr',
        'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W58fek8FHHKdj_WcXuPOfxA5JpX5KzhUgL.Fo-NSK.X1K-XS0q2dJLoI0eLxK-L12qL12eLxK.LBo2LB.eLxK-LBo5L12qLxK-LBKBLB-2LxK.L1KnLBoSkeoBESh.t',
        'SUHB': '0tKqvI_DJpZyB5',
        '_s_tentry': 'login.sina.com.cn',
        'UOR': ',,www.baidu.com',
        'Apache': '572483790754.7565.1517363586707',
        'ULV': '1517363586759:7:4:2:572483790754.7565.1517363586707:1517276163713',
        'SWBSSL': 'usrmdinst_8',
        'SWB': 'usrmdinst_15',
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
    params = {'page':'38','key':'新疆~哈密','type':'shishi','_t':'0','__rnd':timetamp}

    url = "http://s.weibo.com/ajax/morestatus?"
    proxies = { "http":'http://120.77.35.48:8899'}
    response = requests.get(url = url,proxies = proxies,params = params,headers=headers,cookies=cookies).content.decode('utf-8')
    response = re.search(r'(<div .*/div>)',response,re.S).group(1)
    
    # 1.用户id
    # https://m.weibo.cn/u/5821636650
    user_id = re.findall(r'mid=.*?uid=(\d{10})\\"',response)
    print(len(user_id),user_id)
    response = re.findall(r'<div class=\\"con\\">(.*?)\\n\s+<\\/div>\\n\s+<\\/div>\\n<\\/div>\\n',response,re.S)
    # p标签
    p_li = [re.findall(r'<p.*?>(.*?)<\\/p>',i,re.S) for i in response]
    # 2.用户名
    username = [bytes(re.sub(r'\\n\s+|<a.*?>.*<\\/a>','',p0[0]), encoding = "utf8").decode('unicode_escape') for p0 in p_li]
    print(len(username),username)
    # 3.发布时间
    datetime = [bytes(re.match(r'<span>(.*?)<\\/span>',p1[1]).group(1), encoding = "utf8").decode('unicode_escape') for p1 in p_li]
    print(len(datetime),datetime)
    # 4.发布内容
    contents = [re.sub(r'\s\u200b|\n','',etree.HTML(bytes(p2[2], encoding = "utf8").decode('unicode_escape')).xpath('string(.)'))for p2 in p_li]
    print(len(contents),contents)

def main():
    process_request()


if __name__ == '__main__':
    main()

