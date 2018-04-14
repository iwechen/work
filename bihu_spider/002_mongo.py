import pymongo
import urllib.parse
import time
import csv
import re


class ReadMongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = self.client['bihu']
        self.collection = self.db['data']

        self.card_list=[]


    def _read(self):
        for i in self.collection.find():
            self.card_list.append(i)

            # ids = i['_id']
            # content = i['content']
            # contents = re.sub(r'\n','',content)
            # contents = re.sub(r'class=\".*?\"','',contents)
            # contents = re.sub(r'style=\".*?\"|style=\'.*?\'','',contents)
            # contents = re.sub(r'<p></p>','',contents)
            # contents = re.sub(r'&nbsp;','',contents)
            # contents = re.sub(r'<br >|<br>|\?x-oss-process=style/size_lg','',contents)
            # contents = re.sub(r'<span ></span>','',contents)
            # contents = re.sub(r'<p ></p>|<p></p>|<o:p></o:p>','',contents)
            # contents = re.sub(r'lang=\".*?\"','',contents)
            # contents = re.sub(r'<w:.*?>.*?</w:.*?>','',contents)
            # contents = re.sub(r'align=\".*?\"','',contents)
            
            # print(contents)
            # self.collection.update({'_id':ids}, {'$set':{'content':contents}})

            # print(ids)

    def save_to_csv(self):
        '''保存到csv文件'''
        # # print(card_list)
        with open("bihu.csv", "w") as csv_file:
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



    def run(self):
        self._read()
        self.save_to_csv()

    def main(self):
        self.run()

if __name__=='__main__':
    rm = ReadMongo()
    rm.main()

