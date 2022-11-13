import time, functools


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kv):
        print(f'call {func.__name__}():')
        return func(*args, **kv)

    return wrapper


@log
def now():
    print('2022-11-10')


now()


# 把@log放到now()函数的定义处，相当于执行了语句
# now = log(now)

# 如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数
def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)

        return wrapper

    return decorator


@log('execute')
def now():
    print('2015-3-25')


#  now = log('execute')(now)

now()


# 需要把原始函数的__name__等属性复制到wrapper()函数中，否则，有些依赖函数签名的代码执行就会出错
# 只需记住在定义wrapper()的前面加上@functools.wraps(func)即可
#


def metric(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kv):
        start = time.time()
        ret = fn(*args, **kv)
        end = time.time()
        print('%s executed in %s ms' % (fn.__name__, end - start))
        return ret

    return wrapper


@metric
def fast(x, y):
    time.sleep(0.0012)
    return x + y;


@metric
def slow(x, y, z):
    time.sleep(0.1234)
    return x * y * z;


f = fast(11, 22)
s = slow(11, 22, 33)
if f != 33:
    print('测试失败!')
elif s != 7986:
    print('测试失败!')


def outer(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        # 执行前
        # 调用原来的函数
        res = func(*args, **kwargs)
        # 执行后
        return res

    return inner


@outer
def test():
    pass


# 如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数
def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)

        return wrapper

    return decorator


