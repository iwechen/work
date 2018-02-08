import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


lottery = '180208-061'
url = 'http://eoifu.cn/Plus/SendPrize/KR_SendPrize_Ssc.asp?lt=%D6%D8%C7%EC%CA%B1%CA%B1%B2%CA&cp_num='+lottery+'&Submit=%CC%E1%BD%BB'

response = requests.get(url = url).content
print(response.decode('gbk'))
print('ok')
