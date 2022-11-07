import os
import logging
import logging.handlers


def create_logger(logger_name, file_name, dir_name):
    os.makedirs(dir_name, exist_ok=True)
    # formatter = ('[%(asctime)s] [%(process)s:%(thread)d] [%(levelname)-.1s] '
    #              '[%(filename)s:%(lineno)4dL]: %(message)s')
    formatter = '[%(levelname)-.1s][%(asctime)s][%(process)s]' \
                '[%(filename)s:%(lineno)d:%(funcName)s]: %(message)s '
    filehandler = logging.FileHandler(f"{dir_name}/{file_name}")
    filehandler.setLevel(logging.DEBUG)  # TODO:
    filehandler.setFormatter(logging.Formatter(formatter))

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)  # TODO:
    console.setFormatter(logging.Formatter(formatter))

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console)
    logger.addHandler(filehandler)
