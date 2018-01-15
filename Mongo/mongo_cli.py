import pymongo

# client = pymongo.MongoClient(host='127.0.0.1',port=27017)
client = pymongo.MongoClient('mongodb://work:cxgc_2018@10.18.103.154:27017')

db1 = client.e_commerce

# print(db1.collection_names(include_system_collections=False))

collection = db1['jdspider_item']
count = 37910

print(len([item for item in collection.find()]))

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









