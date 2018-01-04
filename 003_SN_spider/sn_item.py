#-*- coding:utf8 -*-
import requests
from lxml import etree
import re
import json
from pymongo import MongoClient
import gevent
from gevent import monkey
monkey.patch_all()
import multiprocessing
import time

class SN(object):
    '''苏宁易购生鲜数据'''
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3236.0 Safari/537.36"}
        # 创建mongo数据库连接
        self.client = MongoClient(host = "127.0.0.1", port = 27017)
        # 创建数据库和集合
        self.db = self.client["Items"]
        self.collection = self.db["sn_item"]

    def send_request(self,url):
        '''发起请求,返回页面html信息'''
        response = requests.get(url = url,headers = self.headers).content.decode('utf-8')
        return response

    def send_price(self,pid):
        '''获取价格'''
        url = 'https://ds.suning.cn/ds/generalForTile/000000000'+str(pid)+'_-010-2-0010128947-1--ds0000000001738.jsonp'
        response = requests.get(url = url,headers = self.headers).content.decode('utf-8')
        price = re.search(r'"snPrice":"(.*?)"',response).group(1)
        return price

    def send_comment_tags(self,pid):
        '''获取评论标签'''
        url = 'https://review.suning.com/ajax/getreview_labels/general-000000000'+str(pid)+'-0010128947-----commodityrLabels.htm'
        response = requests.get(url = url,headers = self.headers).content.decode('utf-8')
        tags_li = re.findall(r'"labelName":"(.*?)"',response)
        return tags_li

    def comment_cnt(self,pid):
        '''获得评价量'''
        url = 'https://review.suning.com/ajax/review_satisfy/general-000000000'+str(pid)+'-0010128947-----satisfy.htm'
        response = requests.get(url = url,headers = self.headers).content.decode('utf-8')
        response = re.search(r'\[(.*?)\]',response).group(1)
        res = json.loads(response)
        return res

    def send_rec_view_buy(self,pid):
        '''看了最终买了'''
        url = 'https://tuijian.suning.com/recommend-portal/dyBase.jsonp?parameter=000000000'+str(pid)+'&sceneIds=1-2&count=5'
        response = requests.get(url = url,headers = self.headers).content.decode('utf-8')
        rec_buy = re.findall(r'"sugGoodsCode":"000000000(.*?)",',response)
        return rec_buy    

    def send_rec_hot(self,pid):
        '''热销推荐'''
        url = 'https://tuijian.suning.com/recommend-portal/dyBase.jsonp?parameter=000000000'+str(pid)+'&sceneIds=1-5&count=10'
        response = requests.get(url = url,headers = self.headers).content.decode('utf-8')
        rec_hot = re.findall(r'"sugGoodsCode":"000000000(.*?)",',response)
        return rec_hot

    def collect_url(self,response):
        '''获取所有子类url'''
        html = etree.HTML(response)
        url_li = html.xpath('//ul[@class="sort-list"]/li/span/a/@href')
        return url_li

    def collect_detail_url(self,response):
        '''获取商品详情页url'''
        html = etree.HTML(response)
        detail_url_li = html.xpath('//ul[@class="clearfix"]/li/div/div/div/div/div/a/@href')
        return detail_url_li

    def collect_data(self,html,pid):
        '''构建收集数据'''
        goods_li = []
        goods_dict = {}
        html = re.sub(r'60x60','800x800',html)
        html = etree.HTML(html)
        goods_dict['pid'] = pid
        goods_dict['link'] = 'http://product.suning.com/0010128947/'+str(pid)+'.html'
        cate = html.xpath('//div[@class="breadcrumb"]')[0]
        goods_dict['category'] = cate.xpath('./a/text()')[0]+'>'+cate.xpath('./div[1]/span/a/text()')[0]+'>'+cate.xpath('./div[2]/span/a/text()')[0]+'>'+cate.xpath('./div[3]/span/a/text()')[0]+'>'+cate.xpath('./span/a/text()')[0]
        goods_dict['title'] = html.xpath('//div[@class="proinfo-title"]/h1/text()')[1].strip()
        goods_dict['price'] = self.send_price(pid)
        goods_dict['package'] = html.xpath('//ul[@class="cnt clearfix"]/li/text()')
        goods_dict['shop_id'] = '苏宁自营'
        goods_dict['comment_tags'] = self.send_comment_tags(pid)
        goods_dict['recommendation'] = {'看了最终买了':self.send_rec_view_buy(pid),'热销推荐':self.send_rec_hot(pid)}
        goods_dict['comment_cnt'] = self.comment_cnt(pid)
        goods_dict['image_list'] = html.xpath('//div[@class="imgzoom-thumb-main"]/ul/li/a/img/@src')
        goods_dict['desc'] = etree.tostring(html.xpath('//*[@id="productDetail"]/p[2]')[0]).decode('utf-8')

        print(goods_dict['category'])
        goods_li.append(goods_dict)

        self.save_to_mongo(goods_li)

    def collect_comment(self,pid,response):
        '''收集商品评价'''
        comment_li = re.findall(r'"content":"(.*?)","publishTime":"(.*?)".*?"sourceSystem":"(.*?)".*?"nickName":"(.*?)".*?"qualityStar":(\d+)',response)
        item_li = []
        for comment in comment_li:
            comment_dict = {}
            comment_dict['pid'] = pid
            comment_dict['content'] = comment[0]
            comment_dict['publishTime'] = comment[1]
            comment_dict['sourceSystem'] = comment[2]
            comment_dict['nickName'] = comment[3]
            comment_dict['qualityStar'] = comment[4]
            item_li.append(comment_dict)
        print(item_li)
        # self.save_to_mongo(item_li)

    def save_to_mongo(self,goods_li):
        '''保存到mongo'''
        try:
            self.collection.insert(goods_li)
            print('successful')
        except:
            print(goods_li)
            print('default')
            time.sleep(5)

    def start_work(self):
        '''开始发送请求'''
        url = 'https://sxs.suning.com/sxspc_huadong.html'
        response = self.send_request(url)
        url_li = self.collect_url(response)
        return url_li

    def start_detail_url(self,url_li):
        '''送详情页请求'''
        for url_str in url_li:
            page = 0
            while True:
                url = url_str.split('#')[0]+'&cp='+str(page)
                response = self.send_request(url)
                html = etree.HTML(response).xpath('//ul[@class="clearfix"]')
                if html==[]:
                    break
                page += 1
                # 获得详情页请求链接
                detail_url_li = self.collect_detail_url(response)
                for url in detail_url_li:
                    url = 'http:' + url
                    pid = re.search(r'/(\d+)\.html',url).group(1)
                    html = self.send_request(url)
                    # 构建收集数据
                    g1 = gevent.spawn(self.collect_data,html,pid)
                    g1.join()
                    # self.collect_data(html,pid)

    def start_comment(self):
        '''开始获取评价'''
        conn = MongoClient(host='127.0.0.1',port=27017)
        db = conn.Items
        arry = db.sn_item.find()
        for pid in arry:
            pid = pid['pid']
            page = 1
            while True:
                url = 'https://review.suning.com/ajax/review_lists/general-000000000'+pid+'-0010128947-total-'+str(page)+'-default-10-----reviewList.htm'
                response = self.send_request(url)
                print(len(response))
                if len(response) < 100 or len(response)==38208:
                    break
                print('第%d页'%page)
                page += 1

                self.collect_comment(pid,response)

    def main(self):
        # 开始获取商品
        url_li = self.start_work()
        p = multiprocessing.Process(target = self.start_detail_url,args = (url_li,))
        p.start()
        # 开始获取评论

        # self.start_comment()

if __name__ == '__main__':
    sn = SN()
    sn.main()
