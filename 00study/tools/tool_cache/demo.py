import cachetools

#
# @lru_cache(maxsize=2)
# def demo(a, b):
#     print('开始计算a+b的值...')
#     return a + b
#
#
# print(demo(1, 1))
# print(demo(2, 2))
# print(demo(3, 3))
# print("*" * 10)
# print(demo(3, 3))
# print(demo(2, 2))
# print(demo(1, 1))

#
# @functools.cache
# def get_sum_cached2(a, b):
#     time.sleep(2)  # to mimic expensive calculations
#     return a + b
#
#
# print(get_sum_cached2(1, 2))  # firstly cost 2 seconds to print 3
# print("*" * 20)
# print(get_sum_cached2(1, 2))  # print 3 immediately


cache = cachetools.FIFOCache(maxsize=3)
cache[1] = 1
cache[2] = 2
cache[3] = 3
print(1, cache[1])
print(3, cache[3])
print("*" * 10)
cache[4] = 4
print("*" * 10)

print(1, cache.get(1))
print(3, cache[3])
print(4, cache[4])

import datetime

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
namespace = "a/b/"
print(namespace.rstrip('/'))
