#!/usr/bin/env python
'''
@author: mingliu

provide a global configuration
'''

import rabbitmq_blocking_client
import settings

MQ_CLIENT_CONFIG = {
"parameters": {"host": settings.RABBITMQSERVER_IP,
                "port": settings.RABBITMQSERVER_PORT,
                "virtual_host": "/",
                "lazy_load": True},
# do not use aux store
"aux_store": {"enabled": False,
               "host": "localhost",
               "port": 27017,
               "name": "mq_aux_store"},
}

# the configuration for message
MESSAGE_CONFIGS = {
 "__default_message_config": {
"priority_level": 3,
"group_mode": False,
"group_counts": None,
"exchange_type": "topic",
"timestamp_expires": False,
"message_ids": None,
"content_type": "text/json",
"persistent": True,
"auto_ack": False,
"with_timestamp": False,
"x_message_ttl": 1000 * 60 * 60 * 24 * 1,
"delete_first": False,
"durable": False,
"exclusive": False,
"auto_delete": False,
"timeout": None,
"rpc_queue_expires": 1000 * 60 * 60 * 12,
"max_rpc_queue_count": 1000,
"rpc_reply_content_type": "text/json",
'message_fields': {}
},
}


def load_global_mq_client(force=False):
    '''
    create a blockingclieng to rabbitmq
    '''
    if force:
        return rabbitmq_blocking_client.RabbitMQBlockingClient(MQ_CLIENT_CONFIG)
