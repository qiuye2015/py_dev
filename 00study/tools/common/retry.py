import time


# 装饰器模块，需要传入参数(重试次数, 重试间隔/second)
def retry(retry_times=2, retry_interval=0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retried = 0
            while retried <= retry_times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retried += 1
                    if retried > retry_times:
                        raise e
                    print("exception occurred: ", e, f", and retry after {retry_interval} seconds")
                    time.sleep(retry_interval)

        return wrapper

    return decorator
