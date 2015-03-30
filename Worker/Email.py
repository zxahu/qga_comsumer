#!/usr/bin/env python
import pika
import sys
import re
from Middle.SysLog import SysLogger

logger = SysLogger().logger

class Email(object):

    MQ_Host = '127.0.0.1'
    connection = None
    channel = None

    QUEUE_NAME = 'email'

    def __init__(self,host):
        self.MQ_Host = host
        self.connect(self.QUEUE_NAME)

    def __del__(self): 
        if self.connection is not None:
            self.connection.close()

    def filt(self,data):
        logger.info("email data:"+data)
 #       level = data['priority']
        try :
            if level == '20':
                self.requeue(self.QUEUE_NAME,data)
        except :
            raise Exception("filt message failed")

    def connect(self,queue_name):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                        host=self.MQ_Host))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.QUEUE_NAME,durable=True)
        except:
            logger.error("filter connect to rabbitmq failed")
            raise Exception("filter connect to rabbitmq failed")

    def requeue(self,queue_name,message):
        try:
            self.channel.basic_publish(exchange='', routing_key=queue_name,body=message, properties=pika.BasicProperties(delivery_mode=2,))
        except:
            logger.error("after filt,send message to rabbitmq failed")
            raise Exception("after filt,send message to rabbitmq failed")
