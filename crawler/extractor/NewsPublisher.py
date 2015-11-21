#encoding: utf-8
'''
Created on 2015年11月21日

@author: lml
'''
import time
import os
import sys
sys.path.append('..')
from mqclient.messagequeue.HandlerRepository  import  HandlerRepository
from config.LogConfig import LOGGER

class NewsPublisher(object):
    '''
    published news to rabbitmq
    '''
    def __init__(self, message_key,message_auth  = None):
        self.handlerRepository = HandlerRepository()
        if message_auth != None:
            self.handlerRepository.init_Message(message_key, message_auth)
        self.message_key = message_key

    def process(self, msg):
        now = int(time.time())
        msg["id"] = time.time()

        if self.handlerRepository.process(self.message_key, msg):
            LOGGER.info('[Publish %d] received message: %s %s'   % (os.getpid(), self.message_key,msg))

if __name__ == "__main__":
    publisher = NewsPublisher("key")
    msg = {"test":"test"}
    while 1:
        publisher.process(msg)