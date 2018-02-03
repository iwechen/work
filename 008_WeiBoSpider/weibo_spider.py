#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import requests
import re
from lxml import etree
import redis
import json
import logging
from cookies import Cookies
from config import PROXY_POOL

class WeiBoSpider(object):
    def __init__(self,redis,cookies_dict):
        self.cookie_dict = cookies_dict
        self.redis = redis
        self.flag = True

    def send_request(self):
        timetamp = str(int((time.time())*1000))
        params = {'page':'38','key':'新疆~哈密','type':'shishi','_t':'0','__rnd':timetamp}
        url = "http://s.weibo.com/ajax/morestatus?"
        proxies = PROXY_POOL[0]
        # proxies = {"http":"13273023501:wpnoft3h@120.28.218.32:16819"} 
        for user_id,cookies in self.cookie_dict.items():
            cookies = str(cookies,'utf-8')
            cookies = re.sub(r"'",'"',cookies)
            cookies =json.loads(cookies)
            response = requests.get(url = url,params = params,proxies = proxies,cookies = cookies).content.decode('utf-8')

            if self.flag == True:
                self.collect_data(response)
            else:
                self.redis.hdel('cookie',user_id)
                continue

    def collect_data(self,response):
        print(response)
        try:
            response = re.search(r'(<div .*/div>)',response,re.S).group(1)
            
            # 1.用户id
            # https://m.weibo.cn/u/5821636650
            # https://m.weibo.cn/api/container/getIndex?type=uid&value=5821636650
            user_id = re.findall(r'mid=.*?uid=(\d{10})\\"',response)
            print(len(user_id),user_id)
            response = re.findall(r'<div class=\\"con\\">(.*?)\\n\s+<\\/div>\\n\s+<\\/div>\\n<\\/div>\\n',response,re.S)
            # p标签
            p_li = [re.findall(r'<p.*?>(.*?)<\\/p>',i,re.S) for i in response]
            # 2.用户名
            # p = re.findall(r'<p.*?>(.*?)<\\/p>',i,re.S)
            # ret = re.sub(r'\\n\s+|<a.*?>.*<\\/a>','',p[0])
            # res = bytes(ret, encoding = "utf8")
            # name = res.decode('unicode_escape')
            username = [bytes(re.sub(r'\\n\s+|<a.*?>.*<\\/a>','',p0[0]), encoding = "utf8").decode('unicode_escape') for p0 in p_li]
            print(len(username),username)
            # 3.发布时间
            # ret = re.match(r'<span>(.*?)<\\/span>',p1[1]).group(1)
            # res = bytes(ret, encoding = "utf8")
            # name = res.decode('unicode_escape')
            datetime = [bytes(re.match(r'<span>(.*?)<\\/span>',p1[1]).group(1), encoding = "utf8").decode('unicode_escape') for p1 in p_li]
            print(len(datetime),datetime)
            # 4.发布内容
            # strs = bytes(p2[2], encoding = "utf8").decode('unicode_escape')
            # html = etree.HTML(strs)
            # da = html.xpath('string(.)')
            # re.sub(r'\s\\u200b|\\n','',da)
            contents = [re.sub(r'\s\u200b|\n','',etree.HTML(bytes(p2[2], encoding = "utf8").decode('unicode_escape')).xpath('string(.)'))for p2 in p_li]
            # print(len(contents),contents)
            for i in contents:
                print(i+'\n')
            if all(user_id):
                raise Exception
        except:
            self.flag = False
        else:
            self.flag = True

    def main(self):
        self.send_request()
        
if __name__ == '__main__':
    redis = redis.Redis(host='127.0.0.1',port=6379, db=1)
    cookie_dict = redis.hgetall('cookie')
    # 判断cookie 池库存
    if len(cookie_dict) < 1:
        logging.warning('Cookies pool low stocks')
        logging.warning('Start stockpiling!')
        cookies = Cookies()
        cookies.main()

    weibo = WeiBoSpider(redis,cookie_dict)
    weibo.main()

