import pymongo
from datetime import datetime


# client = pymongo.MongoClient(host='127.0.0.1',port=27017)


# db1 = client.Items
db1 = client.e_commerce

print(db1.collection_names(include_system_collections=False))

# collection = db1['weather_item']
# count = 37910

# print(len([item for item in collection.find()]))

# for item in collection.find()[37:]:      
#     print(item)
#     count+=1
#     # try:s
#     titles = item['title']
#     print(titles)
#     for del_li in collection.find({"title":titles}):
#         # print(del_li['_id'])
#         collection.remove({"_id":del_li['_id']})

#         print('去重成功!------------%s'%titles)
        
#     # except: 
#         # collection.remove({"_id":item['_id']})
#         # print('数据出现错误')


# for item in collection.find({}, {'date': 1}):
#     time = item['date']
#     _id = item['_id']


#     time = datetime.strptime(time,"%Y年%m月%d日")

#     print(type(time))
#     print(time)
#     collection.update({'_id': _id}, {"$set" :{"date": time}})


    # time = time.replace(r'年','-').replace(r'月','-').replace(r'日','')


    # print(time)
    # print(type(time))

    # timer = ''.join(time.split('-'))
    # print(timer)



