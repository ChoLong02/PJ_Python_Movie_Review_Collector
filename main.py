from common.common_config import CommonConfig
from common.log_config import LogConfig
from collector.movie_review_collector import MovieReviewCollector

import os, json
import logging.config
if __name__ == "__main__":
    
    ##############################
    # 1.Load Config File #
    ##############################
    commonConfig = CommonConfig()
    commonConfig.config_generator()
    config = commonConfig.config_read()

    ##############################
    # 2.Load Log File #
    ##############################
    if not os.path.exists('./common/logs'):
        os.makedirs('./common/logs')
    logConfig = LogConfig()
    log = logConfig.get_logger()

    ##############################
    # 3.Movie Review Collection #
    ##############################
    movie_code = 221031
    try:
        collector = MovieReviewCollector(movie_code)
        collector.movie_review_crawler()
    except Exception as e:
        print(e)
        log.error('Collector is not working.')
    finally:
        pass
