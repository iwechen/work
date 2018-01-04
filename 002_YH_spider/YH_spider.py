#-*- coding:utf-8 -*-  
from gevent import monkey
monkey.patch_all()
import requests
import time
import hashlib 
import re
import json
import gevent
import csv
import pymongo

class YH(object):
    '''永辉超市全站数据'''
    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'}
        self.access_token = 'YH601933yCzc'
        self.api_citys = 'https://activity.yonghuivip.com/api/app/shop/citys?'
        self.api_stores = 'https://activity.yonghuivip.com/api/app/shop/storelist?'
        self.api_category = 'https://activity.yonghuivip.com/api/app/v4/search/sellercategory?'
        self.api_goods = 'https://activity.yonghuivip.com/api/app/v4/search/sellersku?'
        self.url_detail = 'https://activity.yonghuivip.com/h5/yh-weixin-mall/#/detail?'
        # 动态存储当前店铺信息
        self.now_shop_data = {}

        self.count = 0

        # 创建mongo数据库连接
        self.client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
        # 创建数据库和集合
        self.db = self.client["Items"]
        self.collection = self.db["yh_item"]

    @property
    def timestamp(self):
        return str(int(time.time() * 1000))
    
    def sorted_dict(self,adict):
        '''作用：接收字典，返回按keys排序后字符串'''
        # 生成排序后的列表
        keys_li = sorted(adict.keys())
        values_li = map(adict.get,keys_li)
        # 组合k,v有序列表
        sign_li = [list(item) for item in list(zip(keys_li,values_li))]
        sign_str = self.access_token
        
        for i in sign_li:
            sign_str += ''.join(i)
        # print(sign_str)
        return sign_str

    def hash_to_md5(self,sign_str):
        '''
        接收：接收待加密的字符串
        返回：sign签名字符串
        '''
        # 创建MD5对象
        m= hashlib.md5()
        sign_str = sign_str.encode('utf-8')
        # 加密字符串  
        m.update(sign_str) 
        sign = m.hexdigest() 
        return sign

    def send_request(self,url,params_data):
        response = requests.get(url = url, params = params_data,headers = self.headers)
        json_data = response.content.decode('utf-8')
        return json_data

    def collect_city_data(self,response):
        '''提取所有站点城市数据'''
        city_li = re.findall(r'"id":"(\d+)".*?"lat":"(.*?)".*?"lng":"(.*?)".*?"name":"(.*?)"',response)
        # print(city_li)
        for position_tup in city_li:
            city_dict = {}
            city_dict['cityid'] = position_tup[0]
            city_dict['lat'] = position_tup[1]
            city_dict['lng'] = position_tup[2]

            print(position_tup[3])
            # 开始获取店铺信息
            self.start_store_data(city_dict)

    def collect_store_data(self,response):
        '''提取城市下所有店铺'''
        store_li = re.findall(r'"cityid":"(\d+)".*?"commercialid":(\d+),.*?"id":"(.*?)".*?"lat":"(.*?)".*?"lng":"(.*?)".*?"name":"(.*?)"',response)
        store_li = list(set(store_li))

        for store_tup in store_li:
            store_dict = {}
            store_dict['cityid'] = store_tup[0]
            store_dict['sellerid'] = store_tup[1]
            store_dict['shopid'] = store_tup[2]
            store_dict['lat'] = store_tup[3]
            store_dict['lng'] = store_tup[4]
            print(store_tup[5])

            self.start_category_data(store_dict)

    def collect_category_data(self,response):
        '''提取店铺商品种类信息'''
        try:
            ret_str = re.search(r'(\[.*\]),',response).group(1)
            ret_li = json.loads(ret_str)
            # print(ret_li)
        except:
            print('-----------------------error--------------------------')
            print(response)
            # time.sleep(5)
            return
        # 存储当前店铺下种类信息
        # {'10002092': {'10002104': '新鲜水果', '10002092': '新鲜蔬果', '10002103': '时令蔬菜'},}
        category_dict = {}
        for i in ret_li:
            # catagory_dict = {}
            items = {item['categoryid']:item['categoryname'] for item in i['subcategory']}
            items[i['categoryid']] = i['categoryname']
            category_dict[i['categoryid']] = items

        self.start_goods_data(category_dict)

    def collect_goods_data(self,response,category_dict):
        '''提取商品信息'''
        # print(response)
        goods_li = re.findall(r'"id":"(.*?)".*?"value":(\d+).*?"sellercategory":(\d+),"sellercategoryppid":(\d+).*?"shopid":"(.*?)".*?"spec_prop":"(.*?)".*?"title":"(.*?)"',response)
        # ('R-CB196460', '390', '10002103', '10002092', '9538', '250g-270g/份', '彩食鲜蒜苔')
        goods_li_data = []
        for goods  in goods_li:
            try:
                goods_dict = {}
                goods_dict['pid'] = goods[0]
                goods_dict['vender_id'] = goods[0]
                goods_dict['price'] = float(goods[1])/100
                goods_dict['category'] = category_dict[str(goods[3])][str(goods[3])]+'>'+category_dict[str(goods[3])][str(goods[2])]
                goods_dict['link'] = self.url_detail+'productID='+goods[0]+'&shopid='+goods[4]
                goods_dict['shop_id'] = goods[4]
                goods_dict['package'] = {'规格':goods[5]}
                goods_dict['title'] = goods[6]
                goods_dict['comment_cnt'] = {}
                goods_dict['comment_tags'] = []
                goods_dict['recommendation'] = {}
                # print(goods_dict['category'])
            except:
                pass
            
            goods_li_data.append(goods_dict)

        print(goods_li_data)
        # 开始存储
        # self.save_to_mongo(goods_li_data)
 
    def save_to_mongo(self,goods_li_data):
        '''存储MongoDB'''
        try:
            self.collection.insert(goods_li_data)
            print("存储成功！")
        except Exception:
            print("存数失败！")

    def start_city_data(self):
        '''开始获取所有站点城市'''
        params_data = {'timestamp':self.timestamp,
        'platform':'wechat',
        'channel':'wechat',
        'v':'4.0.1'}
        # 字典参数排序
        sign_str = self.sorted_dict(params_data)
        # 对字典参数加密，获得sign
        sign = self.hash_to_md5(sign_str)
        params_data['sign'] = sign
        # 发送请求，获取响应数据
        response = self.send_request(self.api_citys,params_data)
        # 提取数据
        response = self.collect_city_data(response)

    def start_store_data(self,store_dict):
        '''开始获取城市下所有店铺'''
        store_dict['timestamp'] = self.timestamp
        store_dict['platform'] = 'wechat'
        store_dict['channel'] = 'wechat'
        store_dict['v'] = '4.0.1'
        # print(store_dict)
        sign_str = self.sorted_dict(store_dict)

        sign = self.hash_to_md5(sign_str)
        store_dict['sign'] = sign
        # print(store_dict)
        response = self.send_request(self.api_stores,store_dict)
        # print(response)

        self.collect_store_data(response)

    def start_category_data(self,store_dict):
        '''开始获取店铺下所有种类'''
        store_dict['isfood'] = '0'
        store_dict['pickself'] = '1'
        store_dict['timestamp'] = self.timestamp
        store_dict['platform'] = 'wechat'
        store_dict['channel'] = 'wechat'
        store_dict['v'] = '4.0.1'
        # 组件sign并发送请求
        sign_str = self.sorted_dict(store_dict)
        sign = self.hash_to_md5(sign_str)
        store_dict['sign'] = sign
        response = self.send_request(self.api_category,store_dict)
        del store_dict['timestamp']
        self.now_shop_data = store_dict
        # 协程同时获取类下所有商品
        g1 = gevent.spawn(self.collect_category_data,response)
        g1.join()
        # self.collect_category_data(response)
        
    def start_goods_data(self,category_dict):
        '''开始获取商品数据'''
        for category in category_dict.keys(): 
            # 加载每一页商品数据
            page = 0
            while True:
                goods_dict = self.now_shop_data
                goods_dict['ordertype'] = '0'
                goods_dict['order'] = '0'
                goods_dict['page'] = str(page)
                goods_dict['timestamp'] = str(int(time.time()*1000))
                goods_dict['categoryid'] = category
                del goods_dict['sign']
                page += 1
                # print(goods_dict)

                sign_str = self.sorted_dict(goods_dict)

                sign = self.hash_to_md5(sign_str)
                goods_dict['sign'] = sign
                # print(goods_dict)
                response = self.send_request(self.api_goods,goods_dict)
                if len(response) < 120:
                    break
                print('第%d页'%page)
                self.collect_goods_data(response,category_dict)

    def main(self):
        self.start_city_data()

if __name__ == '__main__':
    yh = YH()
    yh.main()

