#encoding: utf-8
'''
Created on 2015年12月2日

@author: lml
'''

import sys
from pymongo.mongo_client import MongoClient
sys.path.append("../")
sys.path.append("../../")
sys.path.append("/home/lml/webcrawler/webcrawler-nlp/crawler/")
import MySQLdb

if __name__ == '__main__':
    datahost = "192.168.1.101"
    mysql_client = MySQLdb.connect(host=datahost, user="root",passwd="lml19870419", db="test",charset="utf8")
    cursor = mysql_client.cursor()
    mongo_client = MongoClient(datahost, 27017)
    result = raw_input("remove all data for %s? "%datahost)
    if result != "YES":
        pass
    else:
        print "truncate failed_url:"
        cursor.execute("truncate failed_url")
    
        print "truncate successed_url:"
        cursor.execute("truncate successed_url")
    
        print "truncate published_url:"
        cursor.execute("truncate published_url")
        
        print "truncate mongo articles:"
        mongo_client.tdb.tcoll.remove()