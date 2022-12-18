
from log import get_logger
from demo2 import test
logger = get_logger("main", filename="app.log")
# 除了主函数需要指定logger_name,其他全用__name__


def main_test():
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    test()


main_test()

a = 1
