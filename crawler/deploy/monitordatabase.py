#encoding: utf-8
'''
Created on 2015年12月2日

@author: lml
'''

import sys
sys.path.append("../")
sys.path.append("../../")
sys.path.append("/home/lml/webcrawler/webcrawler-nlp/crawler/")
from utils.dbmong import MongoClient
from utils.dbmysql import MysqlClient
from time import sleep


if __name__ == '__main__':
    while True:
        print "**************************************************"
        mysql_client = MysqlClient()
        mongo_client =  MongoClient()
        published_url_count  = mysql_client.getOne("select count(*) as count from published_url")
        print "published url count: %s"%published_url_count["count"]
        
        successed_url_count  = mysql_client.getOne("select count(*) as count from successed_url")
        print "successed url count: %s"%successed_url_count["count"]
        
        failed_url_count  = mysql_client.getOne("select count(*) as count from failed_url")
        print "failed url count: %s"%failed_url_count["count"]
        
        count = mongo_client.tdb.tcoll.count()
        print "mongo articles: %s"%count
        sleep(10)
        print ""