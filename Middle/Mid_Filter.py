#!/usr/bin/env python
import pika
import sys
import ast
import json
from libs.Configuration import Configuration
from Worker.Email import Email
from SysLog import SysLogger
from Conf_Parser import Conf_Paser

CFG = Conf_Paser().cfg
logger = SysLogger().logger

class Filter(object):

    MQ_Host = '127.0.0.1'
    email_queue = None
    filters_name = CFG.getSection('Filters')

    def __init__(self,host):
        self.MQ_Host = host
        self.get_filters()

    def filt(self,data):
        self.email_queue.filt(data)

    def get_filters(self):

        filters = self.filters_name['filters']
        if 'email'in filters:
            pass
            self.email_queue = Email(self.MQ_Host)
        if 'ha' in filters:
            # used to life migration
            pass
        if 'net' in filters:
            self.buildWorker('NET.Net')

    def buildWorker(self,name):
        obj = eval(name)
        return obj

     
