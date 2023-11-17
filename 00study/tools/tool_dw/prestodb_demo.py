import logging

import prestodb


# https://github.com/prestodb/presto-python-client
# pip install presto-python-client
# - 使用redash查询大表时尽量加上limit，避免把redash打挂。使用presto直连时，本地代码如果使用流式处理可以不设置limit。
# - 数据表里一般有imp_day字段，表示数据时间（或者数据入数仓时间）。这个字段数仓会用作分区键，尽量设置这个值减少数仓扫描的压力。特别是数据量大的表，如果不设置可能无法完成检索。


def connect():
    conn = prestodb.dbapi.connect(
        host="127.0.0.1",  # host位置
        port=9000,  # 端口位置
        user="hadoop01",  # 用户名
        catalog="hive",  # 使用的hive
        schema="default",  # 使用的schema，默认是default，可以不改
        http_scheme="http",  # 后面的暂时不添加，http的添加后报错
        request_timeout=10,  # default 30s
        max_attempts=2,  # default 3
        # auth=prestodb.auth.BasicAuthentication("", "")
    )
    # conn._http_session.verify = "./presto.pem"  # 校验文件存储位置，这个应该是默认位置
    return conn


def query(sql: str) -> prestodb.dbapi.Cursor:
    # presto不用关闭，这里直接把cursor返回
    logging.info("开始查询presto, sql: %s", sql)
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    return cur


if __name__ == "__main__":
    sql = """
select
  *
from
  orders
where
  datekey = 20230908
limit
  1
    """
    cur = query(sql)
    for row in cur.genall():
        # 处理row里的数据
        print(row)
