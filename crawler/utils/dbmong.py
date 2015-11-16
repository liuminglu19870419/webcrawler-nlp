# encoding: utf-8
'''
Created on 2015年11月16日

@author: lml
'''
import pymongo

class MongoClient(pymongo.MongoClient):
    '''
    mongo client
    '''
    def __init__(self, ip, port):
        super(MongoClient, self).__init__(ip, port)
    
if __name__ == '__main__':
    client = MongoClient("127.0.0.1", 27017)
    test = client.test.test
    test.save({"id":1, "content":"abcdefg"})
    result = test.find_one({"id":1})
    print result