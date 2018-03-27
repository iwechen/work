#coding:utf-8
'''
Created on 2018年3月2日
@author: chenwei
Email:iwechen123@gmail.com
'''
import requests
import threading
import json
import time
import pymongo
import hashlib
from Select import SelectMongo
from datetime import datetime
from six.moves import queue


class XueQiu(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = self.client['XueQiu']
        self.collection = self.db['data']

        self._error_task_queue = queue.Queue(1000)
        self._error_task_set = set()
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        self.cookies = {
            'aliyungf_tc': 'AQAAAKtL+Wx7HAUAs63zdPSJ2jGC8jrG',
            'xq_a_token.sig': 'aaTVFAX9sVcWtOiu-5L8dL-p40k',
            'xq_r_token.sig': 'rEvIjgpbifr6Q_Cxwx7bjvarJG0',
            'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1521288871',
            'device_id': 'ce0a59849606ef4e2a7e215507d44300',
            's': 'ek19tty35r',
            'xq_a_token': '3836bb2166e0e438ade26542b67832432e93209b',
            'xqat': '3836bb2166e0e438ade26542b67832432e93209b',
            'xq_r_token': '43cfe05ee4d224d657f3866da9fc06c5e66b35f7',
            'xq_token_expire': 'Wed%20Apr%2011%202018%2020%3A14%3A52%20GMT%2B0800%20(CST)',
            'xq_is_login': '1',
            'u': '1058215398',
            'bid': '54cdece1f2daa5054574b5263766caff_jevc4mgf',
            'snbim_minify': 'true',
            '__utma': '1.1464544356.1521288913.1521288913.1521288913.1',
            '__utmc': '1',
            '__utmz': '1.1521288913.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            '__utmt': '1',
            '__utmb': '1.3.10.1521288913',
            'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1521288977',
            }



    def symbol_name(self,symbol):
        url = 'https://xueqiu.com/v4/stock/quote.json?'
        params = {'code':symbol}
        response = requests.get(url = url,params=params,headers = self.headers,cookies=self.cookies).content.decode('utf-8')

        ret = json.loads(response)
        # print(ret)
        name = ret[symbol]['name']
        return name

    def hash_to_md5(self,sign_str):
        '''
        接收：接收待加密的字符串
        返回：sign签名字符串
        '''
        # 创建MD5对象
        m= hashlib.md5()
        sign_str = sign_str.encode('utf-8')
        # 加密字符串  
        m.update(sign_str) 
        sign = m.hexdigest() 
        return sign

    def sned_req(self,symbol,page):
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'https://xueqiu.com/S/SZ300001',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }

        params = {
            'count': '10',
            'comment': '0',
            'symbol': symbol,
            'hl': '0',
            'source':'all',
            'sort':'',
            'page':str(page),
            'q':''
        }
        proxies = {'http':'http://120.77.35.48:8899'}
        response = requests.get(
            'https://xueqiu.com/statuses/search.json?',proxies = proxies,headers=self.headers,params=params,cookies=self.cookies).content.decode('utf-8')
        # print(response)
        # print(response.url)
        ret = json.loads(response)
        for i in range(10):
            symbol_li = []
            symbol_dic = {}
            try:
                # 用户ID
                user_id = ret['list'][i]['user_id']
                symbol_dic['user_id'] = user_id
                # 发帖时间
                timestamp = ret['list'][i]['created_at']
                timestamp = str(timestamp)[:10]
                time_local = time.localtime(int(timestamp))
                timestamp = time.strftime("%Y-%m-%d",time_local)
                if (timestamp == '2018-03-16')or(timestamp == '2018-03-17')or(timestamp == '2018-03-18')or(timestamp == '2018-03-19')or(timestamp == '2018-03-20')or(timestamp == '2018-03-21')or(timestamp == '2018-03-22')or(timestamp == '2018-03-23')or(timestamp == '2018-03-24')or(timestamp == '2018-03-25')or(timestamp == '2018-03-26'):
                    continue

                symbol_dic['timestamp'] = timestamp
                # 发帖内容
                text = ret['list'][i]['text']
                symbol_dic['text'] = text
                # 粉丝数
                followers_count = ret['list'][i]['user']['followers_count']
                symbol_dic['followers_count'] = followers_count
                # 关注量
                friends_count = ret['list'][i]['user']['friends_count']
                symbol_dic['friends_count'] = friends_count
                # 帖子量
                status_count = ret['list'][i]['user']['status_count']
                symbol_dic['status_count'] = status_count
                # 评论量
                reply_count = ret['list'][i]['reply_count']
                symbol_dic['reply_count'] = reply_count
                # 点赞量
                like_count = ret['list'][i]['like_count']
                symbol_dic['like_count'] = like_count
                # 转发量
                retweet_count = ret['list'][i]['retweet_count']
                symbol_dic['retweet_count'] = retweet_count
                timestamp = datetime.strptime(timestamp,'%Y-%m-%d')
                sm = SelectMongo(symbol,timestamp)
                a = sm.run()
                current = a['current']
                symbol_dic['current'] = current
                # 成交量
                volume = a['volume']
                symbol_dic['volume'] = volume
                # 后五日走势
                next_day_current = a['next_day_current']
                symbol_dic['next_day_current'] = next_day_current
                # break
                # 股票代码
                symbol_dic['symbol'] = symbol
                # 股票名称
                name = self.symbol_name(symbol)
                symbol_dic['name'] = name

                symbol_li.append(symbol_dic)

                sign_str = str(user_id) + text + str(reply_count) + symbol + str(timestamp)

                sign = self.hash_to_md5(sign_str)

                symbol_dic['sign'] = sign
            except Exception as e:
                print(e)
            else:
                if [i for i in self.collection.find({'sign':sign})] != []:
                    time.sleep(3)
                    break
                # print(symbol_li)
                self.save_to_mongo(symbol_li)

    def save_to_mongo(self,data_li):
        try:
            self.collection.insert(data_li)
            print('successful')
        except:
            print('default')

    def error_loop(self):
        count = 0
        while True:
            print('轮流 %d 转'%count)
            page,symbol = self._error_task_queue.get()
            print(page)
            print(symbol)
            # for page,symbol in error_li:
            self.sned_req(symbol,page)
            time.sleep(2)
            count += 1

    def run1(self,start):
        for i in range(start,300741):
            symbol = 'SZ'+str(i)
            # symbol = 'SZ300002'
            print('股票代码: %s'%symbol)
            for page in range(1,25):
                print('第 %d 页'%page)
                # time.sleep(1)
                self.sned_req(symbol,page)
                time.sleep(1)

    def run2(self,start):
        for i in range(start,300741):
            symbol = 'SZ'+str(i)
            # symbol = 'SZ300002'
            print('股票代码: %s'%symbol)
            for page in range(25,50):
                print('第 %d 页'%page)
                self.sned_req(symbol,page)
                # time.sleep(1)

    def run3(self,start):
        for i in range(start,300741):
            symbol = 'SZ'+str(i)
            # symbol = 'SZ300002'
            print('股票代码: %s'%symbol)
            for page in range(50,75):
                print('第 %d 页'%page)
                self.sned_req(symbol,page)
                # time.sleep(1)

    def run4(self,start):
        for i in range(start,300741):
            symbol = 'SZ'+str(i)
            # symbol = 'SZ300002'
            print('股票代码: %s'%symbol)
            for page in range(75,101):
                print('第 %d 页'%page)
                self.sned_req(symbol,page)
                # time.sleep(1)

    def main(self):
        start = 300491
        t1 = threading.Thread(target=self.run1,args = (start,))
        t1.start()
        t2 = threading.Thread(target=self.run2,args = (start,))
        t2.start()
        t3 = threading.Thread(target=self.run3,args = (start,))
        t3.start()
        t4 = threading.Thread(target=self.run4,args = (start,))
        t4.start()

        # t5 = threading.Thread(target=self.error_loop)
        # t5.start()

            # time.sleep(5)

if __name__ == '__main__':
    xq = XueQiu()
    xq.main()
