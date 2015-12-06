#encoding: utf-8
'''
Created on 2015年11月18日

@author: lml
'''

from logging import config
from config.CommonConfig import LOG_PATH
import logging

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
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_PATH + '/extractor.log',
            'when': 'D',
            'backupCount' : 30
        },
        'perf':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'formatter': 'message_only',
            'filename': LOG_PATH + '/extractor_perf.log',
            'maxBytes': 30 * 1024 * 1024,  # 30MB
            'backupCount' : 30
        },
        'err':{
            'level':'ERROR',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_PATH + '/extractor.err',
            'when': 'D',
            'backupCount' : 30
        },
                 
        'file_crawler':{
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_PATH + '/crawler.log',
            'when': 'D',
            'backupCount' : 30
        },
        'perf_crawler':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'formatter': 'message_only',
            'filename': LOG_PATH + '/crawler_perf.log',
            'maxBytes': 30 * 1024 * 1024,  # 30MB
            'backupCount' : 30
        },
        'err_crawler':{
            'level':'ERROR',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_PATH + '/crawler.err',
            'when': 'D',
            'backupCount' : 30
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'extractor': {
            'handlers': ['file', 'err' ,"console"],
            'level': 'DEBUG',
        },
        'crawler': {
            'handlers': ['file_crawler', 'err_crawler' ,"console"],
            'level': 'DEBUG',
        },
        'extractor_perf': {
            'handlers': ['perf'],
            'level': 'DEBUG',
        },
        'default' : {
            'handlers': ['file', 'err' ],
            'level': 'DEBUG',
        },
    }
}

config.dictConfig(LOGGING)
LOGGER_EXTRACTOR = logging.getLogger("extractor")
LOGGER_CRAWLER = logging.getLogger("crawler")
