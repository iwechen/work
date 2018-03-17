#coding=utf-8
import requests
data=requests.get('http://www.yixieyingxiao.com/JxsHPublish/Index.html').text
print data