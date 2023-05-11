# from peewee import *
from peewee import Model, CharField, IntegerField, MySQLDatabase

# 连接MySQL数据库
db = MySQLDatabase(
    'fjp_example', host='localhost', port=3306, user='fjp', password='fjp'
)


# 定义模型类
class Person(Model):
    name = CharField()
    age = IntegerField()

    class Meta:
        database = db


# 创建数据表
db.create_tables([Person])

# 插入数据
Person.create(name='Alice', age=25)

# 查询数据
query = Person.select().where(Person.name == 'Alice')
for person in query:
    print(person.name, person.age)
