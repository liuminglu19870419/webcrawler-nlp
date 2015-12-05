#encoding: utf-8
'''
Created on 2015年11月22日

@author: lml
'''
import os
from mqclient.messagequeue.MessageHandler import MessageHandler
from _ast import Sub
from config.CommonConfig import PHANTOMJS_PATH, HOST_IP, VERSION
from selenium import webdriver
from config.LogConfig import LOGGER_CRAWLER as LOGGER
import traceback
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.dbmysql import MysqlClient
from utils.dbmong import MongoClient

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
        self.mongo_client = MongoClient().tdb.tcoll
    
    def insertSuccess(self, msg):
        """
        success crawle the article msg, insert into the successed db, insert into mongodb
        """
        try:
            self.mysql_client.begin()
#             print article
#             print msg["url"]
            
            article = self.mysql_client.getOne("select * from failed_url where url=%s", (msg["url"], ))
            if article != False:
                article = self.mysql_client.delete("delete from failed_url where url=%s", (msg["url"], ))
                LOGGER.info("delete the article from failed_url: %s", msg["url"])

            article = self.mysql_client.getOne("select * from successed_url where url=%s", (msg["url"], ))
            if article != False:
                LOGGER.info("repeat crawler the article give up save: %s", msg["url"])
                return
            
            self.mongo_client.save(msg)
            LOGGER.debug("insert into mongo: %s@%s" %(msg["title"], msg["url"]))
            
            self.mysql_client.insertOne("insert into successed_url(url, tag, sub_tag, version, create_time) values(%s, %s, %s, %s, %s)",  \
                                        (msg["url"], msg["tag"], msg["sub_tag"], VERSION, msg["create_time"]));
                                        
            LOGGER.debug("insert successed_url %s" %(msg["url"], ))
            self.mysql_client.end("commit")

        except Exception, e:
            self.mysql_client.end("rollback")

            self.mysql_client.begin()
            self.insertFailed(msg)
            LOGGER.error("insert into mongo/successed_url error: %s"  %(msg["url"]))
            LOGGER.error(traceback.format_exc())
    
    def insertFailed(self, msg):
        """
        insert into failed_url
        """
        try:
            self.mysql_client.begin()
            article = self.mysql_client.getOne("select * from failed_url where url=%s", (msg["url"], ))
            if article == False:
                self.mysql_client.insertOne("insert into failed_url(url, tag, sub_tag, version, create_time) values(%s, %s, %s, %s, %s)",  \
                                        (msg["url"], msg["tag"], msg["sub_tag"], VERSION, msg["create_time"]));
                LOGGER.debug("insert failed_url %s" %(msg["url"], ))
            else:
                self.mysql_client.update("update failed_url set count = count+1 where url = %s", (msg["url"], ))
                LOGGER.debug("update failed_url %s" %(msg["url"], ))
            self.mysql_client.end("commit")
                                        
        except Exception, e:
            LOGGER.error(traceback.format_exc())
            self.mysql_client.end("rollback")
    
    def crawlArticle(self, msg):
        """
        crawler the article referer by msg
        """
        
        url = msg["url"]
        try:
            driver = webdriver.PhantomJS(PHANTOMJS_PATH)
            driver.set_page_load_timeout(10)
            LOGGER.debug("start extractor from %s" %(url, ))
            driver.get(url)
            try:
                #scroll bar set from bottom to top, make the page load all
                js = "var q=document.documentElement.scrollTop=10000"
                driver.execute_script(js)
                js = "var q=document.documentElement.scrollTop=0"
                driver.execute_script(js)
                articles = self.pharseContext(driver)
                msg["text"] = articles
                self.insertSuccess(msg)

            except Exception, e:
                LOGGER.error(traceback.format_exc())
                LOGGER.error("url: %s" %(msg["url"],))
                self.insertFailed(msg)
  
        except TimeoutException, e:
            #scroll bar set from bottom to top, make the page load all
            try:
                js = "var q=document.documentElement.scrollTop=10000"
                driver.execute_script(js)
                js = "var q=document.documentElement.scrollTop=0"
                driver.execute_script(js)
#                 title = driver.find_element_by_css_selector("h1[id=\"h1title\"]").text
                articles = self.pharseContext(driver)
                msg["text"] = articles
                self.insertSuccess(msg)
                
            except Exception, e:
                self.insertFailed(msg)
                LOGGER.error(traceback.format_exc())
                LOGGER.error("url: %s" %(msg["url"], ))

        except Exception, e:
            self.insertFailed(msg)
            LOGGER.error(traceback.format_exc())
            LOGGER.error("url: %s" %(msg["url"], ))
        finally:
            driver.quit()
    
    def pharseTitle(self, driver):
        return ""
    
    def pharseAbstract(self, driver):
        return ""
    
    def pharseContext(self, driver):
        """
        """
        return [""]

class NetEaseNewsCrawler(BasicArticleCrawler):
    
    def __init__(self):
        super(NetEaseNewsCrawler, self).__init__()
        
    def pharseContext(self, driver):
        articles_p = driver.find_element_by_id("endText").find_elements_by_tag_name("p")
        articles = map(lambda article : article.text, articles_p)
        return articles


class NetEaseNewsCrawlerPlay(BasicArticleCrawler):
    
    def __init__(self):
        super(NetEaseNewsCrawlerPlay, self).__init__()

    def pharseContext(self, driver):
        articles_p = driver.find_element_by_id("endText").find_elements_by_tag_name("p")
        articles = map(lambda article : article.text, articles_p)
        return articles
    
class YouminNewsCrawler(BasicArticleCrawler):
    
    def __init__(self):
        super(YouminNewsCrawler, self).__init__()
        
    def pharseContext(self, driver):
        articles_p = driver.find_element_by_class_name("Mid2L_con").find_elements_by_tag_name("p")
        articles = map(lambda article : article.text, articles_p)
        return articles

class SinaNewsCrawler(BasicArticleCrawler):
    
    def __init__(self):
        super(SinaNewsCrawler, self).__init__()
        
    def pharseContext(self, driver):
        articles_p = driver.find_element_by_css_selector("div[class=\"page-content clearfix\"]").find_elements_by_tag_name("p")
        articles = map(lambda article : article.text, articles_p)
        return articles

class SinaNewsCrawlerMili(BasicArticleCrawler):
    
    def __init__(self):
        super(SinaNewsCrawlerMili, self).__init__()
        
    def pharseContext(self, driver):
        articles_p = driver.find_element_by_css_selector("div[id=\"artibody\"]").find_elements_by_tag_name("p")
        articles = map(lambda article : article.text, articles_p)
        return articles

class SinaNewsCrawlerGame(BasicArticleCrawler):
    
    def __init__(self):
        super(SinaNewsCrawlerGame, self).__init__()
        
    def pharseContext(self, driver):
        try:
            articles_p = driver.find_element_by_css_selector("div[id=\"artibody\"]").find_elements_by_tag_name("p")
            articles = map(lambda article : article.text, articles_p)
        except NoSuchElementException, e:
            LOGGER.debug(e)
            articles_p = driver.find_element_by_class_name("text").find_elements_by_tag_name("p")
            articles = map(lambda article : article.text, articles_p)
            return articles
        return articles
        
        
   

class ChinaNewsCrawler(BasicArticleCrawler):
    
    def __init__(self):
        super(ChinaNewsCrawler, self).__init__()
        
    def pharseContext(self, driver):
        articles_p = driver.find_element_by_class_name("left_zw").find_elements_by_tag_name("p")
        articles = map(lambda article : article.text, articles_p)
        return articles
        
        

if __name__ == "__main__":
    print repr({"1", 123, "2",323})