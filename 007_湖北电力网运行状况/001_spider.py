from lxml import etree
import requests
import re
import pymongo


class HB(object):
    def __init__(self):

        self.cookies = {
            '_trs_uv': 'jcyam6ej_256_67g1',
            '_trs_ua_s_1': 'jcyam6ej_256_9eyj',
        }
        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://fgw.hubei.gov.cn/ywcs2016/dlddc/dlyx/index_20.shtml',
            'Connection': 'keep-alive',
        }
        self.client = pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = self.client['HuBei']
        self.collection = self.db['hubei_item']


    def send_requests(self,url):
        response = requests.get(url = url, headers=self.headers, cookies=self.cookies).content.decode('utf-8')
        return response

    def collect_page_url(self,response):
        html = etree.HTML(response)
        url_li = html.xpath('//div[@class="gl_right"]/div/div/h1/a/@href')
        return url_li

    def collect_data(self,response):
        data_li = []
        data_dict = {}
        html = etree.HTML(response)
        try:
            ele_data = html.xpath('//div[@class="TRS_Editor"]')[0].xpath('string(.)')
            month = re.match(r'(\d+月\d+日).*',html.xpath('//div[@class="fgw_xl_content"]/h1/text()')[0]).group(1)
            years = re.match(r'(\d+年).*',html.xpath('//div[@class="xl_source"]/span[2]/span/text()')[0]).group(1)
            datetime = years + month
            data_dict['date'] = datetime
            aa = re.search(r'二、主力火电厂开机情况(.*?)三、',ele_data,re.S).group(1)
            bb = re.search(r'三、主力水电厂水情(.*?)四、',ele_data,re.S).group(1)
            cc = re.search(r'四、全省电煤库存情况(.*)。',ele_data,re.S).group(1)
            # 主力火电厂开机情况
            data_dict['aa'] = re.sub(r'\n|\s','',aa)
            # 主力水电厂水情
            data_dict['bb'] = re.sub(r'\n|\s','',bb) 
            # 全省电煤库存情况
            data_dict['cc'] = re.sub(r'\n|\s','',cc)
        except:
            # pass
            print('匹配失败')
        else:
            data_li.append(data_dict)
            # print(data_li)
            self.save_to_mongo(data_li)
            # print(data_dict)

    def save_to_mongo(self,data_li):
        try:
            self.collection.insert(data_li)
            print('successful')
        except:
            print('default')

    def main(self):
        for page in range(30,67):
            if page==0:
                url_page = 'http://fgw.hubei.gov.cn/ywcs2016/dlddc/dlyx/index.shtml'
            else:
                url_page = 'http://fgw.hubei.gov.cn/ywcs2016/dlddc/dlyx/index_'+str(page)+'.shtml'
            print('第%d页;url:%s'%(page,url_page))
            response = self.send_requests(url_page)

            url_li = self.collect_page_url(response)
            for url_day in url_li:
                url_day = 'http://fgw.hubei.gov.cn/ywcs2016/dlddc/dlyx'+url_day.split('.',1)[1]
                print(url_day)
                response = self.send_requests(url_day)

                self.collect_data(response)


if __name__ == '__main__':
    hb = HB()
    hb.main()




