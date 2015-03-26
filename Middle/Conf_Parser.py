__author__ = 'zhang11'

from libs.Configuration import Configuration
from optparse import OptionParser

class Conf_Paser(object):

    __instance = None
    cfg = None

    def __new__(cls, *args, **kwargs):
        if (cls.__instance is None):
            cls.__instance = super(Conf_Paser, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        parser = OptionParser()
        parser.add_option("-f", "--conf",
                          dest="conf", default="etc/qga_consumer.conf",
                          help="Configuration file")

        (options, args) = parser.parse_args()

        self.cfg = Configuration(options.conf)

