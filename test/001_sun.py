import requests
import time

headers = {
    'Origin': 'https://bihu.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
    'Accept': '*/*',
    'Referer': 'https://bihu.com/?category=hots&code=BTC',
    'Connection': 'keep-alive',
}



proxies = {'http':'http://120.77.35.48:8899'}
url = 'https://be02.bihu.com/bihube-pc/api/content/show/hotArtList'


count = 1
while True:
    data = {

    'code':'项目分析',
    'pageNum':count
    }
    response = requests.post(url = url, proxies = proxies,data=data, headers=headers,verify=False).content.decode('utf-8')

    print(response)
    time.sleep(0.3)
    count +=1
    print(count)




