# 测试文件名约定 test_xxx
# class 名字 Test 打头
# 类继承 unittest.TestCase
# 每个单测方法命名 test_xxx
# 每个测试的关键是：调用 assertEqual() 来检查预期的输出；
# 调用 assertTrue() 或 assertFalse() 来验证一个条件；
# 调用 assertRaises() 来验证抛出了一个特定的异常。
# 使用这些方法而不是 assert 语句是为了让测试运行者能聚合所有的测试结果并产生结果报告。
# 注意这些方法是 unitest 模块的方法，需要使用 self 调用
import unittest


# 定义单元测试类，需要继承 unittest.TestCase 类；
class TestStringMethods(unittest.TestCase):
    def setUp(self):
        # 单测启动前的准备工作，比如初始化一个mysql连接对象
        # 为了说明函数功能，测试的时候没有CMysql模块注释掉或者换做print学习
        # self.conn = CMysql()
        pass

    def tearDown(self):
        # 单测结束的收尾工作，比如数据库断开连接回收资源
        # self.conn.disconnect()
        pass

    def test_upper(self):
        # 逻辑断言
        self.assertEqual('foo'.upper(), 'FOO')

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # 断言异常
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
