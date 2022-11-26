import os
import click
from flask_migrate import Migrate

from apps import create_app, db
from apps.models import User, Role, Permission

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


# 避免每次启动 shell 会话都要导入数据库实例和模型
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission)


# app.cli.command 装饰器把自定义命令变得很简单。
# 被装饰的函数名就是命令名，函数的文 档字符串会显示在帮助消息中
@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.run(port=10000, debug=True)
