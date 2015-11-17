#coding: UTF-8
'''

@author: mingliu
'''
import logging as log
from logging import getLogger

import simplejson
import pika
import multiprocessing
import datetime
import time
import sys
from exceptions import MQError
import DefaultConfig
from utils import datetime2timestamp



#################################################
logging = getLogger('mqclient')
#################################################

def dumps_jsonx(dict_obj):
    appends = []
    for key, value in dict_obj.items():
        if key.endswith("__"):
            if not isinstance(value, str):
                raise MQError("append fields must be str, %s" % key)
            dict_obj[key] = [len(appends), len(value)]
            appends.append(value)

    main = simplejson.dumps(dict_obj)
    if len(main) > 0xffffffff:
        raise MQError("dumps_jsonx length exceeded 0xffffffff")

    prefix = "%08x" % (len(main))
    return ''.join([prefix, main] + appends)


class Select_Connnection(object):

    def __init__(self, process_handler=None, message_config=DefaultConfig.MESSAGE_CONFIGS, client_config=DefaultConfig.MQ_CLIENT_CONFIG.get('parameters'), max_queue_size=10):

        self._connection = None
        self._channel = None
        self._message_config = message_config
        self._message_mq = {}

        self._client_config = client_config
        self. _parameters = pika.connection.ConnectionParameters(host=client_config.get('host', 'localhost'), \
                                                                port=client_config.get('port', 5672), \
                                                                virtual_host=client_config.get('virtual_host', '/'))
        self._queue = multiprocessing.Queue(max_queue_size)
        self._process_handler = process_handler
        self._stop_event = multiprocessing.Event()
        self._exchenge = []
        self._mqqueue = []
        self._bind = {}

        self._unfinished_message = None

    def _get_one_message(self):
        '''
           get one message from the queue, it will be blocked if there is no message
           in the queue
        '''
        message = self._queue.get(True)
        logging.info('get a message from queue' + str(message))
        return message

    def _publish_message(self, exchange, routing_key, message, properties):
        '''
           publish a message to rabbitmq
        '''
        logging.info('publish message:' + routing_key + ':' + message)
        self._channel.basic_publish(exchange, routing_key, message, properties)

    def _declare_exchange(self, message_key):
        exchange = 'exchange_' + message_key

        if exchange not in self._exchenge:
            exchange_type = self._message_config.get(message_key, self._message_config['__default_message_config']).get('exchange_type', 'direct')
            durable = self._message_config.get(message_key, self._message_config['__default_message_config']).get('durable', False)

            self._channel.exchange_declare(callback=None, exchange=exchange, type=exchange_type, durable=durable)
            logging.info('declare exchange:' + exchange)

            self._exchenge.append(exchange)
            self._bind[message_key] = []

        return exchange


    def _generate_name(self, message_key, message_body, pre_name):
        priority = self._message_config.get(message_key, self._message_config['__default_message_config']).get('priority_level', 3) - 1
        if message_body.get('__priority', 0) <= priority:
            priority = message_body.get('__priority', 0)

        name = pre_name + message_key + ".P" + str(priority)

        if self._message_config.get(message_key, self._message_config['__default_message_config']).get('group_mode', False):
            name += ".G" + str(self._message_config.get(message_key, self._message_config['__default_message_config']).get('group_counts'), 0)

        return name

    def _declare_queue(self, message_key, message_body):

        queue_name = self._generate_name(message_key, message_body, 'queue_')

        if queue_name not in self._mqqueue:

            durable = self._message_config.get(message_key, self._message_config['__default_message_config']).get('durable', False)
            auto_delete = self._message_config.get(message_key, self._message_config['__default_message_config']).get('auto_delete', False)
            exclusive = self._message_config.get(message_key, self._message_config['__default_message_config']).get('exclusive', False)
            x_message_ttl = self._message_config.get(message_key, self._message_config['__default_message_config']).get('x_message_ttl', None)
            arguments = {}
            if x_message_ttl is not None:
                arguments["x-message-ttl"] = x_message_ttl

            self._channel.queue_declare(callback=None,\
                                        queue=queue_name, \
                                        durable=durable,  \
                                        auto_delete=auto_delete, \
                                        exclusive=exclusive, \
                                        arguments=arguments)
            logging.info('declare exchange:' + queue_name)

            self._mqqueue.append(queue_name)

        return queue_name
        
    def _bind_exchange(self, message_key, message_body):

        routing_key = self._generate_name(message_key, message_body, 'binding_') 

        if routing_key not in self._bind[message_key]:
            exchange = self._declare_exchange(message_key)
            queue_name = self._declare_queue(message_key, message_body)

            self._channel.queue_bind(callback=None, queue=queue_name, exchange=exchange,
                       routing_key=routing_key)
            logging.info('declare exchange:' + queue_name)

            self._bind[message_key].append(routing_key)
        return routing_key

    def _on_channel_open(self, channel):
        '''
           the main work is done here
        '''
        logging.info('begin publish the message ')
        while not self._stop_event.is_set():
            if self._unfinished_message == None:
                message = self._get_one_message() #get a message from the queue
                self._unfinished_message = message
            else:
                message = self._unfinished_message
            # prision break the block queue
            if message != None:
                message_key = message.get('message_key', None)
                message_body = message.get('message_body', None)
                if message_key == None:
                    logging.error('empty message_key')
                    continue
                if message_body == None:
                    logging.warn('empty message_body')
                    message_body = ''

                # make the exchange queue routing_key as the message_config
                exchange = self._declare_exchange(message_key)
                queue = self._declare_queue(message_key, message_body)
                routing_key = self._bind_exchange(message_key, message_body)

                # make the message parameters
                message_parameters = self._message_config.get(message_key, self._message_config['__default_message_config'])                
                properties = pika.BasicProperties()
                if message_parameters.get('content_type', 'text/json') == 'text/json':
                    properties.content_type = 'text/json'
                    message = dumps_jsonx(message_body)
                if message_parameters.get('persistent', True):
                    properties.delivery_mode = 2
                if message_parameters.get('with_timestamp', False):
                    properties.timestamp = datetime2timestamp(datetime.datetime.utcnow())

                # publish the message use select_connecter
                self._publish_message(exchange, routing_key, message, properties)
                # call handler when publish the message
                if self._process_handler != None:
                    self._process_handler(message_key, message_body)

                # clear the unfinished message
                self._unfinished_message = None
            else:
                break


    def _on_connect_open(self, connection):
        '''
           open the channel when conneciton was made
        '''
        logging.info('start open channel')
        self._channel = self._connection.channel(self._on_channel_open)
        logging.info('open channel successed')

    def connect(self):
        '''
           make a connection in select mode
        '''
        logging.info('start connection to rabbitmq')
        self._connection = pika.SelectConnection(parameters=self._parameters,
                                                on_open_callback=self._on_connect_open)
        logging.info('connection successed')

    def start(self):
        '''
            start the publish the messages in queue
        '''
        reconnection_times = 0
        while not self._stop_event.is_set():
            try:
                self.connect()
                reconnection_times = 0
                logging.info('begin the ioloop')
                self._connection.ioloop.start()
            except (pika.exceptions.AMQPConnectionError, pika.exceptions.AMQPChannelError, \
                    pika.exceptions.AMQPError, pika.exceptions.ConnectionClosed, \
                    pika.exceptions.ChannelError, pika.exceptions.ChannelClosed), e: ##redesign the exception!!!!!!
                print e
                time.sleep(5)
                reconnection_times += 1
                self._exchenge = []
                self._mqqueue = []
                self._bind = {}
                logging.info('reconnection to rabbitmq for ' + str(reconnection_times) + ' times')
            except Exception, e:
                logging.info('unhandled exceptions')
                sys.exit()

    def stop(self):
        '''
           stop the work
        ''' 
        time.sleep(1)
        self._stop_event.set()
        self._queue.put(None, True)
        self._connection.close()
        self._connection.ioloop.start()
        logging.info('close connection')
        while not self._queue.empty(): 
            logging.info('leave  message:' + self._get_one_message()) 

    def publish(self, message):
        '''
           publish a message
        '''

        self._queue.put(message, True)
        logging.info('put message into the queue:' + str(message))
