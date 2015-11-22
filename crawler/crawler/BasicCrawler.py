#encoding: utf-8
'''
Created on 2015年11月22日

@author: lml
'''
import os
from mqclient.messagequeue.MessageHandler import MessageHandler
from _ast import Sub
from config.CommonConfig import PHANTOMJS_PATH, HOST_IP
from selenium import webdriver
from config.LogConfig import LOGGER_CRAWLER as LOGGER
import traceback
from selenium.common.exceptions import TimeoutException
from utils.dbmysql import MysqlClient
from pymongo.mongo_client import MongoClient

class CrawlerMessageHandler(MessageHandler):
    '''
    classdocs
    '''
    
    def __init__(self, mapper):
        self.crawlerMapper = mapper
        super(CrawlerMessageHandler, self).__init__()

    def start(self, log_config, max_threads=1):
        '''
        Override start method for test. NOTICE This is not needed in production.
        '''
        self._worker()
        


    def _process(self, msg):
        '''
        This is the main message process method, normally we have all the process
        logic here
        '''
        url, title, tag, sub_tag, abstract = self.pharseMsg(msg)
        crawler = self.crawlerMapper[tag][sub_tag]
        crawler.crawlArticle(msg)
#         print '[Consumer%d] received message: %s' % (os.getpid(), msg)     
    
    def pharseMsg(self, msg):
        url = msg["url"]
        title = msg["title"]
        abstract = msg["abstract"]
        tag = msg["tag"]
        sub_tag = msg["sub_tag"]
        return url, title,  tag, sub_tag, abstract

class  BasicArticleCrawler(object):
    
    def __init__(self):
        self.mysql_client = MysqlClient()
        self.mongo_client = MongoClient(HOST_IP, 27017)
    
    def insertSuccess(self, msg):
        try:
            self.mysql_client.insertOne("insert into successed_url(url, tag, sub_tag) values(%s, %s, %s)",  (msg["url"], msg["tag"], msg["sub_tag"]));
            LOGGER.debug("insert successed_url %s" %(str(msg), ))
        except Exception, e:
            LOGGER.error(traceback.format_exc())
    
    def insertFailed(self, msg):
        try:
            self.mysql_client.insertOne("insert into failed_url(url, tag, sub_tag) values(%s, %s, %s)",  (msg["url"], msg["tag"], msg["sub_tag"]));
            LOGGER.debug("insert failed_url %s" %(str(msg), ))
        except Exception, e:
            LOGGER.error(traceback.format_exc())
    
    def insertMongodb(self, msg):
        try:
            collection = self.mongo_client.tdb.tcoll
            collection.save(msg)
            LOGGER.debug("insert into mongo: %s@%s" %(msg["title"], msg["url"]))
        except Exception, e:
            LOGGER.error(traceback.format_exc())
    
    def crawlArticle(self, msg):
        pass

class NetEaseNewsCrawler(BasicArticleCrawler):
    
    def __init__(self):
        super(NetEaseNewsCrawler, self).__init__()

    def crawlArticle(self, msg):
        url = msg["url"]
        try:
            driver = webdriver.PhantomJS(PHANTOMJS_PATH)
            driver.set_page_load_timeout(10)
            LOGGER.debug("start extractor from %s" %(url, ))
            driver.get(url)
            #scroll bar set from bottom to top, make the page load all
            try:
                js = "var q=document.documentElement.scrollTop=10000"
                driver.execute_script(js)
                js = "var q=document.documentElement.scrollTop=0"
                driver.execute_script(js)
                articles_p = driver.find_element_by_id("endText").find_elements_by_tag_name("p")
                articles = map(lambda article : article.text, articles_p)
                msg["text"] = articles
                self.insertMongodb(msg)
                self.insertSuccess(msg)
            except Exception, e:
                LOGGER.error(traceback.format_exc())
                LOGGER.error("url: %s" %(msg["url"],))
                self.insertFailed(msg)
                driver.quit()
  
        except TimeoutException, e:
            #scroll bar set from bottom to top, make the page load all
            try:
                js = "var q=document.documentElement.scrollTop=10000"
                driver.execute_script(js)
                js = "var q=document.documentElement.scrollTop=0"
                driver.execute_script(js)
#                 title = driver.find_element_by_css_selector("h1[id=\"h1title\"]").text
                articles_p = driver.find_element_by_id("endText").find_elements_by_tag_name("p")
                articles = map(lambda article : article.text, articles_p)
                msg["text"] = articles
                self.insertMongodb(msg)
                self.insertSuccess(msg)
            except Exception, e:
                self.insertFailed(msg)
                LOGGER.error(traceback.format_exc())
                LOGGER.error("url: %s" %(msg["url"], ))
                driver.quit()
        except Exception, e:
            self.insertFailed(msg)
            LOGGER.error(traceback.format_exc())
            LOGGER.error("url: %s" %(msg["url"], ))
        finally:
            driver.quit()

class NetEaseNewsCrawlerPlay(BasicArticleCrawler):
    
    def __init__(self):
        super(NetEaseNewsCrawlerPlay, self).__init__()

    def crawlArticle(self, msg):
        url = msg["url"]
        try:
            driver = webdriver.PhantomJS(PHANTOMJS_PATH)
            driver.set_page_load_timeout(10)
            LOGGER.debug("start extractor from %s" %(url, ))
            driver.get(url)
            
            try:
#                 print traceback.format_exc()
                js = "var q=document.documentElement.scrollTop=10000"
                driver.execute_script(js)
                js = "var q=document.documentElement.scrollTop=0"
                driver.execute_script(js)
                title = driver.find_element_by_css_selector("h1[class=\"article-h1\"]").text
                articles_p = driver.find_element_by_id("endText").find_elements_by_tag_name("p")
                articles = map(lambda article : article.text, articles_p)
                msg["text"] = articles
                self.insertMongodb(msg)
                self.insertSuccess(msg)
            except Exception, e:
                LOGGER.error(traceback.format_exc())
                LOGGER.error("url: %s" %(msg["url"]))
                self.insertFailed(msg)
                driver.quit()
                pass
        except TimeoutException, e:
            #scroll bar set from bottom to top, make the page load all
            try:
#                 print traceback.format_exc()
                js = "var q=document.documentElement.scrollTop=10000"
                driver.execute_script(js)
                js = "var q=document.documentElement.scrollTop=0"
                driver.execute_script(js)
                title = driver.find_element_by_css_selector("h1[class=\"article-h1\"]").text
                articles_p = driver.find_element_by_id("endText").find_elements_by_tag_name("p")
                articles = map(lambda article : article.text, articles_p)
                msg["text"] = articles
                self.insertMongodb(msg)
                self.insertSuccess(msg)
            except Exception, e:
                LOGGER.error(traceback.format_exc())
                LOGGER.error("url: %s" %(msg["url"]))
                self.insertFailed(msg)
                driver.quit()

        except Exception, e:
            LOGGER.error(traceback.format_exc())
            LOGGER.error("url: %s" %(msg["url"]))
            self.insertFailed(msg)
            driver.quit()
        finally:
            driver.quit()
