#!/usr/bin/env python
#coding=utf-8

import xmlrpclib, json, sys

def main(filename):
    server = xmlrpclib.ServerProxy("http://10.239.21.164")
    x = json.load(open(filename))
    print server.set(json.dumps(x))

if __name__ == '__main__':
    filename = sys.argv[1]
    main(filename)

