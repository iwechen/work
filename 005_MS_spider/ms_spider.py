import requests
import re
from lxml import etree
import time
import pymongo
import gevent
import multiprocessing
from gevent import monkey
monkey.patch_all()

class MSJ_Spider(object):
    '''美食杰菜单爬虫项目'''
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3236.0 Safari/537.36"}
        
        self.client = pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = self.client['Items']
        self.collection = self.db['msj_item']

    def send_request(self,url):
        response = requests.get(url = url,headers = self.headers).content.decode('utf8')
        return response

    def collect_category(self,response):
        html = etree.HTML(response)
        cate_li = html.xpath('//div[@class="dww clearfix dww_cpdq"]/div/dl/dt/a/@href')
        return cate_li

    def collect_food_url(self,response):
        html = etree.HTML(response)
        ret = html.xpath('//div[@class="listnav clearfix"]/div/dl/dd/a/@href')
        return ret

    def collect_page_url(self,response):
        '''提取每一个页面所有链接'''
        # print(response)
        html = etree.HTML(response)
        food_url = html.xpath('//div[@class="listtyle1_list clearfix"]/div/a/@href')
        # 开始处理页面所有链接
        self.start_food(food_url)

    def collect_food_menu(self,response):
        food_dict = {}
        html = etree.HTML(response)
        try:
            food_dict['title'] = html.xpath('//h1[@class="title"]/a/text()')
            category = re.search(r'#(.*)#',html.xpath('//ul[@class="pathstlye1"]')[0].xpath('string(.)')).group(1)
            food_dict['category'] = category
            food_dict['tags'] = [i[0].xpath('string(.)') for i in html.xpath('//div[@class="info1"]/dl/dt')]
            food_dict['time'] = [i.xpath('string(.)') for i in html.xpath('//div[@class="info2"]/ul/li')]
            desc = html.xpath('//div[@class="materials"]/p/text()')
            if desc ==[]:
                food_dict['desc'] = ""
            else:
                food_dict['desc'] = desc[0]
            # 主料
            main_sea = dict(zip([i.xpath('string(.)') for i in html.xpath('//div[@class="materials_box"]/div[1]/ul/li/div/h4/a')],[i.xpath('string(.)') for i in html.xpath('//div[@class="materials_box"]/div[1]/ul/li/div/h4/span')]))
            # 辅料
            assist_sea = dict(zip([i.xpath('string(.)') for i in html.xpath('//div[@class="materials_box"]/div[2]/ul/li/h4/a')],[i.xpath('string(.)') for i in html.xpath('//div[@class="materials_box"]/div[2]/ul/li/span')]))
            food_dict['sessioning'] = {'主料':main_sea,'辅料':assist_sea}
            link = html.xpath('//div[@class="cp_headerimg_w"]/img/@src')[0]
            food_dict['link'] = link
            method = [i.xpath('string(.)') for i in html.xpath('//div[@class="editnew edit"]/div/div/p[1]')]
            method_img = html.xpath('//div[@class="editnew edit"]/div/div/p[2]/img/@src')
            if method==[]:
                method = [i.xpath('string(.)') for i in html.xpath('//div[@class="edit edit_class_0 edit_class_13"]/p')]
                method_img = html.xpath('//div[@class="edit edit_class_0 edit_class_13"]/p/img/@src')
            food_dict['method'] = method
            food_dict['method_img'] = method_img
        except:
            print('--------------------------error--------------------')
            print(food_dict)
            return False
        else:
            print(food_dict)
            return food_dict

    def start_food(self,food_url):
        food_li = []
        for url in food_url:
            # url = 'http://www.meishij.net/zuofa/suanrongzhengjinzhengu.html'
            error_link = {}
            print(url)
            response = self.send_request(url)
            food_dict = self.collect_food_menu(response)
            if food_dict==False:
                error_link['link'] = url
                collection = self.db['msj_error_link']
                collection.insert(error_link)
                print('save_error_link_ok! ')
            else:
                food_li.append(food_dict)
        self.save_to_mongo(food_li)

    def save_to_mongo(self,food_dict):
        try:
            self.collection.insert(food_dict)
            print('successful')
        except:
            print('default！')

    def start_page(self,url_li):
        for url in url_li:
            all_page = 1
            page = 1
            while page <= all_page: 
                url_now = url
                url_now = url_now+'?&page='+str(page)
                if page == 1:
                    response = self.send_request(url_now)
                    all_page = int(re.search(r'共(.*?)页',response).group(1))
                print('第%d/%d页'%(page,all_page))
                # 请求每一个页面数据
                response = self.send_request(url_now)
                # 获取每一个页面数据
                self.collect_page_url(response)
                page += 1
                url = url

    def start_category(self,cate_li):
        for cate_url in cate_li:
            response = self.send_request(cate_url)
            url_li = self.collect_food_url(response)
            # self.start_page(url_li)
            # 创建协程爬取每个页面
            g1 = gevent.spawn(self.start_page,url_li)
            g1.join()

    def start_work(self):
        url = 'http://www.meishij.net/chufang/diy/'
        response = self.send_request(url)
        cate_li = self.collect_category(response) 
        
        self.start_category(cate_li)
        # p = multiprocessing.Process(target=self.start_category,args=(cate_li,))
        # p.start()

    def main(self):
        self.start_work()

if __name__ == '__main__':
    msj = MSJ_Spider()
    msj.main()

