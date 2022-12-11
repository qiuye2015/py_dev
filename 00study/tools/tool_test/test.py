import logging
import os
import random
import json
import traceback
from copy import deepcopy
import time
import datetime
from time import sleep


def current_seconds() -> int:
    return int(datetime.datetime.now().timestamp())


print(current_seconds())
a = datetime.datetime.now()  # 获取当前时间
b = (a + datetime.timedelta(days=3))  # 获取3天后的时间
# c = time.mktime(b.timetuple())  # 将时间转换为时间戳
# d = time.localtime(c)  # 将时间戳转换成时间组
# e = time.strftime("%Y：%m：%d %H:%M:%S", d)

f = b.strftime("%Y:%m:%d %H:%M:%S")

print(a)
print(b)
# print(c)
# print(d)
# print(e)
print(f)

kwargs = {
    "data_type": "dlb",
    "clip_id_or_uuid": "123",
    "namespace": "namespace",
    "region": "region",
}

kwargs_str = json.dumps(kwargs)
print(kwargs_str)

d = json.loads(kwargs_str)
print(d)
print(d['data_type'])

# 创建数据源
day_start_ms = int(time.mktime(datetime.date.today().timetuple())) * 1000
day_end__ms = day_start_ms + 24 * 3600 * 1000 *3
now = int(datetime.datetime.now().timestamp() * 1000)
print(day_start_ms)
print(day_end__ms/1000)
print(now)

kwargs2 = {
    "data_type": "dlb",
    "clip_id_or_uuid": "123",
    "namespace": "namespace",
    "region": "region",
}
kwargs_input = []
kwargs_input.append({"kwargs": json.dumps(kwargs)})
kwargs_input.append({"kwargs": json.dumps(kwargs2)})
print(kwargs_input)
