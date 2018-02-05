import pymongo
import re
import csv


client = pymongo.MongoClient(host='127.0.0.1',port=27017)

db1 = client.HuBei

collection = db1['hubei_item']
collection_save = db1['hubei_data']
count = 37910

print(len([item for item in collection.find()]))

a = 0
def collect():
    
    for item in collection.find():
        data_li = []
        data_dict = {}

        date = item['date']
        # print(date)
        aa = item['aa']
        # print(aa)
        # 主力火电厂开机情况
        data1 = re.findall(r'全省(\d+)台20万千瓦及以上.*?(\d+)台',aa,re.S)
        # 100万千瓦机组
        data2 = re.findall(r'(\d+)台100万千瓦.*?(\d+)台',aa,re.S)
        # 60万千瓦机组
        data3 = re.findall(r'(\d+)台60万千瓦机组.*?(\d+)台',aa,re.S)
        # 30万千瓦机组
        data4 = re.findall(r'(\d+)台30万千瓦机组.*?(\d+)台',aa,re.S)
        # 20万千瓦机组
        data5 = re.findall(r'(\d+)台20万千瓦机组.*?(\d+)台',aa,re.S)
        
        data2[0] = list(data2[0])
        if data2[0][1] == '12':
            data2[0][1] = data2[0][0]
        # print(data2)
        data3[0] = list(data3[0])
        if data3[0][1] == '31':
            data3[0][1] = data3[0][0]
        # print(data3)
        data4[0] = list(data4[0])
        if (data4[0][1] == '3')  or (data4[0][1] =='2'):
            data4[0][1] = data4[0][0]
        # print(data4)
        if data5 == []:
            data5 = [('2','2')]
        # print(data5)
        global a
        a +=1
        data_dict['日期'] = date
        data_dict['总数'] = data1[0][0]
        data_dict['开机数量'] = data1[0][1]
        data_dict['100万千瓦数量'] = data2[0][0]
        data_dict['100万千瓦开机数量'] = data2[0][1]  

        data_dict['60万千瓦数量'] = data3[0][0]
        data_dict['60万千瓦开机数量'] = data3[0][1]     

        data_dict['30万千瓦数量'] = data4[0][0]
        data_dict['30万千瓦开机数量'] = data4[0][1]  

        if data5 == []:
            data_dict['20万千瓦数量'] = '2'
            data_dict['20万千瓦开机数量'] = '2' 
        else:  
            data_dict['20万千瓦数量'] = data5[0][0]
            data_dict['20万千瓦开机数量'] = data5[0][1]

        try:
            cc = item['cc']
            # print(cc)
            cc1 = re.match(r'.*?全省(\d+)家.*?存煤([0-9]*\.?[0-9]+)万.*?进电煤([0-9]*\.?[0-9]+)万吨.*?耗电煤([0-9]*\.?[0-9]+)万吨',cc)
            data_dict['电厂数量'] = cc1.group(1)
            data_dict['合计存煤'] = cc1.group(2)
            data_dict['当日进电煤'] = cc1.group(3)
            data_dict['当日耗电煤'] = cc1.group(4)
            # print(cc1.group(4))
        except:
            pass
        else:
            data_li.append(data_dict)

            save_to_mongo(data_li)
            
def save_to_mongo(data_li):
    try:
        collection_save.insert(data_li)
        print('successful')
    except:
        print('default')

def read_mongo():
    item_li = []
    for item in collection_save.find():
        # print(item)
        item_li.append(item)
    print(item_li)
    save_to_csv(item_li)

def main():
    # collect()
    # print(a)
    read_mongo()

def save_to_csv(item_li):
    '''保存到csv文件'''
    # print(card_list)
    csv_file = open("湖北省电力主网运行情况.csv", "a")
    # 创建csv文件的读写对象
    csv_wirter = csv.writer(csv_file)
    # 包cd 含所有表头数据的列表 []
    sheet_data = item_li[0].keys()
    print(sheet_data)
    # 包含所有数据的大列表 [{}, {},{}, {}] 里面每个小列表都是一条数据
    data_list = [item.values() for item in item_li]
    # [[],[],[]]
    # writerow 写入一行数据，参数是一个列表
    print(data_list)
    csv_wirter.writerow(sheet_data)
    # writerows 写入多行数据，参数是一个嵌套列表
    csv_wirter.writerows(data_list)
    csv_file.close()

if __name__ == '__main__':
    main()








