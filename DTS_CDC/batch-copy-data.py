import operator

from d22d import CsvD, ElasticSearchD, Migration, MySqlD, open_log

"""
索引没复制过来
pip3 install d22d
github.com:DJMIN/D2D.git
"""


def test1():
    """
    Migration 可以全量迁移单表数据，不指定表名可以全量迁移整个数据库

    mysql es等均用流式游标读取的方式，避免程序迁移过程中占用过多内存，导致内存爆炸
    将mysql://localhost:3306/test的user表全量迁移到mysql://localhost:3306/test的user表，若mysql://localhost:3306/test没有user表，会自动建立数据表。
    """
    open_log()
    t = Migration(
        # database_from=MySqlD(host='localhost', port=33065, database='mydb', user='root', passwd='123456'),  # 数据来源数据库
        # database_to=MySqlD(host='localhost', port=33065, database='mydb-fork', user='root', passwd='123456'),  # 数据去向数据库
        database_from=MySqlD(host='localhost', port=33065, database='adw_mock', user='root', passwd='123456'),  # 数据来源数据库
        database_to=MySqlD(host='localhost', port=33065, database='mydb', user='root', passwd='123456'),  # 数据去向数据库
        table_from='table_38',  # 数据来源数据库表名
        table_to='big_tb_keydata',  # 数据去向数据库表名
    )
    t.run()


def test2():
    """
    同上test1 Migration 可以全量迁移单表数据，不指定表名可以全量迁移整个数据库

    将mysql://localhost:33065/mydb的user1表全量迁移到es数据库的user1 index，若es没有user1 index，会自动建立index。
    """
    t = Migration(
        database_from=MySqlD(host='localhost', port=33065, database='mydb', user='root', passwd='123456'),
        database_to=ElasticSearchD(hosts='127.0.0.1:9200'),
        table_from='orders',
        table_to='test_orders_d22d_index',
    )
    t.run()
    """
    ElasticSearchD.create_index()
                elif isinstance(value,decimal.Decimal):
                    properties[name]['type'] = 'double'
    """


def test3():
    """
    同上test1 Migration 可以全量迁移单表数据，不指定表名可以全量迁移整个数据库

    将mysql://localhost:33065/test的user1表全量保存到本地csv文件./data/user1。
    """
    t = Migration(
        database_from=MySqlD(host='localhost', port=33065, database='mydb', user='root', passwd='123456'),
        database_to=CsvD(path='./data'),
        table_from='orders',
        table_to='user1',
    )
    t.run()


if __name__ == '__main__':
    # test1()
    a = {'a': 1, 'b': 2}
    b = {'a': 1, 'b': 2}
    c = {'a': 1, 'b': 3}
    e = {"e": a}
    f = {"e": b}
    print(a == b)  # True
    print(a == c)  # False
    print(e == f)
    print(operator.eq(a, b))  # True
    print(operator.eq(a, c))  # False
