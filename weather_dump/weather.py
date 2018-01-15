# coding: utf-8

import pymongo
import json
import os
from datetime import datetime

conn = pymongo.MongoClient()
db = conn['Items']

all_data = db.weather_item.find({'date': {'$gt': datetime(2017, 9, 1)}})

weather_name_map = json.load(open('weather_type.json', 'r'))


def dump():
    with open('20170901-.txt', 'w') as F:
        for data in all_data:
            try:
                date = data['date'].strftime('%Y%m%d')
                province = data['pro']
                city = data['city']
                temp = data['temp']
                weather = data['weather']
                w1, w2 = map(weather_name_map.get, weather.split('/'))
                encoded_weather = ''.join([w1, w2])
                temp_low, temp_high = map(lambda x: x.strip('℃'), temp.split('/'))
                F.write('\t'.join([date, province, city, encoded_weather, temp_low, temp_high]))
                F.write(os.linesep)
            except Exception as e:
                print(e)
                print(data)
                raise
                

if __name__ == '__main__':
    dump()
            
