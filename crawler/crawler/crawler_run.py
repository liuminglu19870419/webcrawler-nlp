#encoding: utf-8
'''
Created on 2015年11月22日

@author: lml
'''

import sys
import threading
sys.path.append("../")
sys.path.append("../../")
sys.path.append("/home/lml/webcrawler/webcrawler-nlp/crawler/")
from config.CommonConfig import CRAWLER_THREAD_COUNT
from utils.daemon import Daemon, daemon_main
import os
from crawler.BasicCrawler import CrawlerMessageHandler, NetEaseNewsCrawler,\
    NetEaseNewsCrawlerPlay, YouminNewsCrawler, SinaNewsCrawler,\
    SinaNewsCrawlerMili, SinaNewsCrawlerGame, ChinaNewsCrawler, HuanQiuCrawler
from config.LogConfig import LOGGER_CRAWLER as LOGGER
import traceback

crawlerMapper = {
                                    "163":{
                                           "world":NetEaseNewsCrawler(),
                                           "domestic":NetEaseNewsCrawler(),
                                           "shehui":NetEaseNewsCrawler(),
                                           "tech":NetEaseNewsCrawler(),
                                           "mili":NetEaseNewsCrawler(),
                                           "play":NetEaseNewsCrawlerPlay(),
                                           },
                                "youmin":{
                                          "online":YouminNewsCrawler(),
                                          "pcgame":YouminNewsCrawler(),
                                          "tvgame":YouminNewsCrawler(),
                                          },
                                "sina":{
                                        "world":SinaNewsCrawler(),
                                        "domestic":SinaNewsCrawler(),
                                        "shehui":SinaNewsCrawler(),
                                        "mili":SinaNewsCrawlerMili(),
                                        "tech":SinaNewsCrawlerMili(),
                                        "yule":SinaNewsCrawlerMili(),
                                        "sport":SinaNewsCrawlerMili(),
                                        "play":SinaNewsCrawlerGame(),
                                        },
                                "chinanews":{
                                        "world":ChinaNewsCrawler(),
                                        "domestic":ChinaNewsCrawler(),
                                        "shehui":ChinaNewsCrawler(),
                                        "mili":ChinaNewsCrawler(),
                                        "tech":ChinaNewsCrawler(),
                                        "yule":ChinaNewsCrawler(),
                                        "sport":ChinaNewsCrawler(),
                                        "yaowen":ChinaNewsCrawler(),
                                        },
                                   "huanqiu":{
                                        "world":HuanQiuCrawler(),
                                        "domestic":HuanQiuCrawler(),
                                        "shehui":HuanQiuCrawler(),
                                        },
                            }
class Crawler(Daemon):
    '''
    classdocs
    '''
    
    def __init__(self, pidfile, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull ):
        super(Crawler, self).__init__(pidfile , stdin, stdout, stderr)

    def run(self):
        try:
            LOGGING = {'version': 1   }
            QUEUE_NAME = "news_article"
            LOGGER.info("start the news crawler")
            threadCount = CRAWLER_THREAD_COUNT
            messageHandlerList = []
            workThreadList = []
            for _ in range(threadCount):
                messageHandler = CrawlerMessageHandler(crawlerMapper)
                messageHandler.set_inputmessage(QUEUE_NAME)
                messageHandlerList.append(messageHandler)
                workerThread = threading.Thread(target=messageHandler.start,args=(LOGGING))
                workerThread.start()
                workThreadList.append(workerThread)
            
            for worker in workThreadList:
                worker.join()
                
        except Exception,e:
            LOGGER.error(traceback.format_exc())
        finally:
            LOGGER.info("end the news crawler")

if __name__ == "__main__":
#     daemon_main(Crawler, 'c', sys.argv)
    crawler = Crawler("./")
    crawler.run()