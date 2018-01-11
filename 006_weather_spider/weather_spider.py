import requests
import re
from lxml import etree
import time
import pymongo
import gevent
from gevent import monkey
monkey.patch_all()

class Weather_Spider(object):
    '''全国天气爬虫项目'''
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3236.0 Safari/537.36"}
        self.url = 'http://www.tianqihoubao.com'
        self.client = pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = self.client['Items']
        self.collection = self.db['weather_item']
        self.pro_name = ''

    def send_request(self,url):
        '''发送请求，返回response'''
        response = requests.get(url = url,headers = self.headers).content
        return response.decode('gbk')

    def collect_pro(self,response):
        '''收集省下所有城市链接'''
        html = etree.HTML(response)
        pro_li_ele = html.xpath('//div[@class="citychk"]/dl')
        pro_li = []
        for pro in pro_li_ele:
            pro_dict = {}
            pro_name = pro.xpath('./dt/a/b/text()')[0]
            city_url = pro.xpath('./dd/a/@href')
            # print(city_url)
            pro_dict[pro_name] = city_url
            # 3.添加到列表
            pro_li.append(pro_dict)
        # print(pro_li)
        return pro_li

    def collect_month(self,response):
        weather_li = []
        html = etree.HTML(response)
        day_ele = html.xpath('//div[@class="hd"]/div[@class="wdetail"]/table')[0]
        city_h1 = re.sub(r'\r\n\s+','',html.xpath('//div[@class="hd"]/div[@class="wdetail"]/h1/text()')[0])
        city_name = re.match(r'^(.*?)历史',city_h1).group(1) 
        date_li = [re.sub(r'\r\n\s+','',i) for i in day_ele.xpath('//td/a/text()')]
        wea_li = [re.sub(r'\r\n\s+','',i) for i in day_ele.xpath('//td[2]/text()')[1:]]
        temp_li = [re.sub(r'\r\n\s+','',i) for i in day_ele.xpath('//td[3]/text()')[1:]]
        wind_li = [re.sub(r'\r\n\s+','',i) for i in day_ele.xpath('//td[4]/text()')[1:]]      
        for i in range(len(date_li)):
            weather_dict = {}
            weather_dict['date'] = date_li[i]
            weather_dict['weather'] = wea_li[i]
            weather_dict['temp'] = temp_li[i]
            weather_dict['wind'] = wind_li[i]
            weather_dict['pro'] = self.pro_name
            weather_dict['city'] = city_name
            weather_li.append(weather_dict)

            print("%s-%s-%s"%(self.pro_name,city_name,date_li[i]))
        self.save_to_mongo(weather_li)
            
    def save_to_mongo(self,weather_li):
        try:
            self.collection.insert(weather_li)
            print('successful')
        except:
            print('default')


    def start_month(self,month_url):
        # 月分页面
        response = self.send_request(month_url)
        # time.sleep(1)
        self.collect_month(response)

    def start_city(self,pro_li):
        '''请求城市下历史时间'''
        # {'北京': ['/lishi/beijing.html','/lishi/beijing.html']}
        for pro in pro_li:
            # {'陕西': ['/lishi/beijing.html','/lishi/beijing.html']}
            for pro_name,city_li in pro.items():
                self.pro_name = pro_name
                ['/lishi/beijing.html','/lishi/beijing.html']
                for city_url in city_li:
                    url = self.url+city_url
                    # print(url)
                    response = self.send_request(url)
                    # self.collect_year(response)
                    html = etree.HTML(response)
                    year_li_ele = html.xpath('//div[@class="wdetail"]/div[@class="box pcity"]')
                    for month_li_ele in year_li_ele[6:]:
                        month_li = month_li_ele.xpath('./ul/li/a/@href')
                        for month in month_li:
                            if len(month) <= 30:
                                month = '/lishi/' + month
                            month_url = self.url + month
                            # self.start_month(month_url)
                            g1 = gevent.spawn(self.start_month,month_url)
                            g1.join()

    def start_work(self):
        '''开始请求省下城市'''
        url = 'http://www.tianqihoubao.com/lishi/'
        response = self.send_request(url)
        pro_li = self.collect_pro(response)
        self.start_city(pro_li)


    def main(self):
        self.start_work()


if __name__ == '__main__':
    wea = Weather_Spider()
    wea.main()






