__author__ = 'zhang11'

from Handler import Handler
from Middle.Conf_Parser import Conf_Paser
from Middle.SysLog import SysLogger
import re

logger = SysLogger().logger

class Net(Handler):

    trigger = 3
    broken = None
    p_id = re.compile(r'instance-\d{7}')

    def __init__(self):
        self.QUEUE_NAME = "Net_Recovery"
        self.connect(self.QUEUE_NAME)

    def analysis(self,message):
        vm_name = self.p_id.findall(message['guest'])
        name = message['host']+'.'+vm_name
        if name in message.keys:
            self.broken[name] = self.broken[name]+1
        else:
            self.broken[name] =1
        if self.broken[name] > self.trigger :
            self.broken[name] = 0
            self.solve(message,vm_name)

    def solve(self,message,name):
        content ={
            "host" : message['host'],
            "type" : "Net",
            "message":message['message'],
            "vm":name
        }
        logger.info(content)
        self.requeue(self.QUEUE_NAME,content)





