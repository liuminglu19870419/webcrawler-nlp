'''
Created on Dec 14, 2012

@author: fli
'''
import os
from logging.config import dictConfig
from ConfigParser import SafeConfigParser

LOGGING = {
    'version': 1,
    'disable_existing_loggers':False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'detail': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
        },
        'message_only': {
            'format': '%(asctime)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'file':{
            'level':'INFO',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'simple',
            'filename':'/tmp/crawler.log',
            'when': 'D',
            'backupCount' : 3
        },
        'perf':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'formatter': 'message_only',
            'filename':'/tmp/crawler.log',
            'maxBytes': 30 * 1024 * 1024, # 30MB
            'backupCount' : 30
        },
        'err':{
            'level':'ERROR',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'detail',
            'filename':'/tmp/diapatcher.err',
            'when': 'D',
            'backupCount' : 3
        },
    },
    'loggers': {
        'mqclient': {
            'handlers': ['file', 'err' ],
            'level': 'INFO',
        },
        'mqclient.perf': {
            'handlers': ['perf'],
            'level': 'DEBUG',
        },
        'default' : {
            'handlers': ['file', 'err' ],
            'level': 'INFO',
        },
    }
}

RABBITMQSERVER_IP = "192.168.1.101"
RABBITMQSERVER_PORT = 5672
SECTION = 'mqclient'
def _load_config():
    global RABBITMQSERVER_IP, RABBITMQSERVER_PORT
#     cp = SafeConfigParser()
#     
#     cp.read(["/var/app/enabled/mqclient/mqclient.cfg"])
#     cp.read(["imagecrawler.cfg"])

#     RABBITMQSERVER_IP = cp.get(SECTION, 'rabbitmqserver_ip', '192.168.1.101')
#     RABBITMQSERVER_PORT= int(cp.get(SECTION, 'rabbitmqserver_port', '5672'))

#     logs_dir = cp.get(SECTION, 'logs_dir', 'logs')
    logs_dir = "./"
    LOGGING['handlers']['file']['filename'] = os.path.join(logs_dir, 'mqclient.log')
    LOGGING['handlers']['perf']['filename'] = os.path.join(logs_dir, 'mqclient_perf.log')
    LOGGING['handlers']['err']['filename'] = os.path.join(logs_dir, 'mqclient.err')
    log_level = "DEBUG"
#     log_level = cp.get(SECTION, 'log_level', 'INFO')
    # update log level
    for logger_name, logger_config in LOGGING['loggers'].items():
        if logger_name.find('perf') != -1:
            # do not change log level for performance log
            continue
        else:
            logger_config['level'] = log_level
    LOGGING['handlers']['file']['level'] = log_level
    dictConfig(LOGGING)

_load_config()

