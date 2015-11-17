'''
@author: mingliu
'''
import copy
import inspect
from logging.config import dictConfig
import multiprocessing
import signal
import sys
import threading
import traceback
import logging as original_logging

import DefaultConfig
from log import logging, QueueHandler
from DefaultConfig import load_global_mq_client
from mqclient.messagequeue.exceptions import MQError

class HandlerBase(object):
    global_stop_event = multiprocessing.Event()

    @classmethod
    def stop(cls):
        HandlerBase.global_stop_event.set()
        print "all handlers are terminating gracefully"
        logging.debug("all handlers are terminating gracefully")

    def __init__(self):
        self._handler_key = self.__class__.__name__
        self._stop_event = None
        self.initialize()

    def initialize(self):
        pass

    def _stop_condition(self):
        return self._stop_event is not None and self._stop_event.is_set()

    def _before_stop(self):
        pass

    def start(self, log_config, max_threads=1):
        '''
        new start method to have a useless stop event
        '''
        dictConfig(log_config)
        for _ in range(max_threads):
            t = threading.Thread(target=self._worker)
            t.start()

    def mp_start(self, log_config, process_count=1):
        if process_count == 1:
            self.start(log_config)
        else:
            signal.signal(signal.SIGTERM, HandlerBase.stop)
            signal.signal(signal.SIGINT, HandlerBase.stop)  # for ctrl-c

            # start listener process to handle log request comes from worker
            # processes
            queue = multiprocessing.Queue(-1)
            listener = multiprocessing.Process(target=self._log_listener, \
                                               args=(HandlerBase.global_stop_event, \
                                                     queue, \
                                                     log_config,))
            listener.start()

            processes = []
            for _ in range(process_count):
                p = multiprocessing.Process(target=self.run_loop, args=(HandlerBase.global_stop_event, queue,))
                p.daemon(True)
                processes.append(p)

            for p in processes:
                p.start()

    def _worker(self):
        self.run_loop(multiprocessing.Event())

    def _log_listener(self, stop_event, queue, log_config):
        self._stop_event = stop_event
        # apply real log configurations
        dictConfig(log_config)
        while not self._stop_condition():
            try:
                record = queue.get()
                if record is None:
                    # send None record to quit listener
                    break
                logger = original_logging.getLogger(record.name)
                logger.handle(record)
            except:
                traceback.print_exc(file=sys.stderr)
        queue.close()

    def run_loop(self, stop_event, queue=None):
        '''
        run handler in endless loop in one dedicate process
        '''
        # need to config QueueHandler in worker process
        if queue is not None:
            h = QueueHandler(queue)
            root = original_logging.getLogger()
            root.addHandler(h)
            # set level of queue handler to DEBUG to accept all logs
            root.setLevel(original_logging.DEBUG)
            # after this, all log will be put into the queue use QueueHandler
        logging.info("subprocess for handler started", self._handler_key)
        self._stop_event = stop_event
        self._connection.set_stop_condition(self._stop_condition)

        self._main()

        logging.info("loop stopped for handler", self._handler_key)
        if queue is not None:
            # close queue
            queue.close()
        self._before_stop()
        sys.exit(0)

    def _main(self):
        while not self._stop_condition():
            self._main_process()

    def _main_process(self):
        pass

    def _log_formatter(self, message, *args, **kwargs):
        return logging.format_msg("%s,%s" % (self._handler_key, message), *args, **kwargs)


class MessageHandler(HandlerBase):
    '''
    handler._process can be used in two scenarios:
    1) a separate process to run an endless loop that consumes message from message queue and processes.
    2) ondemand approach to let client side to call the method directly.

    HandlerRepository.process can be used in two modes:
    1) viaqueue mode: will publish message to queue directly;
    2) inproc mode:   will call handler._process;
    '''

    def __init__(self, async_mode=False):
        super(MessageHandler, self).__init__()
        self.message_key_dict = {}
        self._async_mode = async_mode
        self._connection = load_global_mq_client(True)
        self._message_auth = ''
        self._message_key = ''

    def set_inputmessage(self, message_key):
        self._message_key = message_key

    def init_Message(self, message_auth):
        self._message_auth = '_' + str(message_auth)

    def process(self, message):
        if self._async_mode:
            raise MQError("process() just support sync_mode operation")
        message = copy.deepcopy(message)
        self._process(message)
        return True

    def _process(self, message):
        pass

    def _build_message_from_args(self, frame):  # not used now
        message = {}

        args, _, _, values = inspect.getargvalues(frame)
        for arg in args:
            if arg != "self":
                message[arg] = values[arg]

        return message

    def _main_process(self):
        message = self._connection.get(self._message_key + self._message_auth, wait_secs=-1)
        if message is not None:
            delivery_tag = message["__delivery_tag"]
            logging.debug(self._log_formatter("start processing message", message.get("url", "")))
            success = self.process(message)
            if success:
                self._connection.ack(self._message_key + self._message_auth, delivery_tag)
            logging.debug(self._log_formatter("ended processing message", message.get("url", "")))
        else:
            logging.debug(self._log_formatter("message queue is empty or handler is terminating", self._message_key))

    def reply(self, message, response):
        self._connection.reply(self._message_key + self._message_auth, message, response)

    def _main(self):
        if self._async_mode:
            raise MQError("process() just support sync_mode operation")
        else:
            while not self._stop_condition():
                self._main_process()
