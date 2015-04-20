__author__ = 'zhang11'
from Middle.Conf_Parser import Conf_Paser
from Middle.SysLog import SysLogger
import pika
import uuid


logger = SysLogger().logger
CFG = Conf_Paser().cfg

class CheckRemote():
    def __init__(self,host):
        logger.info("test1")
#        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
#        logger.info("test2")
#        self.channel = self.connection.channel()
#        logger.info("test3")
#        result = self.channel.queue_declare(exclusive=True)
#        logger.info("test4")
#        self.callback_queue = result.method.queue
#        logger.info("test5")
#        self.channel.basic_consume(self.on_response,no_ack=True,queue=self.callback_queue)
#        logger.info("test6")

    def on_response(self,ch,method,props,body):
        if self.corr_id == props.correlation_id:
            self.response = body


    def call(self,queue,message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=queue,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=message)
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)

