#coding:utf-8
'''
Created on 2018年4月3日
@author: chenwei
Email:iwechen123@gmail.com
'''

import requests
import time
import json
from six.moves import queue
import threading
import urllib.parse
import random
import pymongo

class BiHu(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = self.client['bihu']
        self.collection = self.db['data']

        self.db_proxy = self.client['Proxy']
        self.collection_proxy = self.db_proxy['proxy_daili']

        self.headers = {
            'Origin': 'https://m.bihu.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6',
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            # 'User-Agent':'baiduspider',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Accept': '*/*',
            # 'Referer': 'https://bihu.com/?category=hots&code=BTC',
            'Connection': 'keep-alive',
            }

        self._id_queue = queue.Queue(10)
        self._response_queue = queue.Queue(10)
        self._data_queue = queue.Queue(20)

        self._proxies = None

    def load_page(self,url,data):
        s = requests.Session()
        proxies = {'http':'http://120.77.35.48:8899'}
        # proxies = None

        url1 = 'http://httpbin.org/ip'
        a = requests.get(url=url1,proxies = proxies).content.decode('utf-8')
        print(a)
        response = s.post(url = url,data=data, proxies=proxies,headers=self.headers,verify=False)

        print(response.cookies)
        if response.status_code == 200:
            return response.json()
        else:
            return

    def load_id(self):
        while True:
            uid = self._id_queue.get()
            url = 'https://be02.bihu.com/bihube-pc/api/content/show/getArticle'
            data = {
                'userId':'',
                'accessToken':'',
                'artId':uid
            }
            print(uid)
            response = self.load_page(url,data)
            print(response)

    def init(self):
        t1 = threading.Thread(target = self.load_id)
        t1.start()

        # t2 = threading.Thread(target = self.collection_data)
        # t2.start()

        # t3 = threading.Thread(target = self.save_to_mongo)
        # t3.start()


    def run(self):
        self.init()
        ids = 8628
        end = 10000
        while True:
            if ids < end:
                aid = [aid for aid in self.collection.find({'id':ids})]
                if aid ==[]:
                    self._id_queue.put(ids)
                    ids += 1
                    time.sleep(2)
                    continue
                else:
                    ids += 1
                    continue
            else:
                break

    def main(self):
        self.run()

if __name__=='__main__':
    bihu = BiHu()
    bihu.main()