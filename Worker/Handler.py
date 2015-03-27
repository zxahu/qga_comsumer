__author__ = 'zhang11'

from Middle.Conf_Parser import Conf_Paser
from Middle.SysLog import SysLogger
import pika

logger = SysLogger().logger
CFG = Conf_Paser().cfg

class Handler(object):

    MQ_Host = '127.0.0.1'
    QUEUE_NAME = None
    connection = None
    channel = None

    def __init__(self):
        config=CFG.getSection('Middle')
        self.MQ_Host = config['MQ_HOST']

    def __del__(self):
        pass

    def analysis(self,message):
        pass

    def solve(self):
        pass

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.MQ_Host))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.QUEUE_NAME,durable=True)
        except:
            logger.error("connect to rabbitmq failed")
            raise Exception("connect to rabbitmq failed")

    def requeue(self,queue_name,message):
        try:
            self.channel.basic_publish(exchange='', routing_key=queue_name,body=message, properties=pika.BasicProperties(delivery_mode=2,))
        except:
            logger.error("send message to rabbitmq failed")
            raise Exception("send message to rabbitmq failed")