from tool_log.get_logger import get_logger

logger = get_logger()


def print_hi(name):
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')
    logger.debug("This is applog, debug")
    logger.info("This is applog, info")

