import logging
import random
import json
from copy import copy

import requests


class Response(object):
    """
    workflow3 结果标准返回
    {
        request_id: "xxxxxx",
        result_code: "xxx",
        data: {}
    }
    """

    @staticmethod
    def new_success(request_id, content: dict):
        return {
            "request_id": request_id,
            "result_code": "success",
            "data": {
                "context": content
            }
        }

    @staticmethod
    def new_fail(request_id, content: dict):
        return {
            "request_id": request_id,
            "result_code": "fail",
            "data": {
                "context": content
            }
        }


# print(Response().new_success("12", "45"))
# print(Response.new_success("12", "45"))

import http.client

conn = http.client.HTTPSConnection("rocket.nioint.com")
payload = ''
headers = {
    'X-Domain-Id': 'leo.fu1',
    'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
    'Accept': '*/*',
    'Host': 'rocket.nioint.com',
    'Connection': 'keep-alive',
    'Cookie': 'tgw_l7_route=a896113948d5b576a484803cfe70c6ac'
}
id = "TRWXFQXLCH-2022112519792-1033"
id = "DRWXFQXLCH-2022112520970-8820"
conn.request("GET", f"/api/v1/instance/{id}", payload, headers)
res = conn.getresponse()
data = res.read()
# print(data.decode("utf-8"))
dataDict = json.loads(data)
print(dataDict.get("data").get("status"))
# error

# deny scan
id = "TYJSHQLCHS-2022112518150-1243"
id = "DYJSHQ-2022112520470-8828"
conn.request("GET", f"/api/v1/instance/{id}", payload, headers)
res = conn.getresponse()
data = res.read()
# print(data.decode("utf-8"))
dataDict = json.loads(data)
print(dataDict.get("data").get("status"))