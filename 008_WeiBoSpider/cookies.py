#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import base64
import rsa
import binascii
import requests
import re
import random
import redis
import logging
from config import ACCOUNT_POOL
try:
    from PIL import Image
except:
    pass
try:
    from urllib.parse import quote_plus
except:
    from urllib import quote_plus

class Cookies(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'}
        self.session = requests.session()
        # 访问 初始页面带上 cookie
        index_url = "http://weibo.com/login.php"
        try:
            self.session.get(index_url, headers=self.headers, timeout=2)
        except:
            self.session.get(index_url, headers=self.headers)
        self.redis=redis.Redis(host='127.0.0.1', port=6379, db=1)

    def get_su(self,username):
        """
        对 email 地址和手机号码 先 javascript 中 encodeURIComponent
        对应 Python 3 中的是 urllib.parse.quote_plus
        然后在 base64 加密后decode
        """
        username_quote = quote_plus(username)
        username_base64 = base64.b64encode(username_quote.encode("utf-8"))
        return username_base64.decode("utf-8")

    # 预登陆获得 servertime, nonce, pubkey, rsakv
    def get_server_data(self,su):
        pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
        pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="
        pre_url = pre_url + str(int(time.time() * 1000))
        pre_data_res = self.session.get(pre_url, headers=self.headers)

        sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))

        return sever_data

    def get_password(self,password, servertime, nonce, pubkey):
        rsaPublickey = int(pubkey, 16)
        # print(rsaPublickey)
        key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
        message = message.encode("utf-8")
        passwd = rsa.encrypt(message, key)  # 加密
        passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
        return passwd

    def get_cha(self,pcid):
        cha_url = "http://login.sina.com.cn/cgi/pin.php?r="
        cha_url = cha_url + str(int(random.random() * 100000000)) + "&s=0&p="
        cha_url = cha_url + pcid
        cha_page = self.session.get(cha_url, headers=self.headers)
        with open("cha.jpg", 'wb') as f:
            f.write(cha_page.content)
            f.close()
        try:
            im = Image.open("cha.jpg")
            im.show()
            im.close()
        except:
            print(u"请到当前目录下，找到验证码后输入")

    def login(self,username, password):
        # su 是加密后的用户名
        su = self.get_su(username)
        sever_data = self.get_server_data(su)
        servertime = sever_data["servertime"]
        nonce = sever_data['nonce']
        rsakv = sever_data["rsakv"]
        pubkey = sever_data["pubkey"]
        showpin = sever_data["showpin"]
        password_secret = self.get_password(password, servertime, nonce, pubkey)

        postdata = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
            'vsnf': '1',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': password_secret,
            'sr': '1366*768',
            'encoding': 'UTF-8',
            'prelt': '115',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
            }
        login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        if showpin == 0:
            login_page = self.session.post(login_url, data=postdata, headers=self.headers)
        else:
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            pcid = sever_data["pcid"]
            self.get_cha(pcid)
            postdata['door'] = input(u"请输入验证码")
            login_page = self.session.post(login_url, data=postdata, headers=self.headers)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        login_loop = (login_page.content.decode("GBK"))
        # print(login_loop)
        pa = r'location\.replace\([\'"](.*?)[\'"]\)'
        loop_url = re.findall(pa, login_loop)[0]

        login_index = self.session.get(loop_url, headers=self.headers)
        uuid = login_index.content.decode('gbk')
        # 获取用户id
        logging.warning('put cookie over')
        try:
            userid = re.findall(r'"uniqueid":"(.*?)"', uuid, re.S)[0]
        except Exception as e:
            logging.warning('账号异常，请及时处理！')
            print(uuid)
            logging.warning(e)
        else:
            cookie = self.session.cookies.get_dict()
            # return userid,cookie
            self.save_cookie_to_redis(userid,cookie)

    def save_cookie_to_redis(self,userid,cookie):
        self.redis.hset('cookie',userid,cookie)
        logging.warning("save one cookies in redis!")


    def main(self):
        for ACCOUNT in ACCOUNT_POOL:
            username = ACCOUNT[0]
            password = ACCOUNT[1]  
            self.login(username, password)

if __name__ == "__main__":
    cookie = Cookies()
    cookie.main()



