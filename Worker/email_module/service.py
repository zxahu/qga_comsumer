#!/usr/bin/env python
#coding=utf-8

import SimpleXMLRPCServer
from string import Template
import smtplib, json, os, SocketServer
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class MailSendingRPC:

    SMTPServer = None

    def __init__(self, config):
        self.SMTPHost = config.host
        self.SMTPPort = int(config.port)
        self.TemplatePath = config.path

    def set(self, jsonData):
        data = json.loads(jsonData)
        mail = Mail(data, self.TemplatePath)

        self.SMTPServer = SMTPFactory()
        self.SMTPServer.setConfiguration(self.SMTPHost, self.SMTPPort)

        try:
            self.SMTPServer.sendmail(mail)
            self.SMTPServer.close()
            return jsonData
        except:
            return "false"

class Mail:
    subject = None
    template = None
    sender = None
    receiver = None
    #image = None
    attachment = []
    body = ""

    def __init__(self, json=None, path="./"):
        self.path = path
        if json is not None:
            self.setByJson(json)

    def _getAbsFileName(self, filename):
        return self.path + filename

    def setByJson(self, jsonData):
        self.subject = jsonData["Subject"]
        self.sender = "{sender}@{hostname}".format(sender=jsonData["sender"], hostname=os.popen("hostname").read().rstrip())
        self.receiver = jsonData["reciever"]
        #self.image = jsonData["image"]
        self.addAttachemnt(jsonData["image"])

        if ("template" in jsonData.keys()):
            template = self._getAbsFileName(jsonData["template"])
            self.setBodyByTemplate(template, jsonData["Data"])
        else :
            self.body = jsonData["Data"]

    def setBodyByTemplate(self, template, values):
        tpl = MailBodyGenerator(template)
        self.body = tpl.assign(values)

    def addAttachemnt(self, file):
        self.attachment.append(file)

    def render(self):
        mail = MIMEText(self.body, _subtype='html', _charset='utf-8')
        content = MIMEMultipart('related')
        content['Subject'] = self.subject
        content['From'] = self.sender
        content['To'] = self.receiver

        content.attach(mail)
        for file in self.attachment:
            filename = self._getAbsFileName(file)
            fp = open(filename, 'rb')
            msgImage = MIMEImage(fp.read())
            msgImage.add_header('Content-ID', "<%s>" % file)
            fp.close()

            content.attach(msgImage)
        return content.as_string()

class SMTPFactory(smtplib.SMTP):

    def setConfiguration(self, host, port):
        self.host = host
        self.port = port


    def sendmail(self, mail):
        from_addr = mail.sender
        to_addrs = mail.receiver
        smtplib.SMTP.connect(self, self.host, self.port)
        return smtplib.SMTP.sendmail(self, from_addr, to_addrs, mail.render(), [], [])

class MailBodyGenerator:
    template = None
    templatePath = "./"

    def __init__(self, templateFile):
        self.template = open(templateFile).read()

    def assign(self, values, safe=True):
        tpl = Template(self.template)
        if safe: return  tpl.safe_substitute(values)
        return tpl.substitute(values)

class RPCThreading(SocketServer.ThreadingMixIn, SimpleXMLRPCServer.SimpleXMLRPCServer):
    pass

def main(config):

    worker = MailSendingRPC(config)

    #server = SimpleXMLRPCServer.SimpleXMLRPCServer(("0.0.0.0", int(config.listen)))
    server = RPCThreading(("0.0.0.0", int(config.listen)))
    server.register_instance(worker)
    print "Listening on port %s" % config.listen
    server.serve_forever()
 
if __name__ == '__main__':
    from optparse import OptionParser

    options = OptionParser()
    options.add_option("-l", "--listen", dest="listen", default="80", help="RPC service port")
    options.add_option("-H", "--host", dest="host", default="localhost", help="Mail server hostname or IP address")
    options.add_option("-p", "--port", dest="port", default="25", help="Smtp port, default: 25")
    options.add_option("-f", "--template-path", dest="path", default="./template/", help="Path which contained template files")
    (option, args) = options.parse_args()

    main(option)
    # if os.fork() == 0: main(option)
    # else: exit()
