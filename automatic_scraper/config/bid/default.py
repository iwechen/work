# coding: utf-8

import hashlib
import time

db_config = {
<<<<<<< HEAD
    'host': '101.200.58.91',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'bid_data',
=======
    'host': '101.200.53.168',
    'port': 3306,
    'user': 'wangwei',
    'password': 'ww250369',
    'database': 'autometic_spider',
>>>>>>> origin/dev_wangwei
    'table': 'zhaotoubiao'
}

def to_utf8_bytes(text):
    if isinstance(text, basestring):
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        else:
            pass
    else:
        text = str(text)
    return text

def process_item(item):
    """
    存数据库前处理item
    :param item:
    :return:
    """
    if not item.get('url'):
        return
    md5 = hashlib.md5()
    to_hash = map(to_utf8_bytes, [item['title'], item['url'], item['issue_time']])
    md5.update(''.join(to_hash))
    item['hash_code'] = md5.hexdigest()
    item['insert_time'] = int(time.time())
