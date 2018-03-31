# coding:utf-8
import requests

cookies = {
    'pageReferrInSession': '',
    '_ga': 'GA1.2.1767602614.1522388849',
    '_gid': 'GA1.2.1487470839.1522388849',
    'optimizelyEndUserId': 'oeu1522388851451r0.22347821426051717',
    'f_b_h': 'Wdt/xe6Klkzi8plVcJnZ8Q==',
    'route': 'b1e40ca256c0f143a11445951141f891',
    'c_lb_v': '20180328120001',
    'c_lb_l_ts': '5',
    'c_w_n_g_p': '0',
    'JSESSIONID': '74C9849B0FEF539E50DC6FC75B0082E8-n1.n-2-2',
    'c_lb_s_s': 'narrow',
    'pt_s_47cd0d12': 'vt=1522482419876&cad=',
    'c_lb_l_l_ts': '1',
    'pt_47cd0d12': 'uid=HlrgrIERPXRrYVz9XcrWQA&nid=0&vid=uWyNsfdF29yWT8wSCx5UHQ&vn=7&pvn=4&sact=1522482461817&to_flag=0&pl=vl4GrtjLDyf4CZtqkQkdMw*pt*1522482419876',
}

headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'X-CSRF-TOKEN': '9c0794ee-eac6-4b61-9286-3b9d8c2b1ed9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://www.gucci.cn/zh/ca/women/handbags/top-handles',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

params = {
    'pn':'1',
    'ni':'27',
    '_':'1522482419752'
}

url = 'https://www.gucci.cn/zh/itemList?'
response = requests.get(url = url, params = params,cookies = cookies,headers=headers).content.decode('utf-8')


print(response)
