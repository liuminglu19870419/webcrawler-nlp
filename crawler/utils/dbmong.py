# encoding: utf-8
'''
Created on 2015年11月16日

@author: lml
'''
import pymongo
from config.CommonConfig import MONGO_IP

class MongoClient(pymongo.MongoClient):
    '''
    mongo client
    '''
    def __init__(self ):
        super(MongoClient, self).__init__(MONGO_IP, 27017)
    
if __name__ == '__main__':
    client = MongoClient()
    test = client.test.test
    test.save({"id":1, "content":"abcdefg"})
    result = test.find_one({"id":1})
    print result