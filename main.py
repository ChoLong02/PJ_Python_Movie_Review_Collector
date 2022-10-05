import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import json
import logging
import logging.config
from common.configuration import CommonConfig


if __name__ == "__main__":

    ##############################
    # 1.Load Config File #
    ##############################
    CommonConfig.config_generator()
    config = CommonConfig.config_read()
    
    
    ##############################
    # 2.Load Log Setting #
    ##############################
    with open('logging.json', 'r') as f:
        log_config = json.load(f)
    logging.config.dictConfig(log_config) 
    
    debug_logger = logging.getLogger('server-debug')
    debug_logger.debug('debug')
    debug_logger.info('info')
    debug_logger.error('error')
    debug_logger.error('critical')
    
    error_logger = logging.getLogger('server-error')
    error_logger.debug('debug')
    error_logger.info('info')
    error_logger.error('error')
    error_logger.error('critical')