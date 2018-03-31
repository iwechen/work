import csv
import pymongo


class ChangeCsv(object):
    '''转换成csv文件'''
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1',port = 27017)
        self.db = self.client.XueQiu
        self.collections = self.db['data']
        self.card_list = []

    def find_mongo(self):
        card_list = [i for i in self.collections.find({'symbol':'SZ300002'})]
        self.card_list = card_list
        # print(self.card_list)

    def save_to_csv(self):
        '''保存到csv文件'''
        # # print(card_list)
        with open("SZ300002.csv", "w") as csv_file:
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

    def main(self):
        self.find_mongo()
        self.save_to_csv()

if __name__=="__main__":
    csva = ChangeCsv()
    csva.main()




