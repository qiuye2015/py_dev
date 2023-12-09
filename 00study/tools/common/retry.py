import functools
import time


# 装饰器模块，需要传入参数(重试次数, 重试间隔/second)
def retry(retry_times=2, retry_interval=0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retried = 0
            while retried <= retry_times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retried += 1
                    if retried > retry_times:
                        raise e
                    print(f"func: {func.__name__} exception occurred: {e}, and retry after {retry_interval} seconds, {retried} times")
                    time.sleep(retry_interval)

        return wrapper

    return decorator


@retry(retry_times=2, retry_interval=2)
def func_test(msg):
    print(msg)
    raise Exception('test except')


if __name__ == '__main__':
    # func_test("fjp test")
    # 获取被装饰器修饰过的函数的函数名
    print(func_test.__name__)
