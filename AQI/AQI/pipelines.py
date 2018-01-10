# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
from datetime import datetime
import json
import pymongo
import redis


class AqiPipeline(object):
    def process_item(self, item, spider):
        item['source'] = spider.name
        item['utc_time'] = str(datetime.utcnow())
        return item


class AqiJsonPipeline(object):
    def open_spider(self, spider):
        self.filename = open("aqi.json", "w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item)) + ",\n"
        self.filename.write(content)
        return item

    def close_spider(self, spider):
        self.filename.close()


class AqiCsvPipeline(object):
    def open_spider(self, spider):
        self.filename = open("aqi.csv", "w")
        # 创建一个csv文件读写对象，参数是需要保存数据的csv文件对象
        self.csv_exporter = CsvItemExporter(self.filename)
        # 表示开始进行数据写入
        self.csv_exporter.start_exporting()

    def process_item(self, item, spider):
        self.csv_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        # 表示结束数据写入
        self.csv_exporter.finish_exporting()
        self.filename.close()


class AqiMongoPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host="192.168.118.79", port=27017)
        self.db = self.client['AQI']
        self.collection = self.db['aqi_data']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class AqiRedisPipeline(object):
    def open_spider(self, spider):
        self.client = redis.Redis(host="127.0.0.1", port=6379)

    def process_item(self, item, spider):
        content = json.dumps(dict(item))
        self.client.lpush("AQI_ITEM", content)
        return item












