#encoding: utf-8
'''
Created on 2015年11月17日

@author: lml
'''

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

if __name__ == '__main__':

    try:
        driver = webdriver.PhantomJS("/home/lml/phantomjs/bin/phantomjs")
#         driver.set_page_load_timeout(5)
#         driver.
        driver.get('http://news.163.com/world/')
        js = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)
        js = "var q=document.documentElement.scrollTop=0"
        driver.execute_script(js)

        list = []
        i = 0
        while i < 5:
            link_content = driver.find_element_by_css_selector("div[class=\"tab-con current\"]")
            link_list = link_content.find_elements_by_css_selector("div[class=\"list-item clearfix\"]")
            for elem in link_list:
                title = elem.find_element_by_tag_name("h2")
                if title not in list:
                    print title.text
                    url = title.find_element_by_tag_name("a").get_attribute("href")
                    print url
                    content = elem.find_element_by_class_name("item-Text")
                    print content.text
                    list.append(title)
                else:
                    continue

            next_page = driver.find_element_by_id("add-more-id")
            next_page.click()
            driver.implicitly_wait(5)
            i += 1
        
    except Exception:
        pass
    finally:
        driver.quit()
