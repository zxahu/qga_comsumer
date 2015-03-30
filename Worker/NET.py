__author__ = 'zhang11'

from Handler import Handler
from Middle.Conf_Parser import Conf_Paser
from Middle.SysLog import SysLogger
import re

logger = SysLogger().logger
CFG = Conf_Paser().cfg

class Net(Handler):

    trigger = 3
    broken = None

    def __init__(self):
        self.QUEUE_NAME = "Net_Recovery"
        self.connect(self.QUEUE_NAME)


    def analysis(self,message):
        name = message['host']
        if name in message.keys:
            self.broken[name] = self.broken[name]+1
        else:
            self.broken[name] =1
            self.hosts[name]='ERROR'
        if self.broken[name] > self.trigger :
            self.solve(message)
            self.broken[name] = 0
            self.hosts[name] = 'OK'

    def solve(self,message):
        logger.error(message)
        content ={
            "host" : message['host'],
            "type" : "Net",
            "message":message['message'],
            "vm":name
        }
        logger.info(content)
        self.requeue(self.QUEUE_NAME,content)

    def filt(self,message):
        if message['Priority'] == 20:
            self.analysis(message)




