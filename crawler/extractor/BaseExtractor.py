#encoding: utf-8
'''
Created on 2015年11月18日

@author: lml
'''
import time
from utils.dbmysql import MysqlClient
from config.CommonConfig import NEWS_URL_QUEUE, VERSION
from extractor.NewsPublisher import NewsPublisher
from config.LogConfig import LOGGER_EXTRACTOR as LOGGER
import traceback

class BaseExtractor(object):
    '''
    classdocs
    '''

    def __init__(self, config):
        '''
        Constructor
        '''        
        self.url = config.get("url", "")
        self.tag = config.get("tag", "defaut tag")
        self.sub_tag = config.get("sub_tag", None)
        self.mysql_client = MysqlClient()
        self.news_publisher = NewsPublisher(NEWS_URL_QUEUE)
        
    def extract_links(self):
        """
        extractor links from url
        """
    
    def formatMsg(self, url, tag, sub_tag, title, abstract, priority = 0):
        msg = {}
        msg["url"] = url
        msg["tag"] = tag
        msg["sub_tag"] = sub_tag 
        msg["title"] = title
        msg["abstract"] = abstract
        msg["__priority"] = priority
        msg["version"] = VERSION
        msg["create_time"] = int(time.time() * 1000)
        
        return msg
    
    def isPublished(self, url):
        try:
            url_is_exists = self.mysql_client.getOne("select * from published_url where url=%s", (url, ))
            if url_is_exists == False:
                return False
            else:
                return True
        except Exception, e:
            return True
    
    def publishMsg(self, msg):
        try:
            self.news_publisher.process(msg)
            self.mysql_client.insertOne("insert into published_url(url, tag, sub_tag, version, create_time, title, abstract) values(%s, %s, %s, %s, %s, %s, %s)", \
                                         (msg["url"], msg["tag"], msg["sub_tag"], msg["version"], msg["create_time"], msg["title"], msg.get("abstract", "")));
            self.mysql_client.end("commit")
        except Exception, e:
            self.mysql_client.end("rollback")
            LOGGER.error("published msg error: %s" %(msg["url"], ))
            LOGGER.error(traceback.format_exc())
    
#     def reTryFailedList(self):
#         pass