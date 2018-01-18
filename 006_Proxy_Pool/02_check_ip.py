# -*-coding:utf-8-*-
import pymongo
import urllib
import socket
socket.setdefaulttimeout(5)

import time

import threading

import os


class Check_Ip(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host = '127.0.0.1',port = 27017)
        self.db = self.client.Proxy
        self.collection = self.db.proxy_daili

    def send_check(self,_id,count,proxy_temp):
        # print('这是子进程，进程编号：%d' % os.getpid())
        # time.sleep(10)
        url = "http://ip.chinaz.com/getip.aspx"
        # url = "https://www.baidu.com/"
        try:
            res = urllib.urlopen(url,proxies=proxy_temp).read()
            print(res)
        except Exception as e:
            count -=1 
            print e
            self.collection.update({'_id': _id}, {"$set" :{"count": count}})
        else:
            print proxy_temp
            count += 1
            self.collection.update({'_id': _id}, {"$set" :{"count": count}})

    def check_proxy(self):
        # pool = multiprocessing.Pool(processes=10)
        for mip in self.collection.find({"count":1}):
            ip = mip['ip']
            _id = mip['_id']
            count = mip['count']
            proxy_host = 'http://'+ip

            proxy_temp = {"http":proxy_host}
            # self.send_check(_id,count,proxy_temp)

            t = threading.Thread(target = self.send_check,args=(_id,count,proxy_temp))
            t.start()
            t.join()

    def main(self):
        self.check_proxy()
  
if __name__ == '__main__':
    check_ip = Check_Ip()
    check_ip.main()


