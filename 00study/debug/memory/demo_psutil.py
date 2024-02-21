import os
import time

import psutil


def get_process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


def elapsed_since(start):
    return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))


def profile(func):
    def wrapper(*args, **kwargs):
        mem_before = get_process_memory()
        start = time.time()

        result = func(*args, **kwargs)

        elapsed_time = elapsed_since(start)
        mem_after = get_process_memory()
        print("{}: memory before: {:,}, after: {:,}, consumed: {:,}; exec time: {}".format(func.__name__, mem_before, mem_after, mem_after - mem_before, elapsed_time))
        return result

    return wrapper


@profile
def demo_profile():
    a = [1] * (10 ** 6)
    b = [2] * (10 ** 6)
    time.sleep(10)


if __name__ == '__main__':
    demo_profile()
