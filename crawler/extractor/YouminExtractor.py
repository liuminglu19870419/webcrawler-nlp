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
from time import sleep

class YouminExtractor(BaseExtractor):
 
    def __init__(self, config):
        super(YouminExtractor, self).__init__(config)

    def extract_links(self):
        try:
            driver = webdriver.PhantomJS(PHANTOMJS_PATH)
            LOGGER.debug("start extractor from %s" %(self.url, ))
            driver.get(self.url)
            
            #scroll bar set from bottom to top, make the page load all
            js = "var q=document.documentElement.scrollTop=10000"
            driver.execute_script(js)
            js = "var q=document.documentElement.scrollTop=0"
            driver.execute_script(js)

            list = [] #extract url list
            
            i = 0 #page count
            stop_flag = True #
            republishdThre = 5 #find 5 duplicated article stop extractor urls
            republishedCount = 0
            
#             next = 0
#             while next < 2:
#                 #click the next button three times to get the full article list
#                 
#                 next_page = driver.find_element_by_class_name("HomeMore")
#                 next_page_a = next_page.find_element_by_tag_name("a")
#                 print next_page.text
#                 next_page_a.click()
#                 driver.implicitly_wait(5)
#                 next += 1
                
            while i < 3 and stop_flag:

                # find the article title section
#                 link_content = driver.find_element_by_css_selector("div[class=\"tab-con current\"]")
                # find the article titles
                link_list = driver.find_elements_by_css_selector("ul[class=\"pictxt block\"]")[i].find_elements_by_tag_name("li")
    
                for elem in link_list:
                    article = elem.find_element_by_class_name("tit")
                    title = article.text # article title
                    if title not in list:
                        LOGGER.debug("article title %s"%(title))
#                         print title
                        
                        url = article.find_element_by_tag_name("a").get_attribute("href")
                        LOGGER.info("url:%s"%(url))

                        url_is_exists = self.isPublished(url)
                        if url_is_exists is False:
                            
#                             abstract = elem.find_element_by_class_name("item-Text").text
                            abstract = elem.find_element_by_class_name("txt").text
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

                # load the next page
                next_page = driver.find_element_by_class_name("HomeMore").find_element_by_tag_name("a")
                next_page.click()
                driver.implicitly_wait(5)
                i += 1

        except Exception, e:
            LOGGER.error(traceback.format_exc())
        finally:
            driver.quit()