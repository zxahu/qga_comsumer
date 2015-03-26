#!/usr/bin/env python
import sys
import pika
import json
import datetime
import os
from Mongo_Proc import Mongo_Proc
from Mid_Filter import Filter
from SysLog import SysLogger
from Conf_Parser import Conf_Paser

CFG = Conf_Paser().cfg
logger = SysLogger().logger

class Middle(object):

    db = None
    strainer = None

    MQ_HOST = '127.0.0.1'
    QUEUE_NAME = 'database'

    connection = None

    def __init__(self,cfg):
        keys = cfg.keys()
        if 'mq_host' in keys:
            self.MQ_HOST = cfg['mq_host']
        if 'queue_name' in keys:
            self.QUEUE_NAME = cfg['queue_name']
        self.db = Mongo_Proc(CFG.getSection('Mongo_Proc'))
        self.strainer =Filter(self.MQ_HOST)
        self.receive_init()

    def __del__(self): 
        if self.connection is not None:
            self.connection.close()

    def callback(self,ch, method, properties, body):
        message = body
        self.db.save(message)
        self.strainer.filt(body)

    def receive_init(self):
        try :
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.MQ_HOST))
        except :
            raise Exception("connect to rabbitmq failed")
        try :
            channel = self.connection.channel()
            channel.queue_declare(queue=self.QUEUE_NAME, durable=True)
            print ' [*] Waiting for messages. To exit press CTRL+C'
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(self.callback,queue=self.QUEUE_NAME,no_ack=True)
            channel.start_consuming()
        except :
            raise Exception("init comsuming failed")

if __name__ == '__main__':
    
    mid = Middle() 
  
