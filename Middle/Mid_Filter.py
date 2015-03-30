#!/usr/bin/env python
import pika
import sys
import ast
import json
from libs.Configuration import Configuration
from SysLog import SysLogger
from Conf_Parser import Conf_Paser
from Worker import *

CFG = Conf_Paser().cfg
logger = SysLogger().logger
module = __import__('Worker')

class Filter(object):

    MQ_Host = '127.0.0.1'
    email_queue = None
    net = None
    filters_name = CFG.getSection('Filters')

    def __init__(self,host):
        self.MQ_Host = host
        self.get_filters()

    def filt(self,data):
        self.net.filt(data)
        #self.email_queue.filt(data)

    def get_filters(self):
        try:
            filters = self.filters_name['filters']
            if 'email'in filters:
                pass
                #self.email_queue = Email(self.MQ_Host)
            if 'ha' in filters:
                # used to life migration
                pass
            if 'net' in filters:
                net = eval('NET.Net') 
        except:
            raise Exception("get filters failed")

