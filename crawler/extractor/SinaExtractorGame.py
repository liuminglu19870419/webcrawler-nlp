#encoding: utf-8
'''
Created on 2015年11月17日

@author: lml
'''

from selenium import webdriver

from extractor.BaseExtractor import BaseExtractor
from config.CommonConfig import PHANTOMJS_PATH, NEWS_URL_QUEUE
from config.LogConfig import LOGGER_EXTRACTOR as LOGGER
from utils.dbmysql import MysqlClient
import traceback
from extractor.NewsPublisher import NewsPublisher
import time

class SinaExtractorGame(BaseExtractor):
 
    def __init__(self, config):
        super(SinaExtractorGame, self).__init__(config)

    def extract_links(self):
        try:
            driver = webdriver.PhantomJS(PHANTOMJS_PATH)
#             driver = webdriver.Firefox()
            LOGGER.debug("start extractor from %s" %(self.url, ))
            driver.get(self.url)
            
            list = [] #extract url list
            
            stop_flag = True #
            republishdThre = 5 #find 5 duplicated article stop extractor urls
            republishedCount = 0
         
            js = "var q=document.documentElement.scrollTop=8000"
            driver.execute_script(js)
            driver.implicitly_wait(0)
  
            js = "var q=document.documentElement.scrollTop=0"
            driver.execute_script(js)
            driver.implicitly_wait(0)
            
#             main_section = driver.find_element_by_css_selector("div[class=\"footer\"]")

#             link_list2 = driver.find_elements_by_css_selector("div[class=\"news-item\"]")
            link_list = driver.find_element_by_class_name("page1").find_elements_by_class_name("row")
#             link_list = link_list + link_list2
#                 link_list = main_section.find_elements_by_tag_name("h2")
            
            print len(link_list)
    
            for elem in link_list:
                title = elem.find_element_by_class_name("list-tt").find_element_by_tag_name("a").text # article title
                if title not in list:
                    LOGGER.debug("article title %s"%(title))
                    url = elem.find_element_by_class_name("list-tt").find_element_by_tag_name("a").get_attribute("href")
                    LOGGER.info("url:%s"%(url))
    
                    url_is_exists = self.isPublished(url)
                    if url_is_exists is False:
                        
                        abstract = elem.find_element_by_class_name("f4").text
                        # published the url msg to mq
                        msg = self.formatMsg(url, self.tag, self.sub_tag, title, abstract)
                        self.publishMsg(msg)
    
                    else: # else the remain urls were already published
                        republishedCount += 1
                        if republishedCount >= republishdThre:
                            stop_flag = False
                            break
                    list.append(title)
                        
                else:
                    continue

        except Exception, e:
            LOGGER.error(traceback.format_exc())
        finally:
            driver.quit()