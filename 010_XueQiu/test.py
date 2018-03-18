import requests

cookies = {
    'aliyungf_tc': 'AQAAAKtL+Wx7HAUAs63zdPSJ2jGC8jrG',
    'xq_a_token.sig': 'aaTVFAX9sVcWtOiu-5L8dL-p40k',
    'xq_r_token.sig': 'rEvIjgpbifr6Q_Cxwx7bjvarJG0',
    'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1521288871',
    'device_id': 'ce0a59849606ef4e2a7e215507d44300',
    's': 'ek19tty35r',
    'xq_a_token': '3836bb2166e0e438ade26542b67832432e93209b',
    'xqat': '3836bb2166e0e438ade26542b67832432e93209b',
    'xq_r_token': '43cfe05ee4d224d657f3866da9fc06c5e66b35f7',
    'xq_token_expire': 'Wed%20Apr%2011%202018%2020%3A14%3A52%20GMT%2B0800%20(CST)',
    'xq_is_login': '1',
    'u': '1058215398',
    'bid': '54cdece1f2daa5054574b5263766caff_jevc4mgf',
    'snbim_minify': 'true',
    '__utma': '1.1464544356.1521288913.1521288913.1521288913.1',
    '__utmc': '1',
    '__utmz': '1.1521288913.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1521290240',
    '__utmb': '1.5.10.1521288913',
}

headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://xueqiu.com/S/SZ300002',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

params = {
    'count': '10',
    'comment': '0',
    'symbol': 'SZ300002',
    'hl':'0',
    'source':'all',
    'sort':'',
    'page':'1',
    'q':''
}
# proxies = {'http':'http://120.77.35.48:8899'}
url = 'https://xueqiu.com/statuses/search.json?'
response = requests.get(url = url,params=params,headers=headers, cookies=cookies).content.decode('utf-8')


print(response)