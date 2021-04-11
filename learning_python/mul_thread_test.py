#!/usr/bin/env python
# coding=utf-8
import Queue
import threading

def basic_worker(queue):
    """
    工作者，当队列中没有任务的时候就执行退出。
    """
    while True:
        item = queue.get()
        if item is None:
            break
        print item
        queue.task_done()


def basic():
    """
    主线程，队列中总共放了4个任务。
    """
    print 'start'
    queue = Queue.Queue()
    for i in range(4):
        t = threading.Thread(target=basic_worker, args=(queue,))
        t.daemon = True #　这里daemon必须等于True才能程序才能退出
        t.start()
    for item in range(4):
        queue.put(item)
    queue.join()       # block until all tasks are done
    print 'got here'

if __name__ == '__main__':
    basic()
