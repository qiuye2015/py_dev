#!/usr/bin/env python
# coding=utf-8
# 日志产生器
import random
import time

url_path = [
    "class/112.html",
    "class/128.html",
    "class/145.html",
    "class/146.html",
    "class/131.html",
    "class/120.html",
    "learn/821",
    "course/list"
]

ip_slices = [132,156,124,10,29,167,143,187,30]

def sample_url():
    return random.sample(url_path, 1)[0]
     
def sample_ip():
    slice = random.sample(ip_slices,4)
    return ".".join([str(item) for item in slice])

def generage_log(count = 10):
    f = open("./access.log","w+")
    time_str = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    while count>=1:
        query_log = "{local_time}\t{url}\t{ip}".format(local_time=time_str,url=sample_url(),ip=sample_ip())
        print(query_log)
        f.write(query_log + "\n")
        count = count - 1
    f.close()


if __name__ =='__main__':
    generage_log()
