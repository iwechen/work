import requests
import json
import time
import datetime
import pymongo

class DateTime(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1',port=27017)

        self.db = self.client['XueQiu']

        self.collection = self.db['xueqiu_datetime']

    def main(self,symbol):
        try:
            cookies = {
                'device_id': '0279b10c4c80dea605e612e10396683a',
                '__utmz': '1.1516771804.1.1.utmcsr=(direct)^|utmccn=(direct)^|utmcmd=(none)',
                's': 'fb1215dia5',
                'xq_a_token': '3836bb2166e0e438ade26542b67832432e93209b',
                'xqat': '3836bb2166e0e438ade26542b67832432e93209b',
                'xq_r_token': '43cfe05ee4d224d657f3866da9fc06c5e66b35f7',
                'xq_token_expire': 'Mon^%^20Mar^%^2026^%^202018^%^2020^%^3A53^%^3A30^%^20GMT^%^2B0800^%^20(CST)',
                'xq_is_login': '1',
                'u': '1058215398',
                'bid': '54cdece1f2daa5054574b5263766caff_je8ignqc',
                'aliyungf_tc': 'AQAAAF5fZQlHxAkAZQv3diR/lQ+njB13',
                'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1519908742,1519908985,1519973511,1519973937',
                '__utmc': '1',
                '__utma': '1.1573219580.1516771804.1519997510.1520001483.7',
                '__utmt': '1',
                'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1520001530',
                '__utmb': '1.2.10.1520001483',
            }

            headers = {
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
                'Accept': '*/*',
                'Referer': 'https://xueqiu.com/S/SZ300001',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
            }

            params = {
                'symbol':symbol,
                'period':'all'
                # 'period':'6m'
                # 'one_min':'1'
            }

            response = requests.get('https://xueqiu.com/stock/forchart/stocklist.json', headers=headers, params=params, cookies=cookies).content.decode('utf-8')

            ret = json.loads(response)
            data_list = []
            symbol = ret['stock']['symbol']
            print(symbol)
            for i in ret['chartlist']:
                print(i)
                data_dict = {}
                timestamp = str(i['timestamp'])[:10]
                time_local = time.localtime(int(timestamp))
                symbol = ret['stock']['symbol']
                timestamp = time.strftime("%Y-%m-%d",time_local)
                timestamp = datetime.datetime.strptime(timestamp,'%Y-%m-%d')
                data = [i for i in self.collection.find({'symbol':symbol,'timestamp':timestamp})]
                # print(type(timestamp))
                if data !=[]:
                    print('---------------存在----------------------')
                    continue
                
                # 股票代码
                data_dict['symbol'] = symbol
                # 时间
                data_dict['timestamp'] = timestamp
                # 均价
                data_dict['avg_price'] = i['avg_price']
                # 当前价
                data_dict['current'] = i['current']
                # 成交量 
                data_dict['volume'] = i['volume']
                data_list.append(data_dict)
                # print(data_list)
        except Exception as e:
            print(e)
        else:
            print(data_list)
            # pass
            self.save_to_mongo(data_list)
        
    def save_to_mongo(self,data_list):
        try:
            self.collection.insert(data_list)
            print('successful')
        except:
            print('default')

if __name__=="__main__":
    dt = DateTime()
    for i in range(300731,3000741):
        symbol = 'SZ'+str(i)
        
        dt.main(symbol)
