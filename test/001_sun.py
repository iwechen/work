import requests

cookies = {
    'PHPSESSID': 'i4ugvi5p3645gvgs7383ks6pe5',
    'UM_distinctid': '162c2cf5a73c07-03400595d19889-336c7b05-13c680-162c2cf5a747c9',
    'CNZZDATA1254842228': '1890387376-1523684256-https%253A%252F%252Fwww.baidu.com%252F%7C1523684256',
    'zg_did': '%7B%22did%22%3A%20%22162c2cf5acba6e-0c92e5a93c5c9-336c7b05-13c680-162c2cf5acc1bc8%22%7D',
    'hasShow': '1',
    # 'acw_tc': 'AQAAAOEw9WDFjQwAZa+R23lNXVyJIZYn',
    '_uab_collina': '152368680217178910406075',
    'Hm_lvt_3456bee468c83cc63fb5147f119f1075': '1523686792,1523687618,1523688280',
    'Hm_lpvt_3456bee468c83cc63fb5147f119f1075': '1523688292',
    'zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f': '%7B%22sid%22%3A%201523686791887%2C%22updated%22%3A%201523688299744%2C%22info%22%3A%201523686791888%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%7D',
}

headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://www.qichacha.com',
    'Connection': 'keep-alive',
}





#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('http://www.qichacha.com/search?key=%E5%88%9B%E6%96%B0%E5%B7%A5%E5%9C%BA', headers=headers, cookies=cookies)

url = 'http://www.qichacha.com/search'



params = {
    'key':'渭南师范学院'
}


response = requests.get('http://www.qichacha.com/search', headers=headers, params=params, cookies=cookies).content.decode('utf-8')
print(response)
