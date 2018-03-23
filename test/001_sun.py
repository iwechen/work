import requests
import  threading
from lxml import etree
from six.moves import queue
class BaiduNews(object):
    def __init__(self):
        self._url_task_queue = queue.Queue(10)
        self.cookies = {
            'BAIDUID': '8BC13B61591B44D6BA10747B48CB94FD:FG=1',
            'BIDUPSID': '8BC13B61591B44D6BA10747B48CB94FD',
            'PSTM': '1520752380',
            '__cfduid': 'd3c9da4e037ab059700df91be0e3f5f9d1520776838',
            'BDUSS': 'FabGRCbmx4YW5PTjBVUFQxUk1CcTJRQTNRSHFxV0ZjN3NtczZiUFhjVmV4TXhhQVFBQUFBJCQAAAAAAAAAAAEAAADd0U6CsK7QprXE0KHSu7rFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF43pVpeN6VaSD',
            'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
            'BDRCVFR[feWj1Vr5u3D]': 'I67x6TjHwwYf0',
            'PSINO': '1',
            'LOCALGX': '%u5317%u4EAC%7C%30%7C%u5317%u4EAC%7C%30',
            'Hm_lvt_e9e114d958ea263de46e080563e254c4': '1521634807',
            'Hm_lpvt_e9e114d958ea263de46e080563e254c4': '1521634807',
            'BD_CK_SAM': '1',
            'H_PS_PSSID': '',
            'BDRCVFR[C0p6oIjvx-c]': 'mbxnW11j9Dfmh7GuZR8mvqV',
            'BDSVRTM': '108',
        }

        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://news.baidu.com/ns?word=%E6%91%A9%E6%8B%9C&pn=20&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0&rsv_page=1',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }

    def load_url(self,page):
        params = {
            'word': '摩拜',
            'pn': page,
            'cl': 2,
            'ct': 1,
            'tn': 'news',
            'rn': '20',
            'ie': 'utf-8',
            'bt': 0,
            'et': 0,
            'rsv_page': 0,
            }

        response = requests.get('http://news.baidu.com/ns', params = params,headers=self.headers).content.decode('utf-8')

        html = etree.HTML(response)

        news_url_li = html.xpath('//div[@id="content_left"]/div/div/h3/a/@href')

        self._url_task_queue.put(news_url_li)

    def load_news(self):
        while True:
            news_url_li = self._url_task_queue.get()
            for news_url in news_url_li:
                print(news_url)
                response = requests.get(url = news_url,headers = self.headers).content
                try:
                    ret = response.decode('utf-8')
                except Exception as e:
                    ret = response.decode('gb2312')
                finally:
                    html = etree.HTML(ret)
                    text_li = html.xpath('//body')[0].xpath('string(.)')
                    print(text_li)
                    # for text in text_li:
                    #     content = text.xpath('string(.)')
                    #     print(len(content))
                    #     print(content)
                    #     print('------------------')
                

    def init(self):
        t = threading.Thread(target=self.load_news)
        t.setDaemon(True)
        t.start()

    def run(self):
        self.init()
        for page in range(0,1000,20):
            print('第 %d 页'%(page/20))
            self.load_url(page)

    def main(self):
        self.run()


if __name__=='__main__':
    news = BaiduNews()
    news.main()






