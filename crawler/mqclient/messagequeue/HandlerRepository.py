#!/usr/bin/env python
'''
@author: mingliu
'''
from exceptions import MQError
import DefaultConfig
from DefaultConfig import load_global_mq_client
from rabbitmq_select_client import Select_Connnection
import threading

class HandlerRepository(object):
    
    def __init__(self, asyn=False, process_handler=None):
        if asyn == True:
            self._handler_repository = AsynHandlerRepository(process_handler=process_handler)
        else:
            self._handler_repository = BlockHandlerRepository()
    
    def init_message(self, message_key, message_auth):
        self._handler_repository.init_message(message_key, message_auth)
        
    def process(self, message_key, message_body=None, **kw):
        return self._handler_repository.process(message_key, message_body, **kw) 
        
    def stop(self):
        self._handler_repository.stop() 


class AsynHandlerRepository(object):
    '''
    publish the message
    '''
    def __init__(self, process_handler=None):
        self.message_key_dict = {}
        self.message_config = DefaultConfig.MESSAGE_CONFIGS
        self.client_config = DefaultConfig.MQ_CLIENT_CONFIG
        self.select_connect = Select_Connnection(process_handler=process_handler) #handler unfinished
        self.is_start = False

    def init_message(self, message_key, message_auth):
        '''
        add authentication to a message_key
        '''
        self.message_key_dict[message_key] = message_auth

    def process(self, message_key, message_body=None, **kw):
        '''
        publish a message use the message_inkey
        '''
        if not self.is_start:
            threading.Thread(target=self.select_connect.start).start()
#             self.select_connection.start()
#             self.select_connect.start()
            self.is_start = True
        message_body = AsynHandlerRepository._fill_message(message_key, message_body, **kw)
        message = {'message_key': message_key,
                       'message_body': message_body}
        self.select_connect.publish(message)
#         print 'publish', message_key, message_body\
        return True    

    def stop(self):
        self.select_connect.value.stop()

    @classmethod
    def _fill_message(cls, message_inkey, message_body=None, **kw):
        '''
        fill the message
        '''
        default_message_config = \
        DefaultConfig.MESSAGE_CONFIGS.get('__default_message_config')
        DefaultConfig.MESSAGE_CONFIGS.setdefault(\
                                         message_inkey, \
                                         default_message_config)
        if message_body is None:
            message_body = {}
        for key, value in kw.items():
            message_body[key] = value

        if len(message_body) == 0:
            raise MQError("empty message not allowed")
        return message_body


class BlockHandlerRepository(object):
    '''
    publish the message
    '''
    def __init__(self):
        self.message_key_dict = {}
        self._connection = load_global_mq_client(True)

    def init_message(self, message_new_key, message_auth):
        '''
        add authentication to a message_key
        '''
        self.message_key_dict[message_new_key] = message_auth

    def process(self, message_inkey, message_body=None, **kw):
        '''
        publish a message use the message_inkey
        '''
        message_auth = self.message_key_dict.get(message_inkey)
        if message_auth != None:
            message_inkey = message_inkey + "_" + str(message_auth)

        message_body = self._fill_message(message_inkey, \
                                          message_body, **kw)
        self._connection.publish(\
                               message_type=message_inkey, \
                               message=message_body, \
                               priority=message_body.get("__priority", 0))
        return True

    @classmethod
    def _fill_message(cls, message_inkey, message_body=None, **kw):
        '''
        fill the message
        '''
        default_message_config = \
        DefaultConfig.MESSAGE_CONFIGS.get('__default_message_config')
        DefaultConfig.MESSAGE_CONFIGS.setdefault(\
                                         message_inkey, \
                                         default_message_config)
        if message_body is None:
            message_body = {}
        for key, value in kw.items():
            message_body[key] = value

        if len(message_body) == 0:
            raise MQError("empty message not allowed")
        return message_body
    
    def stop(self): pass
