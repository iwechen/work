import requests
from six.moves import queue
from lxml import etree
import threading
import time
import os

class PradaSpider(object):
    def __init__(self):
        self._response_queue = queue.Queue(1500)
        self._task_url_queue = queue.Queue(1500)
        self._image_queue = queue.Queue(1500)
        self.flag = True
        self.headers = {
            'if-none-match': '"6bb2f-5688e368f89c2-gzip"',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'cache-control': 'max-age=0',
            'authority': 'www.prada.com',
            'referer': 'https://www.prada.com/cn/zh/store-locator.html',
        }

    def load_page(self,url):
        time.sleep(1)
        response = requests.get(url=url,headers=self.headers).content.decode('utf-8')
        return response
        
    def load_goods(self):
        while True:
            image_dict = {}
            ret = self._task_url_queue.get()
            goods_url = ret['goods_url']
            response = self.load_page(goods_url)
            html = etree.HTML(response)
            name = html.xpath('//div[@class="col-xs-12 col-sm-12 pdp-name"]/h1/text()')[0]+'-'+html.xpath('//div[@class="col-xs-12 col-sm-12 pdp-name"]/p[1]/text()')[0]
            # print(name)
            image_li  = list(set(html.xpath('//div[@class="carousel-inner"]/div/div[1]/div[3]/@data-src')))
            type1 = ret['_type1']
            image_dict['type1'] = type1

            type2 = ret['_type2']
            image_dict['type2'] = type2

            type3 = ret['_type3']
            image_dict['type3'] = type3
            image_dict['file_name'] = name
            image_dict['image_li'] = image_li
            self._image_queue.put(image_dict)

    def collection_page(self):
        while True:
            
            type_d = self._response_queue.get()
            response = type_d['response']
            html = etree.HTML(response)
            goods_url_li = ['https://www.prada.com' +i for i in html.xpath('//div[@class="row box-spacer-small-T"]/div/div/div[2]/div[1]/a/@href')]
            for goods_url in goods_url_li:
                goods_d = {}
                goods_d['_type1'] = type_d['_type1']
                goods_d['_type2'] = type_d['_type2']
                goods_d['_type3'] = type_d['_type3']
                goods_d['goods_url'] = goods_url
                self._task_url_queue.put(goods_d)
            if len(goods_url_li) < 12:
                self.flag = False

    def download_image(self):
        while True:
            image_dict = self._image_queue.get()
            # print(image_dict)
            print('%s-->%s'%(image_dict['type3'],image_dict['file_name']))
            name = 1
            for url in image_dict['image_li']:
                proxies = {'http':'http://120.77.35.48:8899'}
                image = requests.get(url = url,proxies=proxies,headers = self.headers).content
                # time.sleep(1)
                path = '/Users/chenwei/Desktop/'+image_dict['type1']+'/'+image_dict['type2']+'/'+image_dict['type3']+'/'+image_dict['file_name']
                folder = os.path.exists(path)  
                if not folder:
                    os.makedirs(path)
                else:  
                    pass
                with open(path+'/'+str(name)+'.jpeg','wb') as f:
                    f.write(image) 
                name +=1

            
        
    def init(self):
        t1 = threading.Thread(target=self.collection_page)
        # t1.setDaemon(True)
        t1.start()
        t2 = threading.Thread(target=self.load_goods)
        # t2.setDaemon(True)
        t2.start()
        t3 = threading.Thread(target=self.download_image)
        # t3.setDaemon(True)
        t3.start()
        t4 = threading.Thread(target=self.download_image)
        # t3.setDaemon(True)
        t4.start()
        t5 = threading.Thread(target=self.download_image)
        # t3.setDaemon(True)
        t5.start()

    def run(self):
        '''briefcases','messenger_bags','clutches','belt_bags','backpacks','''
        self.init()
        _type1 = '女士'
        _task_dic = {
            # 'bags':['handbags','shoulder_bags','tote_bags','backpacks','belt_bags','small_bags','micro-bags','clutches']
            'small_leather_goods':['wallets','technology','pouches']
        }
        for type_world_main, type_world_li in _task_dic.items():
            _type2 = type_world_main
            for type_world in type_world_li:
                page = 1
                self.flag =True
                _type3 = type_world
                
                while self.flag:
                    type_d = {}
                    url = 'https://www.prada.com/cn/zh/women/'+type_world_main +'/'+ type_world +'/jcr:content/par/product-grid.'+ str(page) +'.sortBy_0.html'
                    response = self.load_page(url)  
                    type_d['_type1'] = _type1
                    type_d['_type2'] = _type2
                    type_d['_type3'] = _type3
                    type_d['response'] = response
                    self._response_queue.put(type_d)
                    time.sleep(1)
                    page += 1

    def main(self):
        self.run()


if __name__=="__main__":
    prada = PradaSpider()
    prada.main()
