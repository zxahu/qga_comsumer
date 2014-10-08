#!/usr/bin/env python
import pymongo
import json
from pymongo import MongoClient

class Mongo_Proc(object):

    DB_HOST = 'localhost'
    DB_PORT = 27017
    DB_NAME = 'local'
    COLLECTION_NAME = 'q_g_a_data'
    data_list = []
    message_list = []

    def __init__(self,cfg):
        keys = cfg.keys()
        if 'db_host' in keys:
            self.DB_HOST = cfg['db_host']
        if 'db_port' in keys:
            self.DB_PORT = int(cfg['db_port'])
        if 'db_name' in keys:
            self.DB_NAME = cfg['db_name']
        if 'collection_name' in keys:
            self.COLLECTION_NAME = cfg['collection_name']    
        self.mongo_init()

    def mongo_init(self):
        try:
            self.client = MongoClient(self.DB_HOST,self.DB_PORT)
            self.db = self.client[self.DB_NAME]
            self.collection = self.db[self.COLLECTION_NAME]
        except :
            raise Exception("connect to mongodb failed")

    """this function help save data to mongodb,a tuple save data and save to mongo when length>2"""
    def save(self,data):
        self.data_list.append(data)
        if len(self.data_list) > 32:
            try:
                for data in self.data_list:
                    message = json.loads(data)
                    self.message_list.append(message)
                self.collection.insert(self.message_list)
                self.data_list = []
                self.message_list = []
            except :
                raise Exception("insert data to mongodb failed")
