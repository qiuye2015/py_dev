from loguru import logger

# logger.add("logs/tdsql2es.log", rotation="1 KB", retention=3)
logger.add("logs/tdsql2es.log", rotation="00:01", retention=2)
# logger.add("logs/tdsql2es.log", rotation="10h", retention=3)
# logger.add("logs/tdsql2es.log", rotation="1min", retention=3)


def main():
    import time
    while True:
        logger.debug("this is debug")
        logger.info("this is info")
        logger.warning("this is warn")
        logger.error("this is error")
        time.sleep(1)


if __name__ == '__main__':
    main()
