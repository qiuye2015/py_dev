"""
sqlite一共有5中数据类型可以定义
NULL	NULL 值
INTEGER 带符号的整数,根据值的大小存储在 1、2、3、4、6 或 8 字节中
REAL    浮点值，存储为 8 字节的 IEEE 浮点数字。
TEXT    字符串，使用数据库编码（UTF-8、UTF-16BE 或 UTF-16LE）存储
BLOB    blob 数据，完全根据它的输入存储
"""


# 创建表
def create_table():
    import sqlite3

    conn = sqlite3.connect('test.db')
    # conn = sqlite3.connect(":memory:")  # 在内存中创建数据
    cursor = conn.cursor()
    table_sql = """
    create table user(
      id INTEGER PRIMARY KEY autoincrement NOT NULL ,
      name text NOT NULL,
      age INTEGER NOT NULL
    )
    """
    cursor.execute(table_sql)
    conn.commit()  # 一定要提交,否则不会执行sql
    conn.close()


# insert数据
def insert_data():
    import sqlite3

    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    sql_lst = [
        "insert into user(name, age)values('lili', 18)",
        "insert into user(name, age)values('poly', 19)",
        "insert into user(name, age)values('lilei', 30)",
    ]
    for sql in sql_lst:
        cursor.execute(sql)
        conn.commit()
    conn.close()


def get_data():
    # import sqlite3
    #
    # conn = sqlite3.connect('test.db')
    # conn.row_factory = sqlite3.Row
    # cursor = conn.cursor()
    #
    # sql = "select * from user"
    # cursor.execute(sql)
    # rows = cursor.fetchall()  # 获取全部数据
    # for row in rows:
    #     print(row.keys(), tuple(row))
    #
    # conn.close()
    import sqlite3

    conn = sqlite3.connect('test.db')

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    conn.row_factory = dict_factory
    cursor = conn.cursor()

    sql = "select * from user"
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取全部数据
    for row in rows:
        print(row)

    conn.close()


def update_data():
    import sqlite3

    conn = sqlite3.connect('test.db')

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    conn.row_factory = dict_factory
    cursor = conn.cursor()

    # 修改数据
    update_sql = "update user set age = 22 where id = 1"
    cursor.execute(update_sql)
    conn.commit()

    sql = "select * from user"
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取全部数据
    for row in rows:
        print(row)

    conn.close()


def delete_data():
    import sqlite3

    conn = sqlite3.connect('test.db')

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    conn.row_factory = dict_factory
    cursor = conn.cursor()

    # 删除数据
    delete_sql = "delete from user where id = 1"
    cursor.execute(delete_sql)
    conn.commit()

    sql = "select * from user"
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取全部数据
    for row in rows:
        print(row)

    conn.close()


def batch_insert_data():
    import sqlite3

    conn = sqlite3.connect('test.db')

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    conn.row_factory = dict_factory
    cursor = conn.cursor()

    # 批量执行
    sql = "insert into user(name, age)values(?, ?)"
    user_lst = [('lili', 18), ('poly', 19), ('lilei', 30)]
    cursor.executemany(sql, user_lst)

    sql = "select * from user"
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取全部数据
    for row in rows:
        print(row)

    conn.close()


if __name__ == '__main__':
    # create_table()
    # insert_data()
    # update_data()
    # delete_data()
    batch_insert_data()
