# 记录日志的模块

import os
import pathlib
import sys

os.environ['LOGURU_AUTOINIT'] = '0'
from loguru import logger

logger.info("If you're using Python {}, prefer {feature} of course!", 3.6, feature="f-strings")

# 终端日志输出格式
stdout_fmt = (
    '<cyan>{time:HH:mm:ss.SSS}</cyan> '
    '[<level>{level: <8}</level>] '
    '<blue>{module}</blue>:<cyan>{line}</cyan> - '
    '<level>{message}</level>'
)
# 日志文件记录格式
# logfile_fmt = (
#     '<light-green>{time:YYYY-MM-DD HH:mm:ss.SSS}</light-green> '
#     '[<level>{level: <8}</level>] '
#     '<cyan>{process.name}({process.id})</cyan>:'
#     '<cyan>{thread.name: <10}({thread.id: <5})</cyan> | '
#     '<blue>{name}</blue>:<blue>{function}</blue>:'
#     '<blue>{line}</blue> - <level>{message}</level>'
# )

# 内置格式
# LOGURU_FORMAT = (
#     "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
#     "<level>{level: <8}</level> | "
#     "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
# )
# 日志文件记录格式
logfile_fmt = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<blue>{process.name}({process.id})</blue>:<blue>{thread.name: <10}({thread.id: <5})</blue> | "
    "<cyan>{name}</cyan>:<cyan>{file}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

log_path = pathlib.Path(__file__).parent.resolve().joinpath('logs')
if not log_path.is_dir():
    log_path.mkdir()
log_path = log_path.joinpath('web.log').resolve()

# logger.remove(0)
# logger.level(name='TRACE', no=5, color='<cyan><bold>', icon='✏️')
# logger.level(name='DEBUG', no=10, color='<blue><bold>', icon='🐞 ')
# logger.level(name='INFOR', no=20, color='<green><bold>', icon='ℹ️')
# logger.level(name='ALERT', no=30, color='<yellow><bold>', icon='⚠️')
# logger.level(name='ERROR', no=40, color='<red><bold>', icon='❌️')
# logger.level(name='FATAL', no=50, color='<RED><bold>', icon='☠️')
if not os.environ.get('PYTHONIOENCODING'):  # 设置编码
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# logger.remove()  # Remove all handlers added so far, including the default one.
logger.add(sys.stderr, level='INFO', format=logfile_fmt, enqueue=True)


# logger.add(log_path, level='DEBUG', format=logfile_fmt, enqueue=True, encoding='utf-8')


def func1():
    logger.debug("debug")
    logger.info("func1 info")
    pass


def func2():
    func1()


def main():
    func2()


# 您是否曾经看到程序意外崩溃而没有在日志文件中看到任何内容？
# 您是否注意到线程中发生的异常没有被记录？
# 这可以使用装饰器/上下文管理器来解决 catch()
# 该管理器可确保将任何错误正确传播到 . logger
@logger.catch
def my_function(x, y, z):
    # An error? It's caught anyway!
    return 1 / (x + y + z)


def recipes():
    import hashlib
    import hmac
    import pickle

    def client(connection):
        data = pickle.dumps("Log message")
        digest = hmac.digest(b"secret-shared-key", data, hashlib.sha1)
        connection.send(digest + b" " + data)

    def server(connection):
        expected_digest, data = connection.read().split(b" ", 1)
        data_digest = hmac.digest(b"secret-shared-key", data, hashlib.sha1)
        if not hmac.compare_digest(data_digest, expected_digest):
            print("Integrity error")
        else:
            message = pickle.loads(data)
            logger.info(message)


# 动态调整记录消息的颜色和格式
from collections import defaultdict
from random import choice

colors = ["blue", "cyan", "green", "magenta", "red", "yellow"]
color_per_module = defaultdict(lambda: choice(colors))


def formatter_(record):
    color_tag = color_per_module[record["name"]]
    return "<" + color_tag + ">[{name}]</> <bold>{message}</>\n{exception}"


def rainbow(text):
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
    chars = ("<{}>{}</>".format(colors[i % len(colors)], c) for i, c in enumerate(text))
    return "".join(chars)


def formatter(record):
    rainbow_message = rainbow(record["message"])
    # Prevent '{}' in message (if any) to be incorrectly parsed during formatting
    escaped = rainbow_message.replace("{", "{{").replace("}", "}}")
    return "<b>{time}</> " + escaped + "\n{exception}"


class Formatter:
    def __init__(self):
        self.padding = 0
        self.fmt = "{time} | {level: <8} | {name}:{function}:{line}{extra[padding]} | {message}\n{exception}"

    def format(self, record):
        length = len("{name}:{function}:{line}".format(**record))
        self.padding = max(self.padding, length)
        record["extra"]["padding"] = " " * (self.padding - length)
        return self.fmt


# formatter = Formatter()
#
# logger.remove()
# logger.add(sys.stderr, format=formatter.format)
if __name__ == '__main__':
    # logger.add(sys.stderr, format=formatter)
    # logger.remove(None)
    # LOGURU_FORMAT = (
    #     "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    #     "<level>{level: <8}</level> | "
    #     "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    # )
    # logger.add(sys.stderr, format=LOGURU_FORMAT)
    logger.info("test")

    # recipes()

    # main()
    # my_function(0, 0, 0)

    # logger.remove(handler_id=None)
    # logger.add(sys.stderr, format="{extra[ip]} {extra[user]} {message}")
    # context_logger = logger.bind(ip="192.168.0.1", user="someone")
    # context_logger.info("Contextualize your logger easily")
    # context_logger.bind(user="someone_else").info("Inline binding of extra attribute")
    # context_logger.info("Use kwargs to add context during formatting: {user}", user="anybody")

    # logger.opt(exception=True).info("Error stacktrace added to the log message (tuple accepted too)")
    # logger.opt(colors=True).info("Per message <blue>colors</blue>")
    # logger.opt(record=True).info("Display values from the record (eg. {record[thread]})")
    # logger.opt(raw=True).info("Bypass sink formatting\n")
    # # logger.opt(depth=1).info("Use parent stack context (useful within wrapped functions)")
    # logger.opt(capture=False).info("Keyword arguments not added to {dest} dict", dest="extra")

    # new_level = logger.level("SNAKY", no=38, color="<yellow>", icon="🐍")
    # logger.log("SNAKY", "Here we go!")

    #    export LOGURU_FORMAT="{time} | <lvl>{message}</lvl>"
    # def specific_only(record):
    #     return "specific" in record["extra"]
    #
    # logger.add("specific.log", filter=specific_only)
    #
    # specific_logger = logger.bind(specific=True)
    #
    # logger.info("General message")  # This is filtered-out by the specific sink
    # specific_logger.info("Module message")  # This is accepted by the specific sink (and others)

    # # Only write messages from "a" logger
    # logger.add("a.log", filter=lambda record: record["extra"].get("name") == "a")
    # # Only write messages from "b" logger
    # logger.add("b.log", filter=lambda record: record["extra"].get("name") == "b")
    #
    # logger_a = logger.bind(name="a")
    # logger_b = logger.bind(name="b")
    #
    # logger_a.info("Message A")
    # logger_b.info("Message B")
    # logger.remove(0)
    # fmt = "{time} - {name} - {level} - {message}"
    # logger.add("spam.log", level="DEBUG", format=fmt)
    # logger.add(sys.stderr, level="ERROR", format=fmt)
    # logger.info("test")
    # logger.error("Debug error:", exc_info=True)
    # logger.opt(exception=True).debug("Debug error:")



# LOGURU_FORMAT=
# <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>_{level}_<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>|   <level>{message}</level>