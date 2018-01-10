# -*- coding:utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class AqiCrawlSpider(CrawlSpider):
    name = "aqi_crawl"
    allowed_domains = ['aqistudy.cn']

    base_url = "https://www.aqistudy.cn/historydata/"
    start_urls = [base_url]

    rules = [
        # 在城市列表页提取所有城市的链接，不需要回调函数，默认follow=True
        Rule(LinkExtractor(allow=(r"monthdata\.php\?city=")), follow=True),

        # 在每个城市里提取所有月份的链接，需要处理响应，默认follow=False
        Rule(LinkExtractor(allow=(r"daydata\.php\?city=")), callback = "parse_day", follow=False)
    ]


    def parse_day(self, response):
        # 取出每一天的数据
        node_list = response.xpath("//tr")
        # 取出标题部分
        title = response.xpath("//*[@id='title']/text()").extract_first()

        for node in node_list:
            item = AqiItem()
            item['city'] = title[8:-11]
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
