#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from requests.exceptions import ReadTimeout, HTTPError, RequestException
import time
import json
from mysql import DB
from sendEmail import EmailClient

#db = DB()
#sender = 'f1119345739@163.com'
sender = 'qiuye_tju@163.com'
ecli = EmailClient(sender)
content = """
<!DOCTYPE html>
<html>
<head> 
    <meta charset="utf-8"> 
    <title>fjp</title> 
</head>
<body>
    <table border="1" cellspacing="0">
    <tr>
        <td>职位名称</td>
        <td>岗位要求</td>
    </tr>
"""

class Spider:
    def __init__(self, url):
        self.url = url

    def get_page(self):
        try:
            response = requests.get(self.url, timeout=1)
            if not response.status_code == 200:
                print("status_code error")
            else:
                return response.json()
        except ReadTimeout:
            print("timeout")
        except HTTPError:
            print("http error")
        except RequestException:
            print("error")

    def get_page_index(self,method='GET',data=None):
        try:
            if method=='GET':
                response = requests.get(self.url, timeout=1, params=data)
            elif method == 'POST':
                response = requests.post(self.url, data=data)
            if not response.status_code == 200:
                print("status_code error")
            else:
                return response.json()
        except ReadTimeout:
            print("timeout")
        except HTTPError:
            print("http error")
        except RequestException:
            print("error")

    def write_to_file(content):
        with open("result.txt",'a',encoding='utf-8') as f:
            f.write(json.dumps(content,ensure_ascii=False)+"\n")
            f.close


def parse_page(response):
    global content
    returnValue = response['returnValue']
    totalPage = returnValue['totalPage']
    datas_list = returnValue['datas']
    now = time.time()
    for data in datas_list:
        isOpen = data['isOpen']
        isNew = data['isNew']
        effectiveDate = int(data['effectiveDate']/1000)
        uneffectualDate = int(data['uneffectualDate']/1000)
        degree = data['degree']
        workExperience = data['workExperience']
        id = data['id']
        name = data['name']
        departmentName = data['departmentName']
        requirement = data['requirement'].replace('<br/>','\n').lower()
        recruitNumber = data['recruitNumber']
        description = data['description'].replace('<br/>','\n')
        workLocation = data['workLocation']
        shareLinkPcWechat=""
        if 'shareLinkPcWechat' in data:
            shareLinkPcWechat = data['shareLinkPcWechat']
        # (id, name, degree, workLocation, workExperience, 
        # departmentName,effectiveDate, uneffectualDate,requirement, description,recruitNumber)
        if (isOpen == 'Y') and (isNew == 'Y') and (uneffectualDate > now) and (degree != "博士"):
            if workExperience[:1] in "四五六七八九":
                print("filter %s %s" % (id,workExperience))
                continue
            if "c++" not in requirement:
                print("filter %s requirement" % id)
                continue
                 
            if "java方向" in requirement:
                print("filter %s requirement" % id)
                continue

            effectiveDate = time.gmtime(effectiveDate)
            uneffectualDate = time.gmtime(uneffectualDate)
            params = [id,name,degree,workLocation,workExperience,departmentName,\
                      effectiveDate,uneffectualDate,requirement, description,recruitNumber\
                    ]
            name_url = "<a href={}>{}</a>".format(shareLinkPcWechat,name)
            print("add id %s" % id)
            content +="""
            <tr>
                <td>{}</td>
                <td>{}</td>
            </tr>
            """.format(name_url,requirement)

            
            #db.add_item(params)


def doRequestAndParseData(spider,index=1):
    #while True:
    payload = {
        'first': '技术类',
        'location': '北京',
        'pageIndex': index,
        'pageSize': '10'
    }
    content = spider.get_page_index("POST",payload)
    totalPage = parse_page(content)
        #index +=1
        #if index >6: break
        #if index >totalPage: break

    
def main():
    url = 'https://job.alibaba.com/zhaopin/socialPositionList/doList.json'
    spider = Spider(url)
    for i in range(6):
        doRequestAndParseData(spider,i+1)
    #doRequestAndParseData(spider,1)
    global content
 #   db.show_items()
    content +="""
          </table>
          </body>
          </html>
          """

    ecli.send(content, 'html')
    #with open('job.html','w') as f:
    #    f.write(content)


if __name__ == "__main__":
    main()
