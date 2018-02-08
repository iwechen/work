#encoding=utf-8
import time
import requests
from lxml import etree
import re 

class LaoShiShiCai(object):
    def __init__(self,server,user,password,database):
        # self.conn = pymssql.connect(server, user, password, database,charset='utf8')
        # self.cursor = self.conn.cursor()
        self.cookies = {
            'test_cookie_enable': 'null',
            '__huid': '10^%^2FsCKtA6ymSh7tuoyzFrVPwVW^%^2BWzgyf0xJZyavVkO4TM^%^3D',
            '__guid': '91251416.638506027805254800.1510113247557.8052',
            '__gid': '133660893.168150516.1510399168128.1510406101850.5',
            'lguid': 'DCF7735C-FF4B-A92E-3954-A022755C8588',
            'monitor_count': '1',
            'message_lightbox_id_154': '154',
        }

        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'If-Modified-Since': 'Mon, 05 Feb 2018 14:05:32 GMT',
        }

        self.params = (
            ('menu^', ''),
            ('r_a', 'ZbQbIj'),
        ) 

    def send_requests(self):
        while True:
            response = requests.get('http://cp.360.cn/ssccq/', headers=self.headers, params=self.params, cookies=self.cookies).text
            html = etree.HTML(response)
            try:
                lottery_years = html.xpath('//div[@class="hd clearfix"]/h1/span/em/text()')[0]
                lottery_month = html.xpath('//div[@class="hd clearfix"]/h3/em/text()')[0]
                lottery_str = lottery_years[:2] + lottery_month
                lottery_num = lottery_str[:6] +'-'+ lottery_str[6:]
                
                num_info = html.xpath('//div[@class="hd clearfix"]/div/ul')[0].xpath('string(.)')
                num_info = re.sub(r'\s','',num_info)
                if not re.match(r'\d{5}',num_info):
                    # print('waitting open!')
                    continue
            except:
                print('目标网站更改规则,请及时修复！')
            else:
                print('第%s期,开奖号码：%s,---->> 采集成功！------->>%s'%(lottery_num,num_info,timetemp))
                return lottery_num,num_info

    def save_to_sql(self,lottery_num,num_info):
        sql = "select lottery_num from KR_Lottery_Code where lottery_num='%s';"%lottery_num
        self.cursor.execute(sql)
        temp= self.cursor.fetchall()
        if temp !=[]:
            # print('shujucunzai!')
            return 
        else:
            timetemp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            sql = "INSERT INTO KR_Lottery_Code(lottery_num,num_info1,num_info2,num_info3,num_info4,num_info5,kjtime) VALUES('%s','%s','%s','%s','%s','%s','%s');"%(lottery_num,num_info[0],num_info[1],num_info[2],num_info[3],num_info[4],timetemp)
            self.cursor.execute(sql)
            self.conn.commit()
            print('第%s期,开奖号码：%s,---->> 采集成功！------->>%s'%(lottery_num,num_info,timetemp))

    def main(self):
        lottery_num,num_info = self.send_requests()
        # self.save_to_sql(lottery_num,num_info)

if __name__ == '__main__':
    server = "127.0.0.1"
    user = "sa"
    password = "qq785900731"
    database="sss"
    lao = LaoShiShiCai(server,user,password,database)
    while True:
        hours = time.strftime('%H',time.localtime(time.time()))
        minute = time.strftime('%M',time.localtime(time.time()))
        if re.match(r'^[0][2-9]$',hours):
            print('02:00-10:00点是休息时间！请等待...')
            continue
            time.sleep(60)
        elif re.match(r'[1][0-9]|[2][0-2]$',hours):
            print('10:00-22:00,每10分钟开奖一次！')
            if re.match(r'.*0$|.*1$',minute):
                lao.main()
                time.sleep(3)
            else:
                time.sleep(10)
                continue
        elif re.match(r'[2][2-3]|[0][0-1]',hours):
            print('22:00-02:00,开奖高峰期，5分钟一次！')
            if re.match(r'.*5$|.*6$',minute):
                lao.main()
            else:
                time.sleep(3)
                continue  







