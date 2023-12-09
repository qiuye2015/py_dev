# pip3 install PyMySQL
# pip3 install DBUtils
import threading

from dbutils.pooled_db import PooledDB
import pymysql


class SqlHelper():
    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=10,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host='127.0.0.1',
            port=33065,
            user='root',
            password='123456',
            database='mydb',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.local = threading.local()

    def open(self):
        conn = self.pool.connection()
        cursor = conn.cursor()
        return conn, cursor

    def close(self, conn, cursor):
        cursor.close()
        conn.close()

    def __enter__(self):
        conn, cursor = self.open()
        rv = getattr(self.local, 'stack', None)
        if not rv:
            self.local.stack = [(conn, cursor)]
        else:
            rv.append((conn, cursor))
            self.local.stack = rv
        return cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        rv = getattr(self.local, 'stack', None)
        if not rv:
            # del self.local.stack
            return
        conn, cursor = self.local.stack.pop()
        cursor.close()
        conn.close()

    def fetchone(self, sql, *args):
        conn, cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        self.close(conn, cursor)
        return result

    def fetchall(self, sql, *args):
        conn, cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        self.close(conn, cursor)
        return result


db = SqlHelper()

if __name__ == '__main__':
    r = db.fetchall("select * from orders")
    print(r)
    r = db.fetchone("select * from orders where order_id=%s", 10001)
    print(r)

    with db as c1:
        c1.execute("select 1")
        with db as c2:
            c2.execute('select 2')
    print(123)
