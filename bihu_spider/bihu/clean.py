#coding:utf-8
'''
Created on 2018年4月3日
@author: chenwei
Email:iwechen123@gmail.com
'''

import pymongo
import urllib.parse
import time
import re
import signal
import logging
logger = logging.getLogger(__name__)

class BihuClean(object):
    '''
    输入：帖子id
    功能：输入id，查找mongo数据库，清洗content内容
    存储：mongodb
    '''
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = self.client['bihu']
        self.collection = self.db['datas']

    def _read(self,aid):
        try:
            for i in self.collection.find({'id':aid}):
                _id = i['_id']
                content = i['content']
                contents = re.sub(r'\n','<br>',content)
                contents = re.sub(r'class=\".*?\"','',contents)
                contents = re.sub(r'style=\".*?\"|style=\'.*?\'','',contents)
                contents = re.sub(r'<p></p>','',contents)
                contents = re.sub(r'&nbsp;','',contents)
                contents = re.sub(r'\?x-oss-process=style/size_lg','',contents)
                contents = re.sub(r'<span ></span>','',contents)
                contents = re.sub(r'<p ></p>|<p></p>|<o:p></o:p>','',contents)
                contents = re.sub(r'lang=\".*?\"','',contents)
                contents = re.sub(r'<w:.*?>.*?</w:.*?>','',contents)
                contents = re.sub(r'align=\".*?\"','',contents)

                self.collection.update({'_id':_id}, {'$set':{'content':contents}})
                logger.info('%s clean successful!!!',aid)
                # print(contents)
        except Exception as e:
            logger.warn(e)
        try:
            for i in self.collection.find({'id':aid})[0]:
                print(i)
        except Exception as e:
            print(e)


    def run(self,aid):
        self._read(aid)

    def main(self):
        for i in self.collection.find():
            aid = i['id']
            aid = 23456
            # print(aid)
            self.run(aid)
            time.sleep(100000)

if __name__=='__main__':
    clean = BihuClean()
    clean.main()

