#coding:utf-8
'''
Created on 2018年3月2日
@author: chenwei
Email:iwechen123@gmail.com
'''
import requests
import json
import time
import pymongo
from Select import SelectMongo
from datetime import datetime


class XueQiu(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = self.client['XueQiu']
        self.collection = self.db['data']
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        self.cookies = {
            'device_id':
            '0279b10c4c80dea605e612e10396683a',
            '__utmz':
            '1.1516771804.1.1.utmcsr=(direct)^|utmccn=(direct)^|utmcmd=(none)',
            's':
            'fb1215dia5',
            'xq_a_token':
            '3836bb2166e0e438ade26542b67832432e93209b',
            'xqat':
            '3836bb2166e0e438ade26542b67832432e93209b',
            'xq_r_token':
            '43cfe05ee4d224d657f3866da9fc06c5e66b35f7',
            'xq_token_expire':
            'Mon^%^20Mar^%^2026^%^202018^%^2020^%^3A53^%^3A30^%^20GMT^%^2B0800^%^20(CST)',
            'xq_is_login':
            '1',
            'u':
            '1058215398',
            'bid':
            '54cdece1f2daa5054574b5263766caff_je8ignqc',
            'aliyungf_tc':
            'AQAAAF5fZQlHxAkAZQv3diR/lQ+njB13',
            'Hm_lvt_1db88642e346389874251b5a1eded6e3':
            '1519908742,1519908985,1519973511,1519973937',
            '__utma':
            '1.1573219580.1516771804.1519912827.1519973941.4',
            '__utmc':
            '1',
            'Hm_lpvt_1db88642e346389874251b5a1eded6e3':
            '1519973999',
            '__utmb':
            '1.3.10.1519973941',
        }


    def symbol_name(self,symbol):
        url = 'https://xueqiu.com/v4/stock/quote.json?'
        params = {'code':symbol}
        response = requests.get(url = url,params=params,headers = self.headers,cookies=self.cookies).content.decode('utf-8')

        ret = json.loads(response)
        # print(ret)
        name = ret[symbol]['name']
        return name

    def sned_req(self,symbol,page):



        headers = {
            # 'Accept-Encoding':'gzip, deflate, br',
            # 'Accept-Language':'zh-CN,zh;q=0.9',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            # 'Accept':'*/*',
            # 'Referer':'https://xueqiu.com/S/SZ300001',
            # 'X-Requested-With':'XMLHttpRequest',
            # 'Connection':'keep-alive'
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

        response = requests.get(
            'https://xueqiu.com/statuses/search.json?',headers=self.headers,params=params,cookies=self.cookies).content.decode('utf-8')
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
                if (timestamp == '2018-03-16')or(timestamp == '2018-03-17'):
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
                # 当前价
                current = a['current']
                symbol_dic['current'] = current
                # 成交量
                volume = a['volume']
                symbol_dic['volume'] = volume
                # 后五日走势
                next_day_current = a['next_day_current']
                symbol_dic['next_day_current'] = next_day_current
                # 股票代码
                symbol_dic['symbol'] = symbol
                # 股票名称
                name = self.symbol_name(symbol)
                symbol_dic['name'] = name

                symbol_li.append(symbol_dic)

            except Exception as e:
                print(e)
            else:
                # print(symbol_li)
                self.save_to_mongo(symbol_li)

    def save_to_mongo(self,data_li):
        try:
            self.collection.insert(data_li)
            print('successful')
        except:
            print('default')

    def main(self):
        for i in range(300001,3000741):
            symbol = 'SZ'+str(i)
            # symbol = 'SZ300002'
            print('股票代码: %s'%symbol)
            for page in range(1,101):
                print('第 %d 页'%page)
                self.sned_req(symbol,page)

if __name__ == '__main__':
    xq = XueQiu()
    xq.main()
