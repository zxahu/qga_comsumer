#!/usr/bin/env python
import pika
import sys

class Email(object):

    MQ_Host = '10.239.21.48'
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
        try :
            #if data[0] =='4':
            self.requeue(self.QUEUE_NAME,data[1:])
        except :
            raise Exception("filt message failed")

    def connect(self,queue_name):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                        host=self.MQ_Host))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.QUEUE_NAME,durable=True)
        except:
            raise Exception("filter connect to rabbitmq failed")

    def requeue(self,queue_name,message):
        try:
            self.channel.basic_publish(exchange='', routing_key=queue_name,body=message, properties=pika.BasicProperties(delivery_mode=2,))
        except:
            raise Exception("after filt,send message to rabbitmq failed")
