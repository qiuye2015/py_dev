#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import time


def sing():
    for i in range(5):
        print('sing', i)
        time.sleep(1)


def dance():
    for i in range(5):
        print('dance ', i)
        time.sleep(1)


# 2 用类继承
class MyThread(threading.Thread):
    def login(self):
        print('login...')

    def run(self):  # 必须定义
        print('threading run...')
        self.login()


def main():
    # 多线程的两种使用方式
    # 1 直接使用
    # nums = [11,22]
    # t1 = threading.Thread(target=sing，args=(nums,))  # 参数为元组
    # t2 = threading.Thread(target=dance)

    # t1.start()
    # t2.start()

    # t1.join
    # t2.join

    t = MyThread()
    t.start()

if __name__ == "__main__":
    main()
