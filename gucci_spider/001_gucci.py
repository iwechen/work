import requests
from six.moves import queue
from lxml import etree
import threading
import time
import os
import re

class GucciSpider(object):
    def __init__(self):
        # self._response_queue = queue.Queue(1500)
        self._task_url_queue = queue.Queue(1500)
        self._image_queue = queue.Queue(1500)
        self.flag = True
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://www.gucci.cn/zh/ca/women',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }

    def load_page(self,nid,page):
        params = {
            'pn':page,
            'ni':nid,
            '_':int((time.time()*1000))
        }
        url = 'https://www.gucci.cn/zh/itemList'
        # proxies = {'http':'http://120.77.35.48:8899'}
        response = requests.get(url = url,params = params,headers=self.headers).content.decode('utf-8')
        return response

    def load_page_url(self,url):
        response = requests.get(url = url,headers=self.headers).content.decode('utf-8')
        return response
        
    def load_goods(self):
        while True:
            image_dict = {}
            ret = self._task_url_queue.get()
            goods_url = ret['goods_url']
            # print(goods_url)
            response = self.load_page_url(goods_url)
            html = etree.HTML(response)
            name = html.xpath('//h1[@class="spice-product-name"]/text()')[0]+html.xpath('//*[@id="spice-wrapper"]/section[1]/article[2]/div[1]/div/div[2]/div[1]/span/text()')[0]
            image_li  = re.findall(r'(https.*?1200X1200\.jpg)',response)
            # print(image_li)
            type1 = ret['type1']
            image_dict['type1'] = type1

            type2 = ret['type2']
            # print(type2)
            image_dict['type2'] = type2
            image_dict['file_name'] = name
            image_dict['image_li'] = image_li
            self._image_queue.put(image_dict)

    def download_image(self):
        while True:
            image_dict = self._image_queue.get()
            # print(image_dict)
            print('%s->%s->%s'%(image_dict['type2'],image_dict['type2'],image_dict['file_name']))
            name = 1
            for url in image_dict['image_li']:
                # proxies = {'http':'http://120.77.35.48:8899'}
                image = requests.get(url = url,headers = self.headers).content
                # time.sleep(1)
                path = '/Users/chenwei/Desktop/Gucci/男士/'+image_dict['type1']+'/'+image_dict['type2']+'/'+'/'+image_dict['file_name']
                # print(path)
                folder = os.path.exists(path)  
                if not folder:
                    os.makedirs(path)
                else:  
                    pass
                with open(path+'/'+str(name)+'.jpg','wb') as f:
                    f.write(image) 
                name +=1

            
        
    def init(self):
        t2 = threading.Thread(target=self.load_goods)
        t2.start()
        t3 = threading.Thread(target=self.download_image)
        t3.start()
        t4 = threading.Thread(target=self.download_image)
        t4.start()
        t5 = threading.Thread(target=self.download_image)
        t5.start()
        t6 = threading.Thread(target=self.download_image)
        t6.start()

    def run(self):
        # 女士
        self.init()
        _task_nid = {
            'bags':[
                ["ophidia",205],
                ["messenger",52],
                ["backpacks",53],
                ["belt-bags",203],
                ["totes",54],
                ["pouches-bags",212],
                ["briefcases",55],
                ["suitcases-duffle-bags",56]
                ],
            # 'accessories':[
            #     # ['wallets-small-accessories',63],
            #     ['belts',64]
            # ]
        }
        # _task_nid = {
            # 'handbags':[
            #     ["ophidia",199],
            #     ["top-handles",27],
            #     ["totes",28],
            #     ["shoulder-bags",29],
            #     ["backpacks",30],
            #     ["belt-bags",31],
            #     ["mini-bags",32]
            #     ],
            # 'accessories':[
            #     ['luggage-lifestyle-bags',39],
            #     ['wallets-small-accessories',40],
            #     ['belts',41]
            # ]
        # }
        for type1,type_li in _task_nid.items():
            for types in type_li:
                type2 = types[0]
                nid = types[1]
                # print(type2)
                self.flag = True
                page = 1
                while self.flag:
                    # print(page)
                    response = self.load_page(nid,page)
                    # print(len(response))
                    if len(response)<20:
                        self.flag = False
                        break
                    try:
                        html = etree.HTML(response)
                        goods_li = ['https://www.gucci.cn' +i for i in html.xpath('//li/div[1]/div[1]/a[1]/@href')]

                        # print(len(goods_li))
                    except Exception as e:
                        print(e)
                    else:
                        for goods_url in goods_li:
                            task_dic = {}
                            task_dic['type1'] = type1
                            task_dic['type2'] = type2
                            task_dic['goods_url'] = goods_url
                            self._task_url_queue.put(task_dic)
                        # print(1111)
                        page += 1
                        continue
                    break

    def main(self):
        self.run()


if __name__=="__main__":
    gucci = GucciSpider()
    gucci.main()




