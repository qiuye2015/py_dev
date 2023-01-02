import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from typing import Dict

loggers: Dict[str, logging.Logger] = {}

# FORMATTER = '[%(levelname)-.1s][%(asctime)s][%(process)s]' \
#             '[%(filename)s:%(lineno)d]: %(message)s'
# FORMATTER = '%(levelname)-.1s - %(asctime)s - %(message)s - %(filename)s:%(lineno)d - %(funcName)s'
FORMATTER = '%(levelname)-.1s - %(asctime)s - %(filename)s:%(lineno)d (%(funcName)s) - %(message)s'


# FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"


# color formatter
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey + FORMATTER + reset,
        logging.INFO: grey + FORMATTER + reset,
        logging.WARNING: yellow + FORMATTER + reset,
        logging.ERROR: red + FORMATTER + reset,
        logging.CRITICAL: bold_red + FORMATTER + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter())
    return console_handler


def get_file_handler(filename):
    file_handler = TimedRotatingFileHandler(filename, when='midnight')
    file_handler.setFormatter(logging.Formatter(FORMATTER))
    return file_handler


def get_logger(logger_name=__name__, filename=None, dir_name='log'):
    if logger_name in loggers:
        return loggers[logger_name]

    os.makedirs(dir_name, exist_ok=True)
    _logger = logging.getLogger(logger_name)
    _logger.setLevel(logging.DEBUG)
    _logger.addHandler(get_console_handler())
    if filename:
        _logger.addHandler(get_file_handler(f"{dir_name}/{filename}"))
    # with this pattern, it's rarely necessary to propagate the error up to parent
    _logger.propagate = False

    loggers[logger_name] = _logger
    return _logger


if __name__ == '__main__':
    logger = get_logger(filename="app.log")
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
