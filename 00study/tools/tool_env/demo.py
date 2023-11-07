import os

# 获取环境变量的键值对
env_map_str = os.environ.get('MY_ENV_MAP')

# 将环境变量的字符串解析为字典
env_map = eval(env_map_str)


# 定义要执行的函数
def my_function(input_str):
    return "Hello " + input_str


# 使用环境变量中的值作为函数的输入，并执行函数
for key, value in env_map.items():
    result = my_function(value)
    print(f"{key}: {result}")
