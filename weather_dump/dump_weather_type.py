# coding: utf-8
import pymongo
import json

conn = pymongo.MongoClient()

db = conn.Items

all_weather_type = set()
for item in db.weather_item.find():
    all_weather_type.update(item['weather'].split('/'))


name_map = {}
data = dict(zip(all_weather_type, range(len(all_weather_type))))
for k, v in data.items():
    _v = bin(v).lstrip('0b').zfill(6)
    name_map[k] = _v
    name_map[_v] = k
    print(k, v, _v)
with open('weather_type.json', 'w') as F:
    F.write(json.dumps(name_map, ensure_ascii=False,  indent=2))
