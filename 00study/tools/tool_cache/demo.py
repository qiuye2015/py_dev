from functools import lru_cache


@lru_cache(maxsize=2)
def demo(a, b):
    print('开始计算a+b的值...')
    return a + b


print(demo(1, 1))
print(demo(2, 2))
print(demo(3, 3))
print("*" * 10)
print(demo(3, 3))
print(demo(2, 2))
print(demo(1, 1))
