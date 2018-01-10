# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import scrapy
import time
from selenium import webdriver

class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        # 如果url不是首页，再使用Chrome获取数据，否则使用Scrapy发送请求
        if request.url != "https://www.aqistudy.cn/historydata/":
            driver = webdriver.Chrome()
            driver.get(request.url)
            time.sleep(2)
            # html 是 Unicode
            html = driver.page_source
            driver.quit()
            # 直接返回响应对象给引擎，引擎会交给spider处理，下载器不再参与工作
            return scrapy.http.HtmlResponse(url = request.url, body = html.encode("utf-8"), encoding="utf-8", request=request)

    #spider 将请求 给 引擎， 引擎 - Selenium  response
