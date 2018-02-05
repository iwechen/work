# -*-coding:utf-8-*-
import pymongo
import time
import threading
import requests
from multiprocessing import Process
from daili_spider import Proxy_Spider

class Check_Ip(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host = '127.0.0.1',port = 27017)
        self.db = self.client.Proxy
        self.collection = self.db.proxy_daili

    def send_check(self,_id,count,proxy_temp):
        url = "http://ip.chinaz.com/getip.aspx"
        try:
            res = requests.get(url,proxies=proxy_temp,timeout=5).content.decode('utf-8')
            # print(res)
        except Exception as e:
            # print(e)
            if count < -2: 
                count = count
            else:
                count -= 1
            # print(e)
            self.collection.update({'_id': _id}, {"$set" :{"count": count}})
        else:
            # print(proxy_temp)
            if count > 2: 
                count = count
            else:
                count += 1
            self.collection.update({'_id': _id}, {"$set" :{"count": count}})

    def check_proxy(self,rec):
        mip_li = [mip for mip in self.collection.find({"count":rec})]
        for mip in mip_li:
            ip = mip['ip']
            _id = mip['_id']
            count = mip['count']
            proxy_host = 'http://'+ip

            proxy_temp = {"http":proxy_host}

            t1 = threading.Thread(target = self.send_check,args=(_id,count,proxy_temp))
            t1.start()
        t1.join()

    def start_check(self):
        for i in range(-3,4):
            print('No%d-CHECKED-------------- 正在验证集合%d中---------------'%(i+4,i))
            length = len([mip for mip in self.collection.find({"count":i})])
            print('本次验证集合 %d个'%length)
            if length==0:
                print('当前集合为空，自动跳转到下一层验证\n')
                continue
            self.check_proxy(i)
            if i < 3:
                print('本次验证有效代理%d个'%len([mip for mip in self.collection.find({"count":(i+1)})]))
            else:
                print('本次验证有效代理%d个\n'%len([mip for mip in self.collection.find({"count":i})]))
                break
            time.sleep(5)

    def start_spider(self):
        gip_li = [gip for gip in self.collection.find({'count':3})]
        print('-SPIDER----------------当前有效代理数量：%d-----------------\n'%len(gip_li))
        if len(gip_li)<=200:
            print('-SPIDER----------------代理尺库存代理不足，开始爬取-----------------\n')
            a = Proxy_Spider()
            a.main()
        print('新增代理:%d\n'%len([mip for mip in self.collection.find({"count":0})]))
        print('获取完毕！准备验证中....\n')
        time.sleep(100)
        print('开始验证！')


    # def output(self):
    #     ip_list = 

    def main(self):
        while True:
            self.start_check()
            time.sleep(20)
            self.start_spider()
            time.sleep(20)

if __name__ == '__main__':
    check_ip = Check_Ip()
    check_ip.main()
  



