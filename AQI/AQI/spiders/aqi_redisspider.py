#-*- coding=utf-8 -*-

import scrapy

from scrapy_redis.spiders import RedisSpider

from AQI.items import AqiItem

# 1. 修改爬虫的父类为RedisSpider
class AqiSpider(RedisSpider):
#class AqiSpider(scrapy.Spider):
    name = "aqi_redisspider"
    allowed_domains = ['aqistudy.cn']


    base_url = "https://www.aqistudy.cn/historydata/"

    # 2. 删除start_urls，添加redis_key
    redis_key = "aqispider:start_urls"
    #start_urls = [base_url]

    def parse(self, response):
        # 取出城市列表页所有城市的链接
        city_link_list = response.xpath("//div[@class='all']/div[@class='bottom']//a/@href").extract()[10:11]
        city_name_list = response.xpath("//div[@class='all']/div[@class='bottom']//a/text()").extract()[10:11]


        for city_link, city_name in zip(city_link_list, city_name_list):
            # 发送每一个城市的请求，获取所有月份的数据，并传递城市名
            yield scrapy.Request(self.base_url + city_link, meta = {"city_name" : city_name}, callback = self.parse_month)


    def parse_month(self, response):
        # 取出每个城市的所有月份的链接
        month_link_list = response.xpath("//tr/td/a/@href").extract()[3:4]

        for month_link in month_link_list:
            # 发送每个城市的每个月的链接，并传递meta
            yield scrapy.Request(self.base_url + month_link, meta = response.meta, callback = self.parse_day)


    def parse_day(self, response):
        # 取出每一天的数据

        node_list = response.xpath("//tr")

        node_list.pop(0)

        for node in node_list:
            item = AqiItem()
            item['city'] = response.meta['city_name']
            item['date'] = node.xpath("./td[1]/text()").extract_first()
            item['aqi'] = node.xpath("./td[2]/text()").extract_first()
            item['level'] = node.xpath("./td[3]//text()").extract_first()
            item['pm2_5'] = node.xpath("./td[4]/text()").extract_first()
            item['pm10'] = node.xpath("./td[5]/text()").extract_first()
            item['so2'] = node.xpath("./td[6]/text()").extract_first()
            item['co'] = node.xpath("./td[7]/text()").extract_first()
            item['no2'] = node.xpath("./td[8]/text()").extract_first()
            item['o3'] = node.xpath("./td[9]/text()").extract_first()

            yield item
