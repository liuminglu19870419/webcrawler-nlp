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

class NetEaseExtractorPlay(BaseExtractor):
    def __init__(self, config):
        self.url = config.get("url", "")
        self.tag = config.get("tag", "defaut tag")
        self.sub_tag = config.get("sub_tag", None)
        self.mysql_client = MysqlClient()
        self.news_publisher = NewsPublisher(NEWS_URL_QUEUE)

    def extract_links(self):
        try:
            driver = webdriver.PhantomJS(PHANTOMJS_PATH)
#             driver.set_page_load_timeout(10)
            LOGGER.debug("start extractor from %s" %(self.url, ))
            try:
                driver.get(self.url)
            except Exception, e:
                pass
            
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

            while i < 10 and stop_flag:

                # find the article title section
#                 link_content = driver.find_element_by_css_selector("div[class=\"tab-con current\"]")
                # find the article titles
                link_list = driver.find_elements_by_css_selector("div[class=\"m-collist clearfix\"]")
    
                for elem in link_list:
                    article = elem.find_element_by_tag_name("dt")
                    title = article.text # article title
                    if title not in list:
                        LOGGER.debug("article title %s"%(title))
#                         print title
                        
                        url = elem.find_element_by_tag_name("a").get_attribute("href")
                        LOGGER.info("url:%s"%(url))

                        url_is_exists = self.mysql_client.getOne("select * from successed_url where url=%s", (url, ))
                        if url_is_exists is False:
                            
#                             abstract = elem.find_element_by_class_name("item-Text").text
                            abstract = elem.find_element_by_tag_name("dd").text
                            # published the url msg to mq
                            msg = self.formatMsg(url, self.tag, self.sub_tag, title, abstract)
                            self.news_publisher.process(msg)
                            self.mysql_client.insertOne("insert into published_url(url, tag, sub_tag) values(%s, %s, %s)",  (url, self.tag, self.sub_tag));

                        else: # else the remain urls were already published
                            republishedCount += 1
                            if republishedCount >= republishdThre:
                                stop_flag = False
                                break
                        list.append(title)
                    else:
                        continue

                # load the next page
                next_page = driver.find_element_by_class_name("m-collist-more")
                next_page.click()
                driver.implicitly_wait(5)
                i += 1

        except Exception, e:
            LOGGER.error(traceback.format_exc())
        finally:
            driver.quit()