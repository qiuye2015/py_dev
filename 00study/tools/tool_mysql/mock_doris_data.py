from faker import Faker
import mysql.connector
import random

# 创建 Faker 对象
fake = Faker()

# 建立数据库连接
conn = mysql.connector.connect(host='localhost', port=13306, user='root', password='123456', database='test')

# 创建游标
cursor = conn.cursor()

# # 删除旧数据库
# drop_database_query = "DROP DATABASE IF EXISTS test"
# cursor.execute(drop_database_query)
#
# # 创建新数据库
# create_database_query = "CREATE DATABASE test"
# cursor.execute(create_database_query)

# # 切换到新数据库
# use_database_query = "USE test"
# cursor.execute(use_database_query)

# 删除表
drop_table_query = "DROP TABLE IF EXISTS test.doris"
cursor.execute(drop_table_query)

# 创建表
create_table_query = """
    CREATE TABLE `doris` (
      `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
      `rule_name` varchar(1024) DEFAULT NULL,
      `rule_version` varchar(1024) DEFAULT NULL,
      `artifact_apply_id` varchar(1024) NOT NULL,
      `stage` varchar(100) NOT NULL,
      `metric_name` varchar(100) DEFAULT NULL,
      `metric_cal_time` bigint(20) DEFAULT NULL,
      `value` double DEFAULT NULL,
      `end_status` tinyint(11) DEFAULT NULL,
      `device_type` varchar(100) DEFAULT NULL,
      `artifact_id` varchar(1024) DEFAULT NULL,
      `imp_day` bigint(20) DEFAULT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8
"""
cursor.execute(create_table_query)

# 生成并插入数据
for _ in range(10):
    # 生成假数据
    rule_name = fake.text(max_nb_chars=50)[:50].replace(" ", "_")
    rule_version = f"rules_cn_0_v{random.randint(100, 999)}.{random.randint(0, 99)}"
    artifact_apply_id = fake.uuid4()
    stage = random.choice(['trial_op', 'formal_op'])
    metric_name = random.choice(['push_success_ratio', 'data_return_volume', 'cdm_coredump_cnt'])
    metric_cal_time = fake.random_int(min=1686246893916, max=1694246893916)
    imp_day = int(fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y%m%d%H'))
    if metric_name in ['data_return_volume', 'cdm_coredump_cnt']:
        value = random.randint(0, 100)
    else:
        value = random.uniform(0, 1)
    end_status = random.choice([0, 1, 2])

    device_type = random.choice(['vehicle', 'station'])
    artifact_id = fake.uuid4()

    # 构造插入语句
    insert_query = """
        INSERT INTO test.doris
        (rule_name, rule_version, artifact_apply_id, stage, metric_name,
        metric_cal_time, value, end_status, device_type, artifact_id,imp_day)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # 执行插入语句
    values = (
        rule_name,
        rule_version,
        artifact_apply_id,
        stage,
        metric_name,
        metric_cal_time,
        value,
        end_status,
        device_type,
        artifact_id,
        imp_day,
    )
    cursor.execute(insert_query, values)

# 提交事务
conn.commit()

# 关闭游标和连接
cursor.close()
conn.close()
