# -*- coding: UTF-8 -*-

import xlrd
import requests
from requests import ReadTimeout, HTTPError, RequestException


def get_one_page(url):
    """
    解析url返回得到的页面信息
    """
    try:
        response = requests.get(url)
        # exit() if not response.status_code == 200 else print('Success')
        if response.status_code != 200:
            print('status_code error %d' % response.status_code)
        else:
            return (response.content)
    except ReadTimeout:
        print('Timeout')
    except HTTPError:
        print('HTTPError')
    except RequestException:
     print('Request Error')


def read_excel():
    workbook = xlrd.open_workbook('test.xlsx')
    sheet = workbook.sheets()[0]
    nrows = sheet.nrows

    result_list = []
    for i in range(4, 5):
        name = sheet.cell(i, 0).value
        url = sheet.cell(i, 3).value
        result_list.append({"name":name, "url":url})

    return result_list


if __name__ == '__main__':
    res = read_excel()
    for i in range(len(res)):
        print res[i]["url"]
        url = res[i]["url"]
        content = get_one_page(url)
        print content
