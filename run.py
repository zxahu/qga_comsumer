__author__ = 'zhang11'

import os
from Middle.Middle import Middle
from Middle.Mid_Filter import Filter
from Middle.Mongo_Proc import Mongo_Proc
from Middle.SysLog import SysLogger
from Middle.Conf_Parser import Conf_Paser


def create_instance():
    middle = Middle(CFG.getSection('Middle'))

CFG = Conf_Paser().cfg
logger = SysLogger().logger

if __name__ == '__main__':
    Middle(CFG.getSection('Middle'))

