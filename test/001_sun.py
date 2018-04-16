import pymongo


class MongoC(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = self.client['bihu']
        self.collection = self.db['data']
        self.collection1 = self.db['datas']


    def main(self):
        for i in self.collection.find({},{'_id':0}):
            try:
                print(i)
                self.collection1.insert(i)
                print('succerp')
                print(i.keys())
            
            except Exception as e:
                print(e)
                print(len(i.keys()))


if __name__=='__main__':
    m = MongoC()
    m.main()
