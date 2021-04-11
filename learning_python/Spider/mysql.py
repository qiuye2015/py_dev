# -*- coding: UTF-8 -*-

from pymysql import connect


class DB(object):
    def __init__(self):
        # Connect to the database
        try:
            self.conn = connect(host='localhost', port = 3306, user='root', password='123456', db='findjobs', charset='utf8')
            self.cursor = self.conn.cursor()
        except:
            print("connect database failed !")
            exit(-1)
        
    def __del__(self):
        self.cursor.close()
        self.conn.close()
    
    def execute_sql(self, sql,params=[]):
        self.cursor.execute(sql,params)
        for temp in self.cursor.fetchall():
            print(temp)

    def show_items(self):
        sql = "select * from alibaba"
        self.execute_sql(sql)

    def add_item(self,params):
        try:
            sql = "insert into `alibaba` \
                   (`id`, `name`, `degree`,`workLocation`, \
                    `workExperience`, `departmentName`, \
                    `effectiveDate`, `uneffectualDate`, \
                    `requirement`,`description`, `recruitNumber`)\
                   values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            
            #sql = "INSERT INTO `alibaba` (`id`, `name`) VALUES (%s, %s)"
            self.cursor.execute(sql,params)
            # 与查找不同的地方
            self.conn.commit()
        except:
            print("add_item error, to rollback")
            # 发生错误时回滚
            self.conn.rollback()

def main():
    db = DB()
    id =1 
    name = 'hahah'
    degree = '硕士'
    workLocation = '北京'
    workExperience = '五年以上'
    departmentName = None
    effectiveDate = None
    uneffectualDate = None
    description = None
    recruitNumber = None
    requirement = None
    db.add_item((id,name,degree,workLocation,workExperience,\
            departmentName,effectiveDate,requirement,uneffectualDate,description,recruitNumber\
            ))
    db.show_items()

if __name__ == '__main__':
    main()
