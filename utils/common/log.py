#-*- coing=utf-8 -*-
import os
import logging
import logging.config
from config import logging_config
from logging.config import dictConfig

class Logger(object):
    def __init__(self,logname=__name__):
        self.logname=logname
        logging_config.LOGGING['handlers']['default']['filename']=os.path.join(logging_config.BASE_LOG_DIR,'WonderStithInfo.log')
        logging_config.LOGGING['handlers']['error']['filename'] = os.path.join(logging_config.BASE_LOG_DIR, 'WonderStitchErr.log')
        logging_config.LOGGING['handlers']['collect']['filename'] = os.path.join(logging_config.BASE_LOG_DIR,'WonderStitchCollect.log')
        #print(logging_config.LOGGING['handlers'])
    def get_logger(self):
        dictConfig(logging_config.LOGGING)  # 导入上面定义的logging配置
        self.logger = logging.getLogger(self.logname)  # 生成一个log实例
        return self.logger




