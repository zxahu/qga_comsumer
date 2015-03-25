__author__ = 'zhang11'

import logging.handlers
import os

class SysLogger(object):

    __instance = None
    logger = None
    log_level = logging.DEBUG
    log_file = "/var/log/QGA/consumer.log"
    format = "%(asctime)s - %(filename)s:%(lineno)s  - %(levelname)s - %(message)s"

    def __new__(cls, *args, **kwargs):
        if (cls.__instance is None):
            cls.__instance = super(SysLogger, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.test_path()
        self.logger = logging.getLogger()
        log_handler = logging.handlers.RotatingFileHandler(self.log_file, maxBytes = 1024*1024, backupCount = 5)
        log_fmt = logging.Formatter(self.format)
        log_handler.setFormatter(log_fmt)
        self.logger.addHandler(log_handler)
        self.logger.setLevel(self.log_level)

    def test_path(self):
        if not os.path.exists("/var/log/QGA/"):
            os.makedirs("/var/log/QGA/")





