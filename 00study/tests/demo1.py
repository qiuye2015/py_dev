from loguru import logger


def main():
    # while True:
    logger.trace("A trace message.")
    logger.debug("A debug message.")
    logger.info("An info message.")
    logger.success("A success message.")
    logger.warning("A warning message.")
    logger.error("An error message.")
    logger.critical("A critical message.")
    # time.sleep(1)


if __name__ == '__main__':
    main()



