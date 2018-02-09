import requests
import pymongo
import time
import re


class SheTuSpider(object):
    def __init__(self):
        self.image_name = None
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)

        self.db1 = self.client.SheTu

        self.collection = self.db1['shetuwang_item']

    def download_image(self,image_url):
        image_b = requests.get(url = image_url).content
        print('正在下载---->>%s'%self.image_name)
        with open(self.image_name+'jpg','wb') as f:
            f.write(image_b)

    def read_mongo(self):
        image_li = [item for item in self.collection.find({'category_name': 'people'}, {'id': 1, 'url':1, '_id': 0})]
        # print(id_li)
        for image_dict in image_li:
            response = self.collect_image_url(image_dict)
            print(response)

            image_url = re.sub(r'\\','',re.search(r'(http:.*\.jpg)',response).group(1))
            print(image_url)
            self.download_image(image_url)
            time.sleep(5)

    def collect_image_url(self, image_dict):
        url = 'http://699pic.com/download/getDownloadUrl'
        print(image_dict)
        self.image_name = image_dict['id']
        formdata = {'pid':image_dict['id'],
                    'byso': '0',
                    'bycat': '0',
                    'filetype': '3'}

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '101',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'uniqid=5a7babe03acae; from_data=YTo1OntzOjQ6Imhvc3QiO3M6MTM6Ind3dy5iYWlkdS5jb20iO3M6Mzoic2VtIjtiOjA7czoxMDoic291cmNlZnJvbSI7aTowO3M6NDoid29yZCI7TjtzOjM6ImtpZCI7aTowO30%3D; is_click_activity=1; isSearch=0; isVip=0; isPay=0; is_qy_vip=1; curl_url=http%3A%2F%2F699pic.com%2Factivity%2FlifeVip%3Fclick_type%3D129%3FbindPhone%3D1; session_data=YTo1OntzOjM6InVpZCI7czo2OiIyNTYxMjYiO3M6NToidG9rZW4iO3M6MzI6IjJkMWVkZTk5ZWJjMTc3ZTQ4YzE2ZTE2YWUzM2ExMWM1IjtzOjM6InV1dCI7czozMjoiYjUyMTczYTQ1NzRiNTBlMmM5ODhmYzUxMzUwOWUwYjAiO3M6NDoiZGF0YSI7YToxOntzOjg6InVzZXJuYW1lIjtzOjIwOiLpvormsKNg5bCb77yG6L6l44G1ICI7fXM6NjoiZXh0aW1lIjtpOjE1MTg2NjA4MTc7fQ%3D%3D; username=%E9%BE%8A%E6%B0%A3%60%E5%B0%9B%EF%BC%86%E8%BE%A5%E3%81%B5+; uid=256126; PHPSESSID=25uu42c5paaop5ac9jdha7tsnt0l4a62; resource_number_data20180209=1461836%2C1332047%2C76255%2C45650%2C9805%2C10617; uv_cookie=ab0e614634f0a977d4186c2db106e6ec; Qs_lvt_135734=1518054371%2C1518142617; mediav=%7B%22eid%22%3A%22278616%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22FCpWKR%3Ds%5E%3C%3Amt%25*wGwkM%22%2C%22ctn%22%3A%22%22%7D; Hm_lvt_ddcd8445645e86f06e172516cac60b6a=1518054372,1518054664,1518142618; Hm_lvt_1154154465e0978ab181e2fd9a9b9057=1518054372,1518054664,1518142618; s_token=44d89e01770ce3ae9d3e2d39295ce819; login_user=1; zinfo=975946_2018-02-09; Qs_pv_135734=1519236515796168000%2C4124700567681646000%2C629600314336897900%2C154678413107720600%2C54190875806200670; Hm_lpvt_ddcd8445645e86f06e172516cac60b6a=1518151930; Hm_lpvt_1154154465e0978ab181e2fd9a9b9057=1518151930',
            'Host': '699pic.com',
            'Origin': 'http://699pic.com',
            'Referer': image_dict['url'],
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        response = requests.post(url=url, data=formdata, headers=headers).content.decode('utf-8')
        return response

    def main(self):
        self.read_mongo()

if __name__ == "__main__":
    shetu = SheTuSpider()
    shetu.main()
