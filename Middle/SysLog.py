__author__ = 'zhang11'

import logging.handlers

class SysLogger(object):

    logger = None

    log_level = logging.DEBUG
    log_file = "/etc/QGA/consumer.log"
    format = "%(asctime)s - %(filename)s:%(lineno)s  - %(levelname)s - %(message)s"

    @staticmethod
    def getLogger(self):
        if SysLogger.logger is  None:
            return SysLogger.logger

        SysLogger.logger = logging.getLogger()
        log_handler = logging.handlers.BaseRotatingHandler(filename= SysLogger.log_file)
        log_fmt = logging.Formatter(SysLogger.format)
        log_handler.setFormatter(log_fmt)
        SysLogger.logger.addHandler(log_handler)
        SysLogger.logger.setLevel(SysLogger.log_level)
        return SysLogger






