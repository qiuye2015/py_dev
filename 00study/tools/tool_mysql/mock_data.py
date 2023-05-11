#!/usr/bin/env python

import random
import mysql.connector
from faker import Faker

# https://faker.readthedocs.io/en/master/providers.html
Faker.seed(33422)
fake = Faker()

db_host = 'localhost'
db_name = 'fjp_example'
db_user = 'fjp'
db_pass = 'fjp'
conn = mysql.connector.connect(
    host=db_host, database=db_name, user=db_user, password=db_pass
)
cursor = conn.cursor()

row = [fake.first_name(), random.randint(0, 99), fake.date_of_birth()]

cursor.execute(
    ' INSERT INTO `person_test` (name, age, birth_day) VALUES ("%s", %d, "%s");'
    % (row[0], row[1], row[2])
)
print(row)
conn.commit()
