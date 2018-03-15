# coding: utf-8
import os
# 爬虫作者及邮箱
author_mails = {
    'Nathan': 'n@sequee.com',
    'Denglixi': 'denglixi@sequee.com',
    'WangWei': 'wangwei@sequee.com',
    'lihailin': 'lihailin@sequee.com',
    'lidongjie': 'lidongjie@sequee.com',
    'huangtaiwu': 'huangtaiwu@sequee.com',
    'liriqing': 'liriqing@sequee.com',
    'Arthur': 'wangwei@sequee.com',
    'Max': 'xiahaijiao@sequee.com',
    'liuweiliang': 'liuweiliang@sequee.com',
    'zuoteng': 'zuoteng@sequee.com',
}

# 邮件抄送地址
# cc_addr = ["bug_cc@sequee.com"]
cc_addr = ["n@sequee.com"]

# 日常爬虫启动时间
HOUR = 10
MIN = 50
SEC = 00

# 实时爬虫启动时间间隔，单位为秒
task_config = {
    "country_zfcg_config_fre": 60,
}

# 爬虫目录, 'bid' + os.sep + 'Denglixi'
spider_path = 'bid' + os.sep + 'zuoteng'


SERVER_FLAG = True