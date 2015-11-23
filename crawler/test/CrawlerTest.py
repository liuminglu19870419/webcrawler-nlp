#encoding: utf-8
'''
Created on 2015年11月23日

@author: lml
'''
from config.CommonConfig import VERSION, NEWS_URL_QUEUE
from extractor.NewsPublisher import NewsPublisher
from crawler.crawler_run import Crawler
msgs = [
                {"url":"http://news.163.com/15/1123/18/B94I95JS00014JB5.html",
                  "title":"中央政治局审议《关于打赢脱贫攻坚战的决定》",
                  "tag":"163",
                  "sub_tag":"domestic",
                  "version":VERSION,
                }
            ]
if __name__ == '__main__':
    news_publisher = NewsPublisher(NEWS_URL_QUEUE)
    for  msg in msgs:
        news_publisher.process(msg)
    
    crawler = Crawler("./")
    crawler.run()      
