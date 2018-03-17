import pymongo
import re
from datetime import datetime, timedelta, date, time


class SelectMongo(object):
    def __init__(self,symbol,timestamp):
        self.client = pymongo.MongoClient(host = '127.0.0.1',port = 27017)
        self.db = self.client.XueQiu
        self.collection = self.db['xueqiu_datetime']
        self.symbol = symbol
        self.timestamp = timestamp

        self.today = {}


    def find_mongo(self):
        temp = self.timestamp
        today = [i for i in self.collection.find({'symbol':self.symbol,'timestamp':temp})]
        # 当日数据空，循环查找均值
        if today == []:
            while True:
                # 1,查询当日数据
                max_data = [i for i in self.collection.find({'symbol':self.symbol,'timestamp':temp})]
                if max_data == []:
                    # print(temp)
                    temp = temp + timedelta(days=1)
                    continue
                # 2,查询后五日数据
                else:
                    temp = self.timestamp
                    # print(max_data)
                    break
            # 开始最小值
            while True:
                # 1,查询当日数据
                min_data = [i for i in self.collection.find({'symbol':self.symbol,'timestamp':temp})]
                if min_data == []:
                    # print(temp)
                    temp = temp - timedelta(days=1)
                    continue
                # 2,查询后五日数据
                else:
                    temp = self.timestamp
                    # print(min_data)
                    break
            # 均价
            avg_current = (max_data[0]['current'] + min_data[0]['current'])/2
            self.today = min_data[0]
            self.today['current'] = avg_current
            self.today['timestamp'] = self.timestamp
            self.today['next_day_current'] = max_data[0]['current']

            return self.today

        # 当日有数据，
        else:
            self.today = today[0]
            while True:
                temp = temp + timedelta(days=1)
                max_data = [i for i in self.collection.find({'symbol':self.symbol,'timestamp':temp})]
                if max_data == []:
                    continue
                # 2,查询后五日数据
                else:
                    self.today['next_day_current'] = max_data[0]['current']
                    break
            return self.today

    def run(self):
        data = self.find_mongo()
        return data

    def main(self):
        data = self.find_mongo()
        return data

if __name__=="__main__":
    symbol = 'SZ300001'
    timestamp = '2013-04-16'
    timestamp = datetime.strptime(timestamp,'%Y-%m-%d')
    sm = SelectMongo(symbol,timestamp)
    a = sm.main()
    print(a)









