# 解除分配未使用的对象

class MyClass:
    def __init__(self):
        self.data = [1] * (10 ** 6)

    def process_data(self):
        # Use self.data to process the data
        result = sum(self.data)
        return result


def my_function():
    obj = MyClass()
    result = obj.process_data()
    # Remove the reference to obj to allow it to be deallocated
    obj = None


my_function()


# 使用生成器或迭代器
def my_function():
    def data_generator():
        for i in range(10 ** 6):
            yield i

    result = sum(data_generator())
    print(result)


my_function()


class DataIterator:
    def __init__(self):
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= 10 ** 6:
            raise StopIteration
        self.current += 1
        return self.current


def my_function():
    data = DataIterator()
    result = sum(data)
    print(result)


my_function()

# 使用弱引用
import weakref


class MyClass:
    def __init__(self):
        self.data = [1] * (10 ** 6)


def my_function():
    obj = MyClass()
    # Create a weak reference to obj
    obj_ref = weakref.ref(obj)
    # Remove the reference to obj
    obj = None
    # Check if the object is still alive before accessing its attributes
    if obj_ref() is not None:
        print(obj_ref().data)
    else:
        print('The object has been deallocated')


my_function()
