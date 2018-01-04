# coding:utf-8
import requests
from lxml import etree
import csv
import json
import re
import pymongo

class ZhaoCard(object):
    '''招商银行信用卡数据'''
    def __init__(self):
        self.card_list = []
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3236.0 Safari/537.36"}
        self.client = pymongo.MongoClient(host = '127.0.0.1',port = 27017)
        self.db = self.client['Items']
        self.collection = self.db['zs_card']

    def send_request(self,url):
        '''发起请求,返回页面html信息'''
        response = requests.get(url = url,headers = self.headers).content.decode('utf-8')
        return response

    def params_page(self,html):
        '''解析页面数据,返回数据字典'''
        html = etree.HTML(html)
        # 1.匹配数据区块
        html_list = html.xpath('//div[@class="cardblock"]')
        # card_list = []
        # 2.遍历匹配详细数据
        for html in html_list:
            card_dict = {}
            # 1.信用卡图片链接
            card_img_url = html.xpath('./div/div/a/img/@src')[0]
            card_dict['card_img_url'] = re.sub(r'\r\n\s*',"",card_img_url)
            # 2.信用卡名称
            card_name = html.xpath('./div[2]/h2[1]/a/text()')[0]
            card_dict['card_name'] = re.sub(r'\r\n\s*',"",card_name).encode('utf-8')
            # 3.信用卡说明
            card_detail = html.xpath('./div[2]/h2[2]/text()')
            card_detail_data = ''.join(card_detail)
            card_dict['card_detail'] = re.sub(r'\r\n\s*',"",card_detail_data).encode('utf-8')
            
            self.card_list.append(card_dict)

        # return card_list
        # self.save_to_mongo(card_list)
    
    def save_to_csv(self):
        '''保存到csv文件'''
        # print(card_list)
        csv_file = file("card.csv", "a")
        # 创建csv文件的读写对象
        csv_wirter = csv.writer(csv_file)
        # 包cd 含所有表头数据的列表 []
        sheet_data = self.card_list[0].keys()
        print(sheet_data)
        # 包含所有数据的大列表 [{}, {},{}, {}] 里面每个小列表都是一条数据
        data_list = [item.values() for item in self.card_list]
        # [[],[],[]]
        # writerow 写入一行数据，参数是一个列表
        print(data_list)
        csv_wirter.writerow(sheet_data)
        # writerows 写入多行数据，参数是一个嵌套列表
        csv_wirter.writerows(data_list)

        csv_file.close()

    def save_to_mongo(self):
        try:
            self.collection.insert(self.card_list)
            print('存储成功！')
        except:
            print('存储失败！')
            

    def main(self):
        for page in range(1,21):
            url = 'http://cc.cmbchina.com/card/list_' + str(page) + '.htm'
        
            response_data = self.send_request(url)

            print(response_data)

            self.params_page(response_data)

            print('第%d页'%page)
        self.save_to_mongo()


if __name__ == '__main__':
    zhaocard = ZhaoCard()
    zhaocard.main()




