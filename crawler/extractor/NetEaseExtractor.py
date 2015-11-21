#encoding: utf-8
'''
Created on 2015年11月17日

@author: lml
'''

from selenium import webdriver

from extractor.BaseExtractor import BaseExtractor
from config.CommonConfig import PHANTOMJS_PATH
from config.LogConfig import LOGGER
from utils.dbmysql import MysqlClient
import traceback

class NetEaseExtractor(BaseExtractor):
    def __init__(self, config):
        self.url = config.get("url", "")
        self.tag = config.get("tag", "defaut tag")
        self.sub_tag = config.get("sub_tag", None)
        self.mysql_client = MysqlClient()

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

            while i < 10 and stop_flag:

                # find the article title section
                link_content = driver.find_element_by_css_selector("div[class=\"tab-con current\"]")
                # find the article titles
                link_list = link_content.find_elements_by_css_selector("div[class=\"list-item clearfix\"]")
    
                for elem in link_list:
                    title = elem.find_element_by_tag_name("h2")
                    if title not in list:
                        print title.text # article title
                        LOGGER.debug("article title %s"%(title.text))
                        
                        url = title.find_element_by_tag_name("a").get_attribute("href")
                        LOGGER.info("url:%s"%(url))

                        url_is_exists = self.mysql_client.getOne("select * from published_url where url=%s", (url, ))
                        if url_is_exists is False:
                            self.mysql_client.insertOne("insert into published_url(url, tag, sub_tag) values(%s, %s, %s)",  (url, self.tag, self.sub_tag));
#                             content = elem.find_element_by_class_name("item-Text")
                            # published the url msg to mq

                        else: # else the remain urls were already published
                            stop_flag = False
                            break
                        list.append(title)
                    else:
                        continue

                # load the next page
                next_page = driver.find_element_by_id("add-more-id")
                next_page.click()
                driver.implicitly_wait(5)
                i += 1

        except Exception, e:
            LOGGER.error(traceback.format_exc())
        finally:
            driver.quit()