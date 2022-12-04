# https://www.geeksforgeeks.org/put-method-python-requests/
import json
from pprint import pprint

import requests

# Making a PUT request
r = requests.put('https://httpbin.org/put', data={'key': 'value'})

# check status code for response received
# success code - 200
pprint(r)

# print content of request
print(r.text)  # 返回的是Unicode型的数据(取文本)
print(r.content)  # 返回的是bytes型的数据(取图片，文件)
print(r.json())  # 返回的是json格式数据；dict
