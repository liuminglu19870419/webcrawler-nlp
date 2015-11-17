'''

@author: mingliu
'''

from logging import getLogger
from messagequeue.MessageHandler import MessageHandler 
from messagequeue.HandlerRepository import HandlerRepository
from threading import Thread
import time
import logging as log
import sys
import threading

class Consumer(MessageHandler):
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
        print '[Consumer%s] received message: %s' % (threading.current_thread(), msg)
        # send response message


class Producer():

    def __init__(self, message_key, message_auth=None):
        self.handlerRepository = HandlerRepository(False)
        if message_auth != None:
            self.handlerRepository.init_Message(message_key, message_auth)
        self.message_key = message_key

    def start(self, log_config):
#         while True:
        self.process()

    def process(self):
        now = int(time.time())
        msg = {
               'url': 'http://img1.gtimg.com/news/pics/hv1/59/206/1506/97980239.jpg', 
                   'method': 'GET', 
                   'priority': 1, 
                   'headers': {}, 
                   'params': {}, 
                   '__priority': 1, 
                   '__delivery_tag': 1
        }
        time.sleep(1)
        if self.handlerRepository.process(self.message_key, msg):
            print '[Publish %s] received message: %s %s' % (threading.currentThread(), self.message_key, msg)

if __name__ == '__main__':
    LOGGING = {
    'version': 1
    }
    consumerList = []
    producerList = []
    num = 1
    logging = getLogger('pika.adapters.blocking_connection')
    logging.setLevel(log.INFO)
    sh = log.StreamHandler(sys.stderr)
    sh.setLevel(log.DEBUG)
    logging.addHandler(sh)
    producer = Producer('image_crawler')

#     for i in range(num):
#         producer = Producer('test_message')
#         producerList.append(producer)
#     for producer in producerList:
#         Thread(target=producer.start, args=(LOGGING)).start()
#     for i in range(num + 10):
#         consumer = Consumer()
#         consumer.set_inputmessage('test_message')
#         consumerList.append(consumer)
#     for consumer in consumerList:
#         Thread(target=consumer.start, args=(LOGGING)).start()
#     Process(target=producerList[0].start, args=(LOGGING)).start()
#     Process(target=consumerList[0].start, args=(LOGGING)).start()

