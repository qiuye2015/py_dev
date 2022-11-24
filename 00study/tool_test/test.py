import logging
import random
import json
from copy import copy


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


print(Response().new_success("12", "45"))
