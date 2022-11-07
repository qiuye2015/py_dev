# from tool_log.get_logger import get_logger
# from tool_log.init_logger import Logger
from tool_log import logger as logger3
#
# logger1 = get_logger(conf='applog')
# logger2 = Logger(__name__).get_log()


def print_hi(name):
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')
    # logger1.debug("[logger1] This is applog, debug")
    # logger1.info("[logger1] This is applog, info")
    #
    # logger2.debug("[logger2] This is applog, debug")
    # logger2.info("[logger2] This is applog, info")

    logger3.debug("[logger3] This is applog, debug")
    logger3.info("[logger3] This is applog, info")
