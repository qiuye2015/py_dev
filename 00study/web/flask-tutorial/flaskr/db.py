import sqlite3

import click
from flask import current_app, g


# g是一个特殊对象，对于每个请求都是唯一的。它用于存储在请求期间可能被多个函数访问的数据。
# get_db如果在同一请求中第二次调用该连接，则该连接将被存储和重用，而不是创建新连接

# current_app是另一个特殊对象，它指向处理请求的 Flask 应用程序。
# 由于您使用了应用程序工厂，因此在编写其余代码时没有应用程序对象。
# get_db将在应用程序创建并正在处理请求时调用，因此current_app可以使用
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# open_resource()打开一个相对于flaskr包的文件，
# 这很有用，因为您以后部署应用程序时不一定知道该位置在哪里。
# get_db 返回一个数据库连接，用于执行从文件中读取的命令。
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# click.command()定义一个命令行命令init-db ，
# 调用该init_db函数并向用户显示成功消息。
# 运行init-db命令：现在项目的文件夹中将有一个flaskr.sqlite文件
#           flask --app flaskr init-db
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


# 注册应用程序
def init_app(app):
    # 告诉 Flask 在返回响应后进行清理时调用该函数
    app.teardown_appcontext(close_db)
    # 添加一个可以使用命令调用的新flask命令
    app.cli.add_command(init_db_command)
