import logging
import time
from pyhive import hive
from common.config import *


class Pyhive:
    def __init__(self):
        self.conn = None
        self.cursor = None
    # 链接mysql数据库
    def connect(self, host=HIVE_HOST,port=HIVE_PORT,database=HIVE_DATABASE,charset="utf8"):
        try:
            self.conn = hive.Connection(host=host, port=port, database=database,username='root', auth='NOSASL')
            self.cursor = self.conn.cursor()
            logging.info('connect hive success')
        except Exception as e:
            logging.error('connect hive database %s error! %s' % (database, e))
            return False
        return True


    # 指定sql命令查询
    def query(self, sqlcommand):
        try:
            self.cursor.execute(sqlcommand)
            result = self.cursor.fetchall()
        except Exception as e:
            logging.error("hive query error: %s\n hive command is: %s" %(e, sqlcommand))
            return False,str(e)
        return True,result

    # 指定sql命令执行
    def execute(self, sqlcommand):
        try:
            line = self.cursor.execute(sqlcommand)
        except Exception as e:
            # traceback.print_exc()
            logging.error("hive sql execute error: %s"% e)
            return False,str(e)
        return True,line


    # 关闭链接
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # logging.info('close mysql success')

    # 插入数据
    def insert_data(self, table_name, data_dict):
        data_values = "(" + "%s," * (len(data_dict)) + ")"
        data_values = data_values.replace(',)', ')')
        db_field = data_dict.keys()
        data_tuple = tuple(data_dict.values())
        db_field = str(tuple(db_field)).replace("'", '')
        sql = """ insert into %s %s values %s """ % (table_name, db_field, data_values)
        params = data_tuple

        self.execute(sql, params)
        self.commit()
        #self.close()

    # 创建或修改数据
    def insert_update_data(self,table_name, data_dict,major_key):
        data_values = "(" + "%s," * (len(data_dict)) + ")"
        data_values = data_values.replace(',)', ')')
        db_field = data_dict.keys()
        data_tuple = tuple(data_dict.values())
        db_field = str(tuple(db_field)).replace("'", '')
        sql = 'select '+major_key+' from '+table_name+' where '+major_key+'=%s'
        major_value = data_dict[major_key]
        exist_data = () # self.query(sql,*(major_value,))
        print(sql,major_value,exist_data)

        if not exist_data:
            sql = "insert into %s %s values %s " % (table_name, db_field, data_values)
            params = data_tuple
            # print(sql,params)
            self.execute(sql, params)
            self.commit()
        else:
            sql = "update %s set " % table_name
            params=[]
            for key in data_dict:
                if key!=major_key:
                    if type(data_dict[key])==int:
                        sql+=key+"="+str(data_dict[key])+","
                    elif type(data_dict[key])==str:
                        sql += key + "='" + data_dict[key] + "',"
                    elif type(data_dict[key])==bytes:
                        sql += key + "=%s,"
                        params.append(data_dict[key])
            sql=sql[0:-1]
            sql+=" where "+major_key+"=%s"
            params.append(data_dict[major_key])
            # print(sql,params)
            self.execute(sql, params)
            self.commit()


# docker run -p 3306:3306 --name mysql_docker -v $PWD/conf:/etc/mysql/conf.d -v $PWD/logs:/logs -v $PWD/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.6   运行
#
# mysql -u root -p
# CREATE DATABASE IF NOT EXISTS $PROJECT default charset utf8 COLLATE utf8_general_ci;

def test():
    py_sql = Pyhive()
    py_sql.connect('127.0.0.1', 'root', '123456', 'note', 3306)
    sql = 'drop table if exists user'
    py_sql.cursor.execute(sql)
    py_sql.conn.commit()

    sql = 'drop table if exists product'
    py_sql.cursor.execute(sql)
    py_sql.conn.commit()

    sql = 'drop table if exists user_product'
    py_sql.cursor.execute(sql)
    py_sql.conn.commit()

    create_table = 'create table user(id INTEGER PRIMARY KEY AUTO_INCREMENT ,username varchar(64) not null,password varchar(64) not null, phone varchar(64));'
    py_sql.cursor.execute(create_table)
    py_sql.conn.commit()

    create_table = 'create table product(id INTEGER PRIMARY KEY AUTO_INCREMENT ,type varchar(64) not null,time varchar(64) not null, userid INTEGER,' \
                   'field varchar(64) not null,title varchar(200),content varchar(500),answer varchar(200));'
    py_sql.cursor.execute(create_table)
    py_sql.conn.commit()

    create_table = 'create table user_product(id INTEGER PRIMARY KEY AUTO_INCREMENT ,userid INTEGER not null,productid INTEGER not null, type varchar(64) not null);'
    py_sql.cursor.execute(create_table)
    py_sql.conn.commit()


if __name__ == "__main__":
    pass
    # py_sql = Pyhive()
    # py_sql.connect('47.107.26.202', 'root', 'admin', 'yinli', 3306)
    # for i in range(30,60):
    #     timestamp = int(time.mktime(time.strptime('2019-02-26 19:%d:00'%i,'%Y-%m-%d %H:%M:%S')))
    #     sql='select count(*) from capture where create_time>%s and create_time<%s'%(timestamp,timestamp+60)
    #     result = py_sql.query(sql)
    #     print(i+1,result)









