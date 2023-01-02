# coding: utf-8
import datetime
import logging
import time


# 1秒 = 1000毫秒
# 1毫秒 = 1000微秒
# 1微秒 = 1000纳秒
# time 模块中定义的大多数函数的实现都是调用其所在平台的C语言库的同名函数
# datetime.now(tz=None) 该方法会在可能的情况下提供比通过 time.time() 时间戳所获时间值更高的精度
# 该time模块主要用于处理 Unix 时间戳；表示为自 Unix 纪元以来的秒数的浮点数。
# 该datetime模块可以支持许多相同的操作，但提供了更多面向对象的类型集，并且对时区的支持也有限
def now_ns() -> int:
    return time.time_ns()


# 微秒级时间戳:16位
def now_us() -> int:
    return int(round(time.time() * 1000000))


# 毫秒级时间戳:13位
def now_ms() -> int:
    return int(round(now_us() / 1000))


# 秒级时间戳:10位
def now_s() -> int:
    return int(round(now_ms() / 1000))


# Get the epoch (纪元)
def get_epoch():
    obj = time.gmtime(0)
    epoch = time.asctime(obj)
    print("epoch is:", epoch)
    return epoch


def current_microsecond() -> int:
    return int(datetime.datetime.now().timestamp() * 1000000)


def current_milliseconds() -> int:
    return int(datetime.datetime.now().timestamp() * 1000)


def current_seconds() -> int:
    return int(datetime.datetime.now().timestamp())


# 获取当前日期时间
def current_seconds_str() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def current_microsecond_str() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')


# 将时间戳转为日期
def nano_time_format_to_date(time_nano: int) -> int:
    try:
        time_sec = time_nano / 1000000000
        time_str = datetime.datetime.fromtimestamp(time_sec).strftime("%Y%m%d")
        return int(time_str)
    except Exception as ex:
        logging.error("time: %s cast error, errmsg: %s", time_nano, ex)
        return 0


def nano_time_format_to_sec(time_nano: int) -> int:
    try:
        time_sec = time_nano / 1000000000
        time_str = datetime.datetime.fromtimestamp(time_sec).strftime("%Y%m%d%H%M%S")
        return int(time_str)
    except Exception as ex:
        logging.error("time: %s cast error, errmsg: %s", time_nano, ex)
        return 0


def time_format_to_date(time_sec: int) -> str:
    try:
        time_str = datetime.datetime.fromtimestamp(time_sec).strftime("%Y-%m-%d %H:%M:%S")
        return time_str
    except Exception as ex:
        logging.error("time: %s cast error, errmsg: %s", time_sec, ex)
        return ""


def ms_time_format_to_date(time_ms: int) -> str:
    try:
        time_str = datetime.datetime.fromtimestamp(time_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
        return time_str
    except Exception as ex:
        logging.error("time: %s cast error, errmsg: %s", time_ms, ex)
        return ""


# 将日期转为秒级时间戳  dt = '2018-01-01 10:40:30'
def date_format_to_time(dt: str) -> int:
    ts = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
    return ts


def get_day_of_day(n=0, with_ms=False):
    """
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    """
    if n < 0:
        n = abs(n)
        ret = datetime.datetime.now() - datetime.timedelta(days=n)
    else:
        ret = datetime.datetime.now() + datetime.timedelta(days=n)
    if with_ms:
        return ret
    return ret.strftime("%Y:%m:%d %H:%M:%S")


def after_time_delta(days=0, hours=0, minutes=0, seconds=0, use_timestamp=False):
    ret = datetime.datetime.now() + \
          datetime.timedelta(days=days,
                             hours=hours,
                             minutes=minutes,
                             seconds=seconds)
    if use_timestamp:
        return ret
    return ret.strftime("%Y:%m:%d %H:%M:%S")


def before_time_delta(days=0, hours=0, minutes=0, seconds=0, use_timestamp=False):
    ret = datetime.datetime.now() - \
          datetime.timedelta(days=days,
                             hours=hours,
                             minutes=minutes,
                             seconds=seconds)
    if use_timestamp:
        return ret
    return ret.strftime("%Y:%m:%d %H:%M:%S")


# def fmt(func):
#     print(func.__name__, func())

import time
import pytz
from datetime import datetime


def timestamp2formatter(timestamp: float, timezone: str = None) -> str:
    formatter = '%Y%m%dT%H%M%S'
    if timezone is None:
        return time.strftime(formatter, time.localtime(timestamp))
    else:
        tz = pytz.timezone(timezone)
        dt = pytz.datetime.datetime.fromtimestamp(timestamp, tz)
        return dt.strftime(formatter)


def formatter2timestamp(yyyyMMddTHHMMSS: str, timezone: str = 'Asia/Shanghai') -> float:
    tz = pytz.timezone(timezone)
    formatter = "%Y%m%dT%H%M%S"
    strptime = datetime.strptime(yyyyMMddTHHMMSS, formatter)
    return tz.localize(strptime).timestamp()

if __name__ == '__main__':
    print(now_ns())
    print(now_us())
    print(now_ms())
    print(now_s())
    # print(get_epoch())
    print(current_microsecond())
    print(current_milliseconds())
    print(current_seconds())
    print(current_seconds_str())
    print(current_microsecond_str())
    print(nano_time_format_to_date(now_ns()))
    print(nano_time_format_to_sec(now_ns()))
    print(date_format_to_time(current_seconds_str()))

    print("*" * 10)
    print(current_seconds_str())
    print(after_time_delta(days=1, minutes=10))
    print(before_time_delta(days=1, minutes=10))

    print(after_time_delta(minutes=1440))
    print(get_day_of_day(10))
    print(time_format_to_date(1670771129))

    print(time_format_to_date(1671176729707))
