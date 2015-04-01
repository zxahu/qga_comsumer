#!/usr/bin/env python
import pika
import sys
import re
from Middle.SysLog import SysLogger
from Middle.Conf_Parser import Conf_Paser
from email_module.rpcclient import RPC_Mail

logger = SysLogger().logger
CFG = Conf_Paser().cfg

class Email(object):

    contact_info = None
    mail = None

    def __init__(self):
        self.contact_info = CFG.getSection("Email")
        if 'email_receiver' in self.contact_info.keys():
            self.receiver  = self.contact_info['email_receiver']
        else:
            self.receiver = "EC OpenStack"

        if 'email_server' in self.contact_info.keys():
            email_server = "http://"+self.contact_info['email_server']
        else:
            email_server = "http://10.239.21.164"

        self.sender = "VM_Monitor"
        self.mail = RPC_Mail(email_server)

    def __del__(self): 
        pass

    def filt(self,data):
        if data['priority'] != 10:
            self.send_mail(data)

    def build_json(self,message):
        content = {}
        mail_content ={}
        if 'host' in message:
            host = message['host']
        else:
            host = 'unknown'

        if 'timestamp' in message:
            time = message['timestamp']
        else:
            time = 'unknown'

        if 'message' in message:
            try:
                problem_type = message['message']['action']
                Data = message['message']['content']
            except:
                problem_type = 'unknown'
        else:
            problem_type = 'unknown'
            Data = 'unknown'

        subject = "OpenStack "+problem_type+"Problem"

        content['host'] = host
        content['title'] = subject
        content['time'] =time
        content['Data'] =Data

        mail_content['sender']  = self.sender
        mail_content['reciever'] = self.receiver
        mail_content['template'] ="iLab_Default.html"
        mail_content['image'] ="iLab.png"

        mail_content['Subject'] = subject
        mail_content['Data'] = content

        return mail_content

    def send_mail(self,data):
        mail_content = self.build_json(data)
        self.mail.send_mail(mail_content)


