#!/usr/bin/env python
import pika
import sys
import ast
from libs.Configuration import Configuration
from Worker.Email import Email

class Filter(object):

    MQ_Host = '10.239.21.48'
    Filters = ['email',]
    email_queue = None

    def __init__(self,host):
        self.MQ_Host = host
        self.email_queue = Email(self.MQ_Host)

    def filt(self,data):
        self.email_queue.filt(data)



     
