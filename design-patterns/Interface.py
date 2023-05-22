from abc import ABCMeta, abstractmethod


# 接口类
# class Payment():
class Payment(metaclass=ABCMeta):
    @abstractmethod
    def pay(self, money):
        pass


# # 类 Alipay 必须实现所有 abstract 方法
# # TODO add: def pay(self, money):
# class Alipay(Payment):
#     pass


class Wechatpay(Payment):
    def pay(self, money):
        pass


class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class MyClass(Singleton):
    def __init__(self, a):
        self.a = a


A = MyClass(10)
B = MyClass(20)
print(A.a, B.a)  # 20 20
print(id(A), id(B))  # 4337697792 4337697792
