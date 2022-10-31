import logging
import logging.config
import os
from os import path
import time


def get_logger(conf="applog"):
    os.makedirs('logs', exist_ok=True)
    # log_file_path = path.join(path.dirname(path.abspath(__file__)), '../conf/logging.conf')
    # print(log_file_path)
    logging.config.fileConfig("conf/logging.conf")
    return logging.getLogger(conf)


def main():
    logger = get_logger()
    logger.debug('Debugging')
    logger.info('Finished')
    logger.warning('Warning')
    logger.error('Error')
    logger.debug("process_msg {} {} {}".format("test", 1, True))
    logger.critical('Critical')


if __name__ == '__main__':
    main()
