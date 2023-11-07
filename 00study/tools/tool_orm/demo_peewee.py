from peewee import *

db = SqliteDatabase('peoplev2.db')


# # Connect to a MySQL database on network.
# mysql_db = MySQLDatabase('my_app', user='app', password='db_password', host='10.1.0.8', port=3306)
# mysql_db_pool = PooledMySQLDatabase('my_app', user='app', password='db_password', host='10.1.0.8', port=3306)


class Person(Model):
    name = CharField(null=False)
    birthday = DateField()

    class Meta:  # Peewee将自动从类的名称推断数据库表名。您可以通过指定 table_name 内部“meta”类中的属性
        database = db  # This model uses the "people.db" database.


class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db


if __name__ == '__main__':
    # 尽管不需要显式打开连接
    r = db.connect()
    print(r)
    db.create_tables([Person, Pet])
    from datetime import date

    uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
    r = uncle_bob.save()  # bob is now stored in the database
    # # Returns: 1
    # print(r)
    # grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
    # herb = Person.create(name='Herb', birthday=date(1950, 5, 5))
    # grandma.name = 'Grandma L.'
    # grandma.save()  # Update grandma's name in the database.

    bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
    query = Pet.select()
    sql, param = query.sql()
    print("fjp--->", sql.replace("?", "{}").format(*param))
    db.close()
