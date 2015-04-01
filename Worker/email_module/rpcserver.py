#!/usr/bin/env python
#coding=utf-8
# 
#                                  _oo8oo_
#                                 o8888888o
#                                 88" . "88
#                                 (| -_- |)
#                                 0\  =  /0
#                               ___/'==='\___
#                             .' \\|     |// '.
#                            / \\|||  :  |||// \
#                           / _||||| -:- |||||_ \
#                          |   | \\\  -  /// |   |
#                          | \_|  ''\---/''  |_/ |
#                          \  .-\__  '-'  __/-.  /
#                        ___'. .'  /--.--\  '. .'___
#                     ."" '<  '.___\_<|>_/___.'  >' "".
#                    | | :  `- \`.:`\ _ /`:.`/ -`  : | |
#                    \  \ `-.   \_ __\ /__ _/   .-` /  /
#                =====`-.____`.___ \_____/ ___.`____.-`=====
#                                  `=---=`
# 
# 
#               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                          佛祖保佑         永不宕机/永无bug
#

'''
python rpcserver.py

mailservice

Created on Jan 30, 2015

@author: lina

'''


import SimpleXMLRPCServer
import SocketServer
import threading
import json
import jinja2
import os
import smtplib
from SocketServer import ThreadingMixIn
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class CRpcServer:#(SocketServer.ThreadingMixIn,SimpleXMLRPCServer.SimpleXMLRPCServer)
    def __init__(self):
        self.data = "empty"

    # def run_queqe(self):
    #   content = list()
    #   for x in xrange(1,10):
    #       content.append(self.data)
 
    def set(self, jsonData):
        self.Subject = jsonData["Subject"]
        self.template = jsonData["template"]
        self.sender = "{sender}@{hostname}".format(sender=jsonData["sender"], hostname=os.popen("hostname").read().rstrip())    
        self.receiver = jsonData["reciever"]
        self.image = jsonData["image"]
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        tm_loader = jinja2.FileSystemLoader([curr_dir])
        env = jinja2.Environment(loader=tm_loader)
        tpl = env.get_template(self.template)
        print tpl.render(jsonData["Data"])

        #send mail
        ilabcontent = open(self.template).read()
        print ilabcontent
        #self.send(ilabcontent)
        self.send(tpl.render(jsonData["Data"]))
        self.server.quit()
        return 0

    def send(self, mailcontent):
        self.server = smtplib.SMTP()
        self.server.connect("localhost")
        mail = MIMEText(mailcontent ,_subtype='html' ,_charset='utf-8')
        self.msRoot = MIMEMultipart('related')
        self.msRoot['Subject'] = self.Subject
        self.msRoot['From'] = self.sender
        self.msRoot['To'] = self.receiver
        self.msRoot.attach(mail)
        fp = open(self.image, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()

        msgImage.add_header('Content-ID', '<image1>')
        self.msRoot.attach(msgImage)
        #self.msRoot.attach(self.picture)
        self.server.sendmail(self.sender, self.receiver, self.msRoot.as_string())

    def get(self):
        return self.template

class RPCThreading(SocketServer.ThreadingMixIn, SimpleXMLRPCServer.SimpleXMLRPCServer):
    pass
        
def main():
    obj = CRpcServer()
    server = RPCThreading(("0.0.0.0", 10086))
    server.register_instance(obj)
    print "Listening on port 10086"
    server.serve_forever()
 
if __name__ == '__main__':
     main() 
