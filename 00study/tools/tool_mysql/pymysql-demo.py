import os
from typing import Text

from loguru import logger
import pymysql
import yaml

# https://mp.weixin.qq.com/s/0hAX9-oxSf6HM44HpSyFpw
class MysqlClient:
    """
    Mysql类型数据库 封装工具 数据库连接信息读取配置文件
    """

    def __init__(self, host: Text, port: int, user: Text, password: Text, db_name: Text):
        """
        初始化数据库连接
        :param host:
        :param port:
        :param user:
        :param password:
        :param db_name:
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name

        self.conn = None
        self.cursor = None

    @staticmethod
    def handle_error(error, message):
        """
        处理报错信息输出
        :param error:
        :param message:
        :return:
        """
        logger.error(f"{message}: {error}")

    def connect(self):
        """
        建立数据库连接
        :return:
        """
        try:
            """创建链接"""
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db_name,
                charset='utf8',
            )

            """创建游标，默认是元组型游标，我们设置为字典型游标"""
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            self.handle_error(e, '数据库连接失败')
            raise e

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        if self.cursor:
            try:
                self.cursor.close()
            except Exception as e:
                self.handle_error(e, '关闭数据库cursor失败 ')

        if self.conn:
            try:
                self.conn.close()
            except Exception as e:
                self.handle_error(e, '关闭数据库connection失败 ')

    def execute_query(self, sql):
        """
        执行查询语句
        :param sql:
        :return:
        """
        try:
            self.connect()
            if self.cursor is not None:
                self.cursor.execute(sql)
                results = self.cursor.fetchall()
                return results
        except Exception as e:
            self.handle_error(e, '执行查询SQL失败 ')
        finally:
            self.close()

    def execute_update(self, sql):
        """
        执行更新语句
        :param sql:
        :return:
        """
        try:
            self.connect()
            if self.cursor is not None:
                self.cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            if self.conn is not None:
                self.conn.rollback()
            self.handle_error(e, '执行更新SQL失败 ')
        finally:
            self.close()


class DbTools:
    """
    Mysql 数据库操作工具
    """

    def __init__(self):
        self.db_connection_info = self.get_db_connection_info()

        self.host = self.db_connection_info['host']
        self.port = self.db_connection_info['port']
        self.user = self.db_connection_info['user']
        self.password = self.db_connection_info['password']
        self.db_name = self.db_connection_info['db_name']

        self.db_client = self.get_db_client()

    @staticmethod
    def get_db_connection_info():
        config_path = './config/mysql_connect_info.yaml'

        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                data_base_config = yaml.load(f.read(), Loader=yaml.SafeLoader)
        return data_base_config['mysql_ecoa']

    def get_db_client(self):
        return MysqlClient(host=self.host, port=self.port, user=self.user, password=self.password, db_name=self.db_name)

    def close_client(self):
        self.db_client.close()


def main():
    db_tool = DbTools().db_client

    select_sql = "SELECT * FROM `user` WHERE username IS NOT NULL;"
    table_results = db_tool.execute_query(select_sql)

    print("返回结果长度：{}".format(len(table_results)))

    for row in table_results:
        print(row["username"])


if __name__ == '__main__':
    """读取配置文件中数据信息"""
    config_path = './config/mysql_connect_info.yaml'

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            data_base_config = yaml.load(f.read(), Loader=yaml.SafeLoader)
    db_connection_info = data_base_config['mysql_ecoa']

    host = db_connection_info['host']
    port = db_connection_info['port']
    user = db_connection_info['user']
    password = db_connection_info['password']

    db_name = "main"

    mysql_client = MysqlClient(host=host, port=int(port), user=user, password=password, db_name=db_name)

    select_sql = "SELECT * FROM `user` WHERE username IS NOT NULL;"
    table_results = mysql_client.execute_query(select_sql)

    print("返回结果长度：{}".format(len(table_results)))

    for row in table_results:
        print(row["username"])
