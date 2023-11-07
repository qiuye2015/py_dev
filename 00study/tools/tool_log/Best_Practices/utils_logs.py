from modules import logger


def log_test():
    logger.info("This is a Info")
    logger.debug("This is a Debug")
    logger.warning("This is a Warning")
    logger.error("This is a Error")
    import logging

    logging.debug("logging debug")
    logging.info("logging info")


def main():
    log_test()


if __name__ == '__main__':
    main()
