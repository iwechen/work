# -*-coding:utf-8-*-
import requests
import re
import time
import pymongo

class Proxy_Spider(object):
    def __init__(self):
        self.headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Hosts': 'hm.baidu.com',
        'Referer': 'http://www.xicidaili.com/nn',
        'Connection': 'keep-alive'
        }
        self.client = pymongo.MongoClient(host = '127.0.0.1',port = 27017)
        self.db = self.client['Proxy']
        self.collection = self.db['proxy_daili']

    def spider_proxy(self):
        '''获取代理'''
        # 获取页码范围
        i = 0
        for page in range(22,1000):
            print('第%d页'%page)

            gip_li = [gip for gip in self.collection.find({'count':1})]

            if i > len(gip_li)-1:
                i = 0

            pro_host = gip_li[i]['ip']
            proxies = { "http":pro_host}
            url = 'http://www.xicidaili.com/nn/' + str(page)
            try:
                response = requests.get(url = url, proxies = proxies, headers = self.headers).content.decode('utf-8')
            except:
                i+=1
                continue
            i+=1
            ip_list = re.findall("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{2,6})", response, re.S)
            print(ip_list)
            
            ip_li = [] 
            for ip_tup in ip_list:
                ip_dict = {}
                ip = ip_tup[0] + ':' + ip_tup[1]
                mip = [mip for mip in self.collection.find({'ip':ip})]
                if len(mip) != 0:
                    print('ip:%s已经存在!'%ip)
                    continue
                print(ip)
                ip_dict['ip'] = ip
                ip_dict['count'] = 0
                ip_li.append(ip_dict)

            print(ip_li)
            self.save_to_mongo(ip_li)
            # time.sleep(1)
            
    def save_to_mongo(self,ip_li):
        '''保存未验证ip到mongo'''
        try:
            self.collection.insert(ip_li)
            print('successful!')
        except:
            print('default!')
        
    def check_proxy(self):
        '''验证代理'''

        pass

    def main(self):
        self.spider_proxy()
        # self.check_proxy()

if __name__ == '__main__':
    proxy = Proxy_Spider()
    proxy.main()












