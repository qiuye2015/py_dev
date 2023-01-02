import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED


def spider(page):
    time.sleep(random.randint(1, 10))
    print(int(time.time() * 1000), page, "spider")
    return page


input_list = [2, 3, 1, 4]
futures = {}
with ThreadPoolExecutor() as pool:
    for arg in input_list:
        future = pool.submit(spider, arg)
        # futures.append(future)
        futures[future] = arg

    # wait(futures, return_when=ALL_COMPLETED)
    for future, arg in futures.items():
        print(int(time.time() * 1000), "start", arg)
        print(int(time.time() * 1000), future.result(), arg)
        print(int(time.time() * 1000), "end", arg)



