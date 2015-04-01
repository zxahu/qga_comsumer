#!/usr/bin/env python

import xmlrpclib
import json

class RPC_Mail(object):

    server = None

    def __init__(self,server):
        self.server = xmlrpclib.ServerProxy("http://10.239.21.164")

    def send_mail(self,data):
        message = json.dumps(data)
        self.server.set(message)

data = {'sender': 'VM_Monitor', 'image': 'iLab.png', 'template': 'iLab_Default.html', 'reciever': 'xin1.x.zhang@intel.com', 'Data': {'host': u'SHCNNODE02', 'time': 1427855499.163463, 'Data': [0.0, 0.01, 0.05], 'title': u'OpenStack LoadAvgProblem'}, 'Subject': u'OpenStack LoadAvgProblem'}

r = RPC_Mail("abc")
r.send_mail(data)
