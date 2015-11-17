'''

@author: mingliu
'''
import time
import os
import sys
sys.path.append('..')
from messagequeue.MessageHandler import MessageHandler
from messagequeue.HandlerRepository  import  HandlerRepository
from multiprocessing import *

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
        print '[Consumer%d] received message: %s' % (os.getpid(), msg)
        # send response message
            
class Producer():
    def __init__(self, message_key,message_auth  = None):
        self.handlerRepository = HandlerRepository()
        if message_auth != None:
            self.handlerRepository.init_Message(message_key, message_auth)
        self.message_key = message_key
    def start(self,log_config):
        while True:
            self.process()
    def process(self):
        now = int(time.time())
        msg = {
            'id': now,
            'name': 'producer %s' % (now % 10),
            'phone': now,
            '__priority': (now % 3),
        }
        if self.handlerRepository.process(self.message_key, msg):
            print '[Publish %d] received message: %s %s'   % (os.getpid(), self.message_key,msg)

if __name__ == '__main__':
    LOGGING = {
    'version': 1
    }
    consumerList = []
    producerList = []
    num = 10
    for i in range(num):
        consumer = Consumer()
        consumer.setInPutMessage('test_message' + str(i))
        consumerList.append(consumer)
    for i in range(num):
        producer = Producer('test_message' + str(i))
        producerList.append(producer)
#     for producer in producerList:
#         Process(target=producer.start, args=(LOGGING)).start();

#     for consumer in consumerList:
#         Process(target=consumer.start, args=(LOGGING)).start();

    Process(target=producerList[0].start, args=(LOGGING)).start();
    Process(target=consumerList[0].start, args=(LOGGING)).start();