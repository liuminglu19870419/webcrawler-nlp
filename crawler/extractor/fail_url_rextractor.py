#encoding: utf-8
'''
Created on 2015年11月24日

@author: lml
'''

import sys
sys.path.append("../")
sys.path.append("../../")
sys.path.append("/home/lml/webcrawler/webcrawler-nlp/crawler/")

from utils.daemon import Daemon, daemon_main
from utils.dbmysql import MysqlClient
from extractor.NewsPublisher import NewsPublisher
from config.CommonConfig import NEWS_URL_QUEUE
from config.LogConfig import LOGGER_EXTRACTOR as LOGGER
import os
import traceback

class FailedExtractor(Daemon):
    '''
    classdocs
    '''
    def __init__(self, pidfile, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull ):
        '''
        Constructor
        '''
        super(FailedExtractor, self).__init__(pidfile , stdin, stdout, stderr)
        
    
    def run(self):
        """
        """
        self.mysql_client = MysqlClient()
        self.news_publisher = NewsPublisher(NEWS_URL_QUEUE)
        self.threhold = 5
        self.page = 14
        LOGGER.info("start re extractor the failed url if count() < %s"%(self.threhold, ))
        failed_count = 0
        try:
            failed_count = self.mysql_client.getOne("select count(*) as c from failed_url where count < %s", (self.threhold, ) )
        except Exception, e:
            LOGGER.error("failed to load the failed url count")
            LOGGER.error(traceback.format_exc())
        failed_count = int(failed_count["c"])
        count = 0
        while count < failed_count:
            try:
                print count
                urls = self.mysql_client.getAll("select * from failed_url where count < %s limit %s, %s", (self.threhold, count, self.page))
                if urls == False:
                    break
                count += len(urls)
                for url in urls:
                    LOGGER.info("re extractor url: %s"%(url["url"], ))
                    msg = self.mysql_client.getOne("select abstract, title from published_url where url = %s", (url["url"], ))
                    url["title"] = msg["title"]
                    url["abstract"] = msg["abstract"]
                    self.news_publisher.process(url)
            except Exception, e:
                LOGGER.error("re extractor urls error")
                LOGGER.error(traceback.format_exc())
        

if __name__ == "__main__":
#     failedExtractor = FailedExtractor("./")
#     failedExtractor.run()
    daemon_main(FailedExtractor, "failed", sys.argv)