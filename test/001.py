import requests
from lxml import etree



class SheTuWang(object):
    """摄图网爬虫"""
    def __init__(self,):
        self.cookies = {
            'mediav': '^%^7B^%^22eid^%^22^%^3A^%^22278616^%^22^%^2C^%^22ep^%^22^%^3A^%^22^%^22^%^2C^%^22vid^%^22^%^3A^%^229^%^5B^%^3C4KhV^%^3AMa^%^3A^%^23()^%^3CPW^%^2Bq^%^23^%^22^%^2C^%^22ctn^%^22^%^3A^%^22^%^22^%^7D',
            'uniqid': '5a7b97b211066',
            'from_data': 'YTo1OntzOjQ6Imhvc3QiO3M6MTM6Ind3dy5iYWlkdS5jb20iO3M6Mzoic2VtIjtiOjA7czoxMDoic291cmNlZnJvbSI7aTowO3M6NDoid29yZCI7TjtzOjM6ImtpZCI7aTowO30^%^3D',
            'resource_number_data20180208': '1460395^%^2C1332047^%^2C76128^%^2C45650^%^2C9805^%^2C10617',
            'uv_cookie': '1e7dcf4316d6d64b2ce72e5c2b5bd028',
            's_token': '47a002cc048f6ae05f936e0f57d6d2f7',
            'is_click_activity': '1',
            'isSearch': '0',
            'isVip': '0',
            'isPay': '0',
            'session_data': 'YTo1OntzOjM6InVpZCI7czo2OiIyNTYxMjYiO3M6NToidG9rZW4iO3M6MzI6IjdiM2IwYzhjNDMyNjA2ZjNkZjlhMTJmNmU5YmZhMTI0IjtzOjM6InV1dCI7czozMjoiNjU1YzI4ZGQwZTg3YTYxYmQwZjAxNGJiMTk2NWYzMTciO3M6NDoiZGF0YSI7YToxOntzOjg6InVzZXJuYW1lIjtzOjIwOiLpvormsKNg5bCb77yG6L6l44G1ICI7fXM6NjoiZXh0aW1lIjtpOjE1MTg2ODMxODI7fQ^%^3D^%^3D',
            'username': '^%^E9^%^BE^%^8A^%^E6^%^B0^%^A3^%^60^%^E5^%^B0^%^9B^%^EF^%^BC^%^86^%^E8^%^BE^%^A5^%^E3^%^81^%^B5+',
            'uid': '256126',
            'is_qy_vip': '1',
            'search_video_kw': '^%^E6^%^96^%^B0^%^E5^%^B9^%^B4',
            'PHPSESSID': '4643idt91mepkg6muffcgbkmv1610549',
            'login_user': '1',
            'Qs_lvt_135734': '1518049202^%^2C1518049886^%^2C1518078347^%^2C1518102489',
            'Hm_lvt_ddcd8445645e86f06e172516cac60b6a': '1518049203,1518049887,1518078348,1518102490',
            'Hm_lvt_1154154465e0978ab181e2fd9a9b9057': '1518049203,1518049887,1518078348,1518102490',
            'Qs_pv_135734': '665634284627190400^%^2C4550128524240184300^%^2C748973623841536300^%^2C3648418536209805000^%^2C3936988818086429700',
            'Hm_lpvt_ddcd8445645e86f06e172516cac60b6a': '1518102506',
            'Hm_lpvt_1154154465e0978ab181e2fd9a9b9057': '1518102506',
        }

        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://699pic.com/',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }
    def send_request(self,url):
        response = requests.get(url = url, headers=self.headers, cookies=self.cookies)
        return response.content.decode('utf-8')

    def collect_category_url(self,response):
        '''收集所有类url'''
        html = etree.HTML(response)
        categoty_url_li = html.xpath('//div[@class="nav-row"]/div/a/@href')
        return categoty_url_li

    def start_ategory(self,categoty_url_li):
        for url in categoty_url_li[:1]:
            response = self.send_request(url)
            html = etree.HTML(response)
            image_url_li = html.xpath('//*[@id="wrapper"]/div[3]/div[2]/div/a/@href')
            print(image_url_li)


    def main(self):
        url = 'http://699pic.com/photo/'
        response = self.send_request(url)
        categoty_url_li = self.collect_category_url(response)
        self.start_ategory(categoty_url_li)


if __name__ == '__main__':
    shetu = SheTuWang()
    shetu.main()


