

#coding=utf-8
import time
from selenium import webdriver

def process_request():
    # 如果url不是首页，再使用Chrome获取数据，否则使用Scrapy发送请求
    # url = "http://s.weibo.com/weibo/%25E6%2596%25B0%25E7%2596%2586%257E%25E5%2593%2588%25E5%25AF%2586&nodup=1&page=2"
    url = 'https://weibo.com/'
    driver = webdriver.Chrome()
    
    
    cookies = {
        'SINAGLOBAL': '1531888812599.662.1514185346553',
        'login_sid_t': '5d0c3df20df6969cd559a9f9b1107118',
        'cross_origin_proto': 'SSL',
        'YF-Ugrow-G0': '1eba44dbebf62c27ae66e16d40e02964',
        '_s_tentry': 'www.baidu.com',
        'Apache': '9879396964238.555.1517276163701',
        'ULV': '1517276163713:6:3:1:9879396964238.555.1517276163701:1515465112553',
        'YF-Page-G0': '091b90e49b7b3ab2860004fba404a078',
        'YF-V5-G0': '4d1671d4e87ac99c27d9ffb0ccd1578f',
        'WBtopGlobal_register_version': '49306022eb5a5f0b',
        'UOR': ',,login.sina.com.cn',
        'un': '15389378206',
        'TC-Page-G0': '42b289d444da48cb9b2b9033b1f878d9',
        'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W58fek8FHHKdj_WcXuPOfxA5JpX5K2hUgL.Fo-NSK.X1K-XS0q2dJLoI0eLxK-L12qL12eLxK.LBo2LB.eLxK-LBo5L12qLxK-LBKBLB-2LxK.L1KnLBoSkeoBESh.t',
        'ALF': '1548832322',
        'SSOLoginState': '1517296322',
        'SCF': 'AjXlxvkVQwWjkRYO13oa5v9O0HiO8bSJV8MbmXcObCKHQv4at8FA_bl4v-2OC_hY4jx25lXYm6lJ36x3c-UnPjk.',
        'SUB': '_2A253dGqTDeRhGeNJ7lsV-SvIzDqIHXVUANtbrDV8PUNbmtANLW2skW9NS6YrshECuDmton0Pb2MA0YuTEpirjnER',
        'SUHB': '0k1CYDXqJYiCmM',
        'wvr': '6',
        'wb_cusLike_5759495476': 'N',
    }
    # time.sleep(2)

    # newwindow='window.open("http://s.weibo.com/weibo/%25E6%2596%25B0%25E7%2596%2586%257E%25E5%2593%2588%25E5%25AF%2586&nodup=1&page=2");'

    # 携带cookie打开
    # driver.add_cookie(cookies)
    driver.get(url)

    html = driver.page_source
    print(html)
    time.sleep(10)
    driver.quit()


    
def main():
    process_request()


if __name__ == '__main__':
    main()

