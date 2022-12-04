import logging
import sys
import traceback

from .log import create_logger

__logger_name = 'test_logger'
create_logger(__logger_name, 'applog3.log', 'logs')

logger = logging.getLogger(__logger_name)


# from tool_log import logger

# make Python output exceptions in one line / via logging
def exception_logging(exctype, value, tb):
    """
    Log exception by using the root logger.

    Parameters
    ----------
    exctype : exception type
    value : seems to be the Exception object (with its message)
    tb : traceback
    """
    # logging.error(''.join(traceback.format_exception(exctype, value, tb)))
    write_val = {'exception_type': str(exctype),
                 'message': str(traceback.format_tb(tb, 10))}
    logger.exception(str(write_val))


sys.excepthook = exception_logging
