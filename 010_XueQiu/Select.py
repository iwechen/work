import pymongo
import re


class SelectMongo(object):
    def __init__(self,symbol,timestamp):
        self.client = pymongo.MongoClient(host = '127.0.0.1',port = 27017)
        self.db = self.client.XueQiu
        self.collection = self.db['xueqiu_datetime']
        self.symbol = symbol
        self.timestamp = timestamp

    def find_mongo(self):
        while True:
            data = [i for i in self.collection.find({'symbol':self.symbol,'dt':self.timestamp})]
            if data == []:
                datetime_li = self.timestamp.split('-')
                # print(datetime_li)
                day = int(datetime_li[2])
                month = int(datetime_li[1])
                year = int(datetime_li[0])
                if day <=30:
                    day += 1
                    if len(str(day))<2:
                        day = '0'+ str(day)
                    if len(str(month))<2:
                        month = '0'+ str(month)
                    self.timestamp = str(year)+'-'+str(month)+'-'+str(day)
                    continue
                else:
                    if month >= 12:
                        year += 1
                        month = 0
                    month +=1
                    day = 1
                    if len(str(month))<2:
                        month = '0'+str(month)
                    if len(str(day))<2:
                        day = '0'+str(day)
                    self.timestamp = str(year)+'-'+str(month)+'-'+str(day)
                    day = int(day) 
                    day += 1
                    continue
            else:
                return data

    def main(self):
        data = self.find_mongo()
        return data

if __name__=="__main__":
    symbol = 'SZ300001'
    timestamp = '2017-09-05'
    sm = SelectMongo(symbol,timestamp)
    a = sm.main()
    print(a)









