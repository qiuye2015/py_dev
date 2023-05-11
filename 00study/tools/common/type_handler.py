import ast
import json
import logging
from typing import Union, Dict, List

logger = logging.getLogger(__name__)


class TypeHandler:
    @staticmethod
    def to_int(value):
        if isinstance(value, int):
            return value
        elif isinstance(value, (float, str)):
            try:
                return int(value)
            except ValueError:
                raise TypeError(f"Invalid value: {value}. Cannot convert to int.")
        else:
            raise TypeError(f"Invalid type: {type(value)}. Cannot convert to int.")

    @staticmethod
    def to_json(data: Union[Dict, List, str]) -> str:
        """支持将 dict list str 对象转成 json, 前提是得保证对象满足 json 数据格式"""
        if isinstance(data, (dict, list)):
            return json.dumps(data)
        elif isinstance(data, str):
            try:
                data_dict = json.loads(data)
                return json.dumps(data_dict)
            except json.JSONDecodeError as e:
                logger.warning(f"Error decoding JSON from string: {data}. Error: {str(e)}")
            try:
                data_dict = ast.literal_eval(data)
                return json.dumps(data_dict)
            except (ValueError, SyntaxError) as e:
                logger.warning(f"Error parsing string as literal: {data}. Error: {str(e)}")
        else:
            try:
                data_info_str = str(data)
                data_dict = ast.literal_eval(data_info_str)
                return json.dumps(data_dict)
            except (ValueError, SyntaxError) as e:
                logger.warning(f"Error parsing object as literal: {data}. Error: {str(e)}")
        return ""

    @staticmethod
    def to_dict(data: Union[Dict, str]) -> Dict:
        if not data:
            return {}
        elif isinstance(data, dict):
            return data
        elif isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError as ex:
                print(f"Failed to parse payload as JSON: {ex}")
                raise ValueError('Payload must be a valid JSON string') from ex
        else:
            print(f"Unsupported payload type: {type(data).__name__}")
            raise ValueError('Payload must be a string or dictionary')

    # def to_dict(data):
    #     if not data:  # 如果输入的 payload 为空，则返回空字典
    #         return {}
    #     elif isinstance(data, dict):  # 如果输入的 payload 已经是字典，则直接返回它
    #         return data
    #     elif isinstance(data, str):  # 如果输入的 payload 是字符串，则将其解析为字典
    #         return json.loads(data)
    #     else:  # 如果输入的 payload 是其他类型，则无法进行转换，抛出异常
    #         print("wrong type!!!")
    #         raise ValueError('Payload must be a string or dictionary')


if __name__ == '__main__':
    print("*" * 20)
