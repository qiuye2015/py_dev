import unittest
from flask import current_app
from app import create_app, db


# 测试用例类的 setUp() 和 tearDown() 方法分别在各测试之前和之后运行。
# 名称以 test_ 开头的方法都作为测试运
class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        # 创建应用
        self.app = create_app('testing')
        # 激活上下,确保能在测试中使用 current_app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
