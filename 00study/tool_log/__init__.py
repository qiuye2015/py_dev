import logging
from .log import create_logger

__logger_name = 'test_logger'
create_logger(__logger_name, 'applog3.log', 'logs')

logger = logging.getLogger(__logger_name)
# from tool_log import logger
