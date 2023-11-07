import os
import sqlite3
import mysql.connector

mysql_host = "82.156.150.79"
mysql_port = 13306
mysql_user = "leo"
mysql_pwd = "dlmutju"
mysql_database = "BJ"

workdir = os.path.dirname(os.path.realpath(__file__))
dbpath = f"{workdir}/house_trade_stat.db"

# 连接到SQLite数据库
sqlite_conn = sqlite3.connect(dbpath)
sqlite_cursor = sqlite_conn.cursor()

# 连接到MySQL数据库
mysql_conn = mysql.connector.connect(
    host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_pwd, database=mysql_database
)
mysql_cursor = mysql_conn.cursor()
# 创建MySQL表（如果不存在）
mysql_cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS bj_zjw_house_trade_stat (
        row_uuid VARCHAR(255),
        title TEXT,
        trade_date VARCHAR(255),
        online_sign_count INT,
        online_sign_area FLOAT,
        house_sign_count INT,
        house_sign_area FLOAT,
        createdatetime FLOAT
    )
'''
)

# 查询MySQL中的所有row_uuid
mysql_cursor.execute('SELECT row_uuid FROM bj_zjw_house_trade_stat')
existing_row_uuids = set(row[0] for row in mysql_cursor.fetchall())

# 查询SQLite中的所有数据
sqlite_cursor.execute('SELECT * FROM bj_zjw_house_trade_stat')
for row in sqlite_cursor.fetchall():
    (
        row_uuid,
        title,
        trade_date,
        online_sign_count,
        online_sign_area,
        house_sign_count,
        house_sign_area,
        createdatetime,
    ) = row

    if row_uuid in existing_row_uuids:
        # 如果row_uuid已存在于MySQL中，则执行更新操作
        mysql_cursor.execute(
            '''
            UPDATE bj_zjw_house_trade_stat 
            SET title = %s, trade_date = %s, online_sign_count = %s, 
                online_sign_area = %s, house_sign_count = %s, 
                house_sign_area = %s, createdatetime = %s 
            WHERE row_uuid = %s
        ''',
            (
                title,
                trade_date,
                online_sign_count,
                online_sign_area,
                house_sign_count,
                house_sign_area,
                createdatetime,
                row_uuid,
            ),
        )
        print(f"==>update {row}")
    else:
        # 如果row_uuid不存在于MySQL中，则执行插入操作
        mysql_cursor.execute(
            '''
            INSERT INTO bj_zjw_house_trade_stat 
            (row_uuid, title, trade_date, online_sign_count, online_sign_area, 
             house_sign_count, house_sign_area, createdatetime) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''',
            (
                row_uuid,
                title,
                trade_date,
                online_sign_count,
                online_sign_area,
                house_sign_count,
                house_sign_area,
                createdatetime,
            ),
        )
        print(f"==>insert {row}")

# 提交更改
mysql_conn.commit()

# 关闭连接
sqlite_conn.close()
mysql_conn.close()
