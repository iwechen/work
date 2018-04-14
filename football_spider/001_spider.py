import requests
import time
import re
import json


class FootBall(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        }

    
    def mouse_xi(self):
        params = {'d':str(int((time.time())*1000))}
        url = 'http://s.390ko.net:3389/mouse_xi/11520/11520456'
        response = requests.get(url=url,params=params,headers=self.headers).content.decode('utf-8')
       
        data1 = re.sub(r',,',',-1,',re.findall(r'var ximt=(\{.*?\});',response,re.S)[0])
        data3 = re.findall(r'var xitp=(\{.*?\});',response,re.S)[0]
        data = re.findall(r'var xitm=(\{.*?\});',response,re.S)[0]
        data4 = re.findall(r'var xi_array=(\{.*?\});',response,re.S)[0]
        # print('---------------------------------------------------------------------------------------')

        # print(data)
        
        a = eval(data)
        # print(type(a))
        for i in a.values():
            print(i)
    def mouse_zd(self):
        url = 'http://s.390ko.net:3389/odds_new/mouse_zd/397/11486/11486716'
        params = {'d':str(int((time.time())*1000))}
        response = requests.get(url=url,params=params,headers=self.headers).content.decode('utf-8')
        # print(response)
        a = response.split(';')
        for i in a:

            print(i)


    def run(self):
        # self.mouse_xi()
        self.mouse_zd()
        

    def main(self):
        self.run()


if __name__=="__main__":
    football = FootBall()
    football.main()
