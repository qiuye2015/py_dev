#!/usr/bin/env python
# coding=utf-8

import sys
reload(sys);
sys.setdefaultencoding("utf8")
import xlrd


def read_excel(fileName,sheet=0,startRow=1,endRow=0,startCol=0,endCol=2):
    print("read_excel...")
    workbook = xlrd.open_workbook(fileName)
    sheet = workbook.sheets()[sheet]
    if endRow == 0:
        endRow = sheet.nrows

    for i in range(startRow, endRow):
        line = ""
        for j in range(startCol,endCol):
            name = sheet.cell(i, j).value
        #    print(name)
            if len(line) != 0:
                line +="\t"
            line += str(name)
        print line


if __name__ == '__main__':
    if len(sys.argv) > 1:
        read_excel(sys.argv[1])
