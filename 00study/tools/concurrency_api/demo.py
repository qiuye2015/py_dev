import threading
from threading import Thread, current_thread
from time import sleep

# # function executed in a new thread
# def task():
#     # get the current thread
#     thread = current_thread()
#     # report a message
#     print(f'Hello from a new thread: {thread.name}')
#     # report if daemon thread
#     print(f'Daemon thread: {thread.daemon}')
#
#
# # create a daemon thread with a custom name
# thread = Thread(name='Worker', daemon=True, target=task)
# print(thread.name)
# # start the new thread
# thread.start()
# # wait for the thread to finish
# thread.join()

#####################################################

# # target function that raises an exception
# def work():
#     print('Working...')
#     sleep(1)
#     # rise an exception
#     raise Exception('Something bad happened')
#
#
# # custom exception hook
# def custom_hook(args):
#     # report the failure
#     print(f'Thread failed: {args.exc_value}')
#
#
# # set the exception hook
# threading.excepthook = custom_hook
#
# # create a thread
# thread = Thread(target=work)
# # run the thread
# thread.start()
# # wait for the thread to finish
# thread.join()
# # continue on
# print('Continuing on...')


# import time
# import threading
#
#
# def run(n, se):
#     print("begin the thread: %s" % n)
#     se.acquire()
#     print("run the thread: %s" % n)
#     time.sleep(1)
#     se.release()
#     print("end the thread: %s" % n)
#
#
# # 设置允许5个线程同时运行
# semaphore = threading.BoundedSemaphore(5)
# for i in range(20):
#     t = threading.Thread(target=run, args=(i, semaphore))
#     t.start()

# from bounded_executor import BoundedThreadPoolExecutor
#
#
# def job(i):
#     print(i)
#
#
# with BoundedThreadPoolExecutor(max_workers=10, max_waiting_tasks=50) as pool:
#     for i in range(1000):
#         pool.submit(job, i)


from bounded_pool_executor import BoundedProcessPoolExecutor
from time import sleep
from random import randint


def do_job(num):
    sleep_sec = randint(1, 10)
    print('value: %d, sleep: %d sec.' % (num, sleep_sec))
    sleep(sleep_sec)


with BoundedProcessPoolExecutor(max_workers=5) as worker:
    for num in range(10000):
        print('#%d Worker initialization' % num)
        worker.submit(do_job, num)
