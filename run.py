import os
from Middle.Middle import Middle
from Middle.Mid_Filter import Filter
from Middle.Mongo_Proc import Mongo_Proc
from libs.Configuration import Configuration
from optparse import OptionParser
from multiprocessing import Process


def create_instance():
    middle = Middle(CFG.getSection('Middle'))

parser = OptionParser()
parser.add_option("-f", "--conf",
                  dest="conf", default="etc/qga_consumer.conf",
                  help="Configuration file")

(options, args) = parser.parse_args()

CFG = Configuration(options.conf)

if __name__ == '__main__':
   # for i in range(10):
    proc = Process(target=create_instance)
    proc.start()
