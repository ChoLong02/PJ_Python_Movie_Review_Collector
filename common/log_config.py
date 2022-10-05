import json
import logging
import logging.config


class LogConfig:

    def get_logger(self):
        with open('./common/logging.json', 'r') as f:
            log_config = json.load(f)
        logging.config.dictConfig(log_config)
        return logging.getLogger('server')