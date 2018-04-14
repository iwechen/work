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
import os
import sys
import signal
import logging
logger = logging.getLogger(__name__)

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
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6',
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'User-Agent':'baiduspider',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Accept': '*/*',
            # 'Referer': 'https://bihu.com/?category=hots&code=BTC',
            'Connection': 'keep-alive',
            # 'Host': 'bihu2001.oss-cn-shanghai.aliyuncs.com',
            # 'Host': 'be02.bihu.com',
            # 'Set-Cookie': 'acw_tc=AQAAAL6XlxrRsAIAZa+R25eKAjTxJKW7; Path=/; HttpOnly',
            # 'cookie': 'pgv_pvi=8890480640; pt2gguin=o1639663168; RK=07LY5hOQUa; ptcz=1680aa32aec4454a020ae7b149f1d6274145f87098d6a1212e486a18f336d1fb; pgv_pvid=1016131917; tvfe_boss_uuid=20ab809534b8633a; ptui_loginuin=18513117286; o_cookie=1639663168',
        }

        self._id_queue = queue.Queue(10)
        self._response_queue = queue.Queue(10)
        self._data_queue = queue.Queue(20)

    def load_page(self,url,data):
        s = requests.Session()
        proxies = None
        response = s.post(url = url,data=data, proxies=proxies,headers=self.headers,verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            return

    def kill(self,pid):
        try:
            a = os.kill(pid, signal.SIGKILL)
            print('已杀死pid为%s的进程,返回值是:%s',(pid,a ))
        except OSError as e:
            print('没有如此进程!!!')

    def load_id(self):
        while True:
            uid = self._id_queue.get()
            url = 'https://be02.bihu.com/bihube-pc/api/content/show/getArticle'
            data = {
                # 'userId':'',
                # 'accessToken':'',
                'artId':uid
            }
            print(uid)
            response = self.load_page(url,data)
            try:
                if response['res']==0:
                    pid = os.getpid()
                    self.kill(pid)
                    self._id_queue.put(uid)
                    
                elif response['res']==1:
                    self._response_queue.put(response)
                else:
                    print('该帖已删除!')
            except:
                pass
            else:
                with open('id.txt','w') as f:
                    f.write(str(uid))

    def collection_data(self):
        while True:
            response = self._response_queue.get()
            try:
                c = response['data']['content']
                content = urllib.parse.unquote(c)
            except Exception as e:
                print(e)
                print(response)   
            else:
                response['data']['content'] =  content
                data = response['data']
                self._data_queue.put(data)       

    def save_to_mongo(self):
        while True:
            data = self._data_queue.get()
            try:
                self.collection.insert(data)
                print('successful')
            except:
                print('default')

    def init(self):
        t1 = threading.Thread(target = self.load_id)
        t1.start()

        t2 = threading.Thread(target = self.collection_data)
        t2.start()

        t3 = threading.Thread(target = self.save_to_mongo)
        t3.start()

    def run(self):
        self.init()
        # code_li = ['BTC','CYBEX','DEW','ENG','EOS','ETH','KEY','LRC','MKR','NEO']
        code_li = ['ONT','VEN','安全资产','百咖说','币圈八卦','大咖访谈','行情解读','精链币答','LAUNCH','通证经济','挖矿','小白入门','项目分析','知识库']
        for code in code_li:
            count = 1
            while True:
                # time.sleep(0.3)
                data = {
                    'code':code,
                    'pageNum':count
                    }
                count +=1
                url = 'https://be02.bihu.com/bihube-pc/api/content/show/hotArtList'
                response = self.load_page(url,data)
                try:
                    ids = response['data']['list']
                except Exception as e:
                    # print(e)
                    # print(response)
                    proxies_li = [proxie for proxie  in self.collection_proxy.find({'count':3})]
                    # print(proxies_li)
                    self._proxies = proxies_li[random.randint(0,len(proxies_li)-1)]
                    # print(self._proxies)
                else:
                    if len(ids)<20:
                        break
                    id_li = [ i['id'] for i in ids]

                    for ids in id_li:
                        aid = [aid for aid in self.collection.find({'id':ids})]
                        if aid ==[]:
                            self._id_queue.put(ids)
                        else:
                            break

    def add_id_run(self):
        self.init()
        with open('id.txt','r') as f:
            ids = f.read()
        ids = int(ids)
        end = 3000000
        while True:
            if ids < end:
                aid = [aid for aid in self.collection.find({'id':ids})]
                if aid ==[]:
                    self._id_queue.put(ids)
                    ids += 1
                    time.sleep(0)
                    continue
                else:
                    ids += 1
                    continue
            else:
                break

    def main(self):
        self.add_id_run()
        

if __name__=='__main__':
    bihu = BiHu()
    bihu.main()