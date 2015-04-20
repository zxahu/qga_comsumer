__author__ = 'zhang11'

from Handler import Handler
from Middle.Conf_Parser import Conf_Paser
from Middle.SysLog import SysLogger
import Check_remote
import re
import json

logger = SysLogger().logger
CFG = Conf_Paser().cfg

broken = {}
class Net():

    trigger = 3

    def __init__(self):
        config=CFG.getSection('Middle')
        self.MQ_Host = config['MQ_HOST']
        self.check = Check_remote(self.MQ_Host)


    def analysis(self,message):
        global broken
        name = message['host']
        if name in broken:
            broken[name] = broken[name]+1
        else:
            broken[name] =1
            self.hosts[name]='ERROR'
        if broken[name] > self.trigger :
            self.solve(name,message['message'])
            broken[name] = 0
            self.hosts[name] = 'OK'

    def solve(self,host,message):
        content ={
            "host" : host,
            "type" : "Net",
            "message":message,
        }
        str_content = json.dumps(content) 
        response = self.check.call(host,str_content)
        ####mail(response)

    def filt(self,message):
        if message['priority'] != 10:
            self.analysis(message)



