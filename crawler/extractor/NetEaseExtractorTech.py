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

class NetEaseExtractorTech(BaseExtractor):

    def __init__(self, config):
        super(NetEaseExtractorTech, self).__init__(config)

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
#             print driver.find_element_by_tag_name("body").text

            list = [] #extract url list
            
            i = 0 #page count
            stop_flag = True #
            republishdThre = 5 #find 5 duplicated article stop extractor urls
            republishedCount = 0

            while i < 10 and stop_flag:

                # find the article title section
#                 link_content = driver.find_element_by_css_selector("div[class=\"tab-con current\"]")
                # find the article titles
                contents = driver.find_elements_by_class_name("list_txt")
                for content in contents:
                    link_list = content.find_elements_by_tag_name("li")
 
                    for elem in link_list:
                        hrefs = elem.find_elements_by_tag_name("a")
                        title = hrefs[1].text # article title
                        if title not in list:
                            LOGGER.debug("article title %s"%(title))
#                             print title
                            
                            url = hrefs[1].get_attribute("href")
                            LOGGER.info("url:%s"%(url))
    
                            url_is_exists = self.isPublished(url)
                            if url_is_exists is False:
                                
    #                             abstract = elem.find_element_by_class_name("item-Text").text
                                abstract = ""
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
                next_page = driver.find_elements_by_class_name("bar_pages_flip")[1]
                next_page.click()
                driver.implicitly_wait(5)
#                 print driver.find_element_by_tag_name("body").text
                i += 1

        except Exception, e:
            LOGGER.error(traceback.format_exc())
        finally:
            driver.quit()