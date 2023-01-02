import datetime
import json
import sys

import functools
import time

from loguru import logger


# 根据大小和时间轮换日志文件
class Rotator:
    def __init__(self, *, size, at):
        now = datetime.datetime.now()

        self._size_limit = size
        self._time_limit = now.replace(
            hour=at.hour, minute=at.minute, second=at.second)

        if now >= self._time_limit:
            # The current time is already past the target time, so it would rotate already.
            # Add one day to prevent an immediate rotation.
            self._time_limit += datetime.timedelta(days=1)

    def should_rotate(self, message, file):
        file.seek(0, 2)
        if file.tell() + len(message) > self._size_limit:
            return True
        if message.record["time"].timestamp() > self._time_limit.timestamp():
            self._time_limit += datetime.timedelta(days=1)
            return True
        return False


simple_formatter = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | " \
                   "<level>{level: <8}</level> | " \
                   "<cyan>[{file.name}:{line}]</cyan> " \
                   "<blue>{name}:{function}</blue> " \
                   "- <level>{message}</level> "

simple_extra_formatter = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | " \
                         "<level>{level: <8}</level> | " \
                         "<cyan>[{file.name}:{line}]</cyan> " \
                         "<blue>{name}:{function}</blue> " \
                         "- <level>{message}</level> " \
                         "| {extra}"


def logger_config(filepath: str = None, level: str = 'DEBUG', formatter=simple_formatter, **kwargs) -> None:
    """
    Define loggers for file output and stderr.
    param filepath: Where to save log output.
    param level: Log level. eg: TRACE DEBUG INFO SUCCESS WARNING ERROR CRITICAL
    param kwargs: Any keyword arguments valid in logger.add() method.
    """
    # 删除默认处理程序（其 ID 为0）的配置
    # logger.remove(0)
    # 删除所有处理程序
    logger.remove(handler_id=None)

    logger.add(sink=sys.stdout,
               level=level,
               format=formatter,
               )

    if filepath:
        # Rotate file if over 500 MB or at midnight every day
        rotator = Rotator(size=5e+8, at=datetime.time(0, 0, 0))
        logger.add(sink=filepath,
                   level=level,
                   rotation=rotator.should_rotate,
                   format=formatter,
                   **kwargs
                   # 指定关闭当前日志文件并创建新文件的条件。
                   # 此条件可以是int,datetime或 str,str建议使用，因为它更易于阅读
                   # 当rotation有一个int值时，它对应于当前文件在创建新文件之前允许容纳的最大字节数
                   # 当它有一个datetime.timedelta值时，它表示每次旋转的频率，
                   # 同时datetime.time指定每次旋转应该发生的时间
                   # rotation还可以取一个str值，它是上述类型的人性化变体。
                   # encoding="utf-8",
                   # retention=3,    # 指定每个日志文件在从文件系统中删除之前将如何保留

                   # filter=""       # 决定一个记录是否应该被记录
                   # colorize=True,  # 是否启用终端着色
                   # serialize=True, # 日志记录以 JSON 格式呈现
                   # backtrace=True, # 确定异常跟踪是否应扩展到捕获错误点之外，从而使调试更容易
                   # diagnose=True,  # 确定变量值是否应显示在异常跟踪中
                   # enqueue=True,   # 将日志记录放入队列中，以避免多个进程记录到同一目的地时发生冲突
                   # catch=True,     # 如果在记录到指定sink时发生意外错误,错误将打印到标准错误
                   )

    return


# 使用装饰器记录函数的进入和退出,记录函数时间
def logger_wraps(*, entry_=True, exit_=True, level_="DEBUG", cost_=True):
    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry_:
                logger_.log(
                    level_, "Entering '{}' (args={}, kwargs={})", name, args, kwargs)
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            if exit_:
                logger_.log(level_, "Exiting '{}' (result={})", name, result)
            if cost_:
                logger_.log(
                    level_, "Function '{}' executed in {:f} s", name, end - start)
            return result

        return wrapped

    return wrapper


# def level_filter(level):
#     def is_level(record):
#         return record["level"].name == level
#
#     return is_level


# def serialize(record):
#     subset = {
#         "timestamp": record["time"].timestamp(),
#         "message": record["message"],
#         "level": record["level"].name,
#     }
#     return json.dumps(subset)
#
#
# def patching(record):
#     record["extra"]["serialized"] = serialize(record)


# logger = logger.patch(patching)
# logger.add(sink=sys.stdout,
#            level="DEBUG",
#            # format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
#            format="{extra[serialized]}",
#            filter=level_filter(level="WARNING"),
#            serialize=True,
#            )


@logger_wraps()
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

    childLogger = logger.bind(seller_id="001", product_id="123")
    childLogger.info("product page opened")

    def log():
        logger.info("A user requested a service.")

    with logger.contextualize(seller_id="001", product_id="123"):
        log()

    logger.info("INFO message end")


if __name__ == '__main__':
    logger_config()
    # logger_config(filepath='app.log')
    main()
