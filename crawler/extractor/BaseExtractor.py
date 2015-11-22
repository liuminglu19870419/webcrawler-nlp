#encoding: utf-8
'''
Created on 2015年11月18日

@author: lml
'''
import time

class BaseExtractor(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def extract_links(self):
        """
        extractor links from url
        """
    
    def formatMsg(self, url, tag, sub_tag, title, abstract, priority = 0):
        msg = {}
        msg["url"] = url
        msg["tag"] = tag
        msg["sub_tag"] = sub_tag 
        msg["title"] = title
        msg["abstract"] = abstract
        msg["__priority"] = priority
        return msg