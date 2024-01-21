from functools import wraps
from threading import RLock
import time


def timer(func):
    """测量执行时间"""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute.")
        return result

    return wrapper


# 如果装饰器不希望跟print函数耦合，可以编写可以参数化的装饰器
def record(output):
    """可以参数化的装饰器"""

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            output(func.__name__, time() - start)
            return result

        return wrapper

    return decorate


class Record():
    """通过定义类的方式定义装饰器"""

    def __init__(self, output):
        self.output = output

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            self.output(func.__name__, time() - start)
            return result

        return wrapper


def log_results(func):
    """日志输出"""

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open("results.log", "a") as log_file:
            log_file.write(f"{func.__name__} - Result: {result}\n")
            print(f"{func.__name__} - Result: {result}")
        return result

    return wrapper


def memoize(func):
    """
    缓存结果
    """
    cache = {}

    def wrapper(*args):
        if args in cache:
            print(f"{args} Hit cache")
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


def suppress_errors(func):
    """优雅的错误处理"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            return None

    return wrapper


def retry(max_attempts, delay):
    """重试执行"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(
                        f"Attempt {attempts + 1} failed. Retrying in {delay} seconds. Error: {e}"
                    )
                    attempts += 1
                    time.sleep(delay)
            raise Exception("Max retry attempts exceeded.")

        return wrapper

    return decorator


def debug(func):
    """打印函数的输入参数和它们的值，以便于调试"""

    def wrapper(*args, **kwargs):
        print(f"Debugging {func.__name__} - args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)

    return wrapper


@debug
def complex_data_processing(data, threshold=0.5):
    # Your complex data processing code here
    pass


def deprecated(func):
    """处理废弃的函数:一个函数不再被推荐时通知用户"""
    import warnings

    def wrapper(*args, **kwargs):
        warnings.warn(f"{func.__name__} is deprecated and will be removed in future versions.", DeprecationWarning)
        return func(*args, **kwargs)

    return wrapper


# def visualize_results(func):
#     """自动生成漂亮的可视化结果"""
#     import matplotlib.pyplot as plt
#
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         plt.figure()
#         # Your visualization code here
#         plt.show()
#         return result
#
#     return wrapper
# @visualize_results
# def analyze_and_visualize(data):
#     # Your combined analysis and visualization code here
#     pass

# def validate_input(func):
#     """
#     验证函数参数，确保它们在继续计算之前符合特定的标准
#     """
#
#     def wrapper(*args, **kwargs):
#         # Your data validation logic here
#         if valid_data:
#             return func(*args, **kwargs)
#         else:
#             raise ValueError("Invalid data. Please check your inputs.")
#
#     return wrapper
#
#
# def valid_data():
#     pass
#
#
# @validate_input
# def analyze_data(data):
#     # Your data analysis code here
#     pass


# def validate_output(func):
#     """验证函数的输出，确保它在进一步处理之前符合特定的标准"""
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         if valid_output(result):
#             return result
#         else:
#             raise ValueError("Invalid output. Please check your function logic.")
#     return wrapper
#
# @validate_output
# def clean_data(data):
#      pass


@timer
def my_data_processing_function():
    time.sleep(10)


@log_results
def calculate_metrics(data):
    return data


@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@suppress_errors
def preprocess_data(data):
    raise Exception(data)


@retry(max_attempts=3, delay=2)
def fetch_data_from_api(api_url):
    raise Exception("test error")


@deprecated
def old_data_processing(data):
    # Your old data processing code here
    pass


def rate_limit(fn):
    """
    限制函数被执行的频率，比如10秒一次
    """
    start = 0  # 上一次访问的时间

    def inner(*args, **kwargs):
        nonlocal start
        now = time.time()
        if now - start > 10:
            ret = fn(*args, **kwargs)
            start = now
            return ret
        else:
            print(f"访问过于频繁,请于{int(10 - (now - start))}之后访问")

    return inner


@rate_limit
def rate_limit_demo():
    print("visit rate_limit_demo")


# 用装饰器来实现单例模式
def singleton(cls):
    """装饰类的装饰器"""
    instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


# 线程安全的单例装饰器
def singleton(cls):
    """线程安全的单例装饰器"""
    instances = {}
    locker = RLock()

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            with locker:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


@singleton
class President:
    """总统(单例类)"""
    pass


if __name__ == "__main__":
    # my_data_processing_function()
    # print(fibonacci(30))
    # calculate_metrics("success")
    # preprocess_data("test error")
    # fetch_data_from_api("wwww")
    # complex_data_processing("test")
    # old_data_processing("test")

    rate_limit_demo()
    time.sleep(4)
    rate_limit_demo()
