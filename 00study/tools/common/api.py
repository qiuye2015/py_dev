# !/usr/bin/env python3
from enum import IntEnum
from typing import Optional, Generic, Union, TypeVar
from pydantic.generics import GenericModel


class ApiCode(IntEnum):
    NORMAL = 0

    MOVED_PERMANENTLY = 301

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404

    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502


DataT = TypeVar('DataT')


class ApiResponse(GenericModel, Generic[DataT]):
    code: Union[int, str]
    message: str = None
    data: Optional[DataT]

    def is_success(self):
        return self.code == 0

    @staticmethod
    def new_success(data: Optional[DataT] = None):
        return ApiResponse(code=ApiCode.NORMAL, message='success', data=data)

    @staticmethod
    def new_fail(code, message):
        return ApiResponse(code=code, message=message)


class PageResponse(GenericModel, Generic[DataT]):
    total: int = None
    result: Optional[DataT]
    limit: int = None
    offset: int = None
    cursor: str = None


if __name__ == '__main__':
    Data = {'name': 'John', 'age': 30}
    resp = ApiResponse.new_success(Data)
    print(resp.json())

    # Test new_fail() method
    resp = ApiResponse.new_fail(404, 'Not found')
    print(resp.json())
