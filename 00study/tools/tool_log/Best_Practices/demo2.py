
from log import get_logger
logger = get_logger(__name__, filename="app2.log")


def test():
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
