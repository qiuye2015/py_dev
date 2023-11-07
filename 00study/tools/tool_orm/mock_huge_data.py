import random
import string

import pymysql

# 尝试连接数据库
try:
    host = '127.0.0.1'
    port = 33065
    password = '123456'
    user = 'root'
    database = 'adw_mock'

    # host = '82.156.150.7'
    # port = 13306
    # user = 'root'
    # password = 'dlmutju'
    # database = 'adw_mock'

    # conn = pymysql.connect(
    #     host='82.156.150.7',
    #     port=13306,
    #     user='root',
    #     password='dlmutju',
    #     database='adw_mock',
    #     connect_timeout=1000,
    #     read_timeout=1000,
    #     write_timeout=1000,
    # )

    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        connect_timeout=1000,
        read_timeout=1000,
        write_timeout=1000,
    )
    print("成功连接到数据库")
except Exception as e:
    print(f"连接数据库失败: {e}")
    exit()

# 创建游标
cursor = conn.cursor()


# 生成随机字符串
def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


# 生成随机整数
def random_int():
    return random.randint(1, 10000)


# 生成随机大整数
def random_bigint():
    return random.randint(1, 1000000000)


# 生成随机时间戳
def random_timestamp():
    return random.randint(1000000000, 2000000000)


# 判断表是否存在，如果不存在则创建表
table_name = 'table_38'
create_table_query = """
-- adw.table_38 definition

CREATE TABLE IF NOT EXISTS `table_38`  (
  `id` bigint(20) NOT NULL DEFAULT '0' COMMENT 'id',
  `partition_id` bigint(20) NOT NULL DEFAULT '0' COMMENT 'parition id',
  `rowkey` varchar(100) NOT NULL DEFAULT '' COMMENT 'rowkey',
  `sys_data_name` varchar(500) NOT NULL DEFAULT '' COMMENT 'data name',
  `sys_data_id` bigint(20) NOT NULL DEFAULT '0' COMMENT 'data id',
  `sys_data_size` bigint(20) NOT NULL DEFAULT '0' COMMENT 'data size bytes',
  `sys_create_time` int(11) NOT NULL DEFAULT '0' COMMENT 'create time',
  `sys_update_time` int(11) NOT NULL DEFAULT '0' COMMENT 'update time',
  `sys_update_user` varchar(50) NOT NULL DEFAULT '' COMMENT 'update user',
  `sys_original_ip` varchar(50) NOT NULL DEFAULT '' COMMENT 'original ip',
  `sys_original_type` varchar(50) NOT NULL DEFAULT '' COMMENT 'original type',
  `sys_original_path` varchar(500) NOT NULL DEFAULT '' COMMENT 'original path',
  `meta_task_id` varchar(200) NOT NULL DEFAULT '' COMMENT 'meta.task_id',
  `meta_date` int(11) NOT NULL DEFAULT '0' COMMENT 'meta.date',
  `meta_car_id` varchar(100) NOT NULL DEFAULT '' COMMENT 'meta.car_id',
  `meta_nt_version` varchar(100) NOT NULL DEFAULT '' COMMENT 'meta.nt_version',
  `meta_model_type` varchar(100) NOT NULL DEFAULT '' COMMENT 'meta.model_type',
  `meta_region` varchar(100) NOT NULL DEFAULT '' COMMENT 'meta.region',
  `meta_start_time` bigint(20) NOT NULL DEFAULT '0' COMMENT 'meta.start_time',
  `meta_end_time` bigint(20) NOT NULL DEFAULT '0' COMMENT 'meta.end_time',
  `meta_frames` int(11) NOT NULL DEFAULT '0' COMMENT 'meta.frames',
  `meta_duration` int(11) NOT NULL DEFAULT '0' COMMENT 'meta.duration',
  `meta_data_size` bigint(20) NOT NULL DEFAULT '0' COMMENT 'meta.data_size',
  `meta_file_type` varchar(100) NOT NULL DEFAULT '' COMMENT 'meta.file_type',
  `meta_file_name` varchar(200) NOT NULL DEFAULT '' COMMENT 'meta.file_name',
  `meta_file_path` varchar(500) NOT NULL DEFAULT '' COMMENT 'meta.file_path',
  `meta_topic` varchar(100) NOT NULL DEFAULT '' COMMENT 'meta.topic',
  `meta_etag` varchar(100) NOT NULL DEFAULT '' COMMENT 'meta.etag',
  `data_data_type` int(11) NOT NULL DEFAULT '0' COMMENT 'data type: 0-none, 1-extern',
  `data_data_value` varchar(500) NOT NULL DEFAULT '' COMMENT 'data value',
  `data_storage_type` varchar(50) NOT NULL DEFAULT '' COMMENT 'storage type, S3,COS,HDFS...',
  `data_endpoint` varchar(100) NOT NULL DEFAULT '' COMMENT 'endpoint, address',
  `data_bucket` varchar(100) NOT NULL DEFAULT '' COMMENT 'bucket',
  `data_ak` varchar(100) NOT NULL DEFAULT '' COMMENT 'access key id',
  `data_sk` varchar(100) NOT NULL DEFAULT '' COMMENT 'secret key',
  PRIMARY KEY (`rowkey`),
  KEY `meta_task_id` (`meta_task_id`),
  KEY `meta_date` (`meta_date`),
  KEY `meta_start_time` (`meta_start_time`),
  KEY `meta_end_time` (`meta_end_time`),
  KEY `meta_car_id` (`meta_car_id`),
  KEY `idx_carid_date` (`meta_car_id`,`meta_date`),
  KEY `idx_0` (`meta_topic`,`meta_car_id`,`meta_start_time`),
  KEY `idx_sys_update_time` (`sys_update_time`),
  KEY `idx_task_filename` (`meta_task_id`,`meta_file_name`),
  KEY `idx_task_topic` (`meta_task_id`,`meta_topic`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='roadtest/datafiles';
"""
cursor.execute(create_table_query)

# 插入10万条测试数据
for i in range(1000000):
    rowkey = random_string(10)
    sys_create_time = random_timestamp()
    sys_update_time = random_timestamp()
    sys_update_user = random_string(8)
    sys_original_ip = (
        f'{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'
    )
    sys_original_type = random_string(8)
    sys_original_path = random_string(50)
    meta_task_id = random_string(20)
    meta_date = random_int()
    meta_car_id = random_string(10)
    meta_nt_version = random_string(10)
    meta_model_type = random_string(10)
    meta_region = random_string(10)
    meta_start_time = random_bigint()
    meta_end_time = random_bigint()
    meta_frames = random_int()
    meta_duration = random_int()
    meta_data_size = random_bigint()
    meta_file_type = random_string(10)
    meta_file_name = random_string(30)
    meta_file_path = random_string(50)
    meta_topic = random_string(10)
    meta_etag = random_string(10)
    data_data_type = random_int()
    data_data_value = random_string(50)
    data_storage_type = random_string(5)
    data_endpoint = random_string(15)
    data_bucket = random_string(10)
    data_ak = random_string(10)
    data_sk = random_string(10)

    insert_query = f"INSERT INTO table_38 (rowkey, sys_create_time, sys_update_time, sys_update_user, sys_original_ip, sys_original_type, sys_original_path, meta_task_id, meta_date, meta_car_id, meta_nt_version, meta_model_type, meta_region, meta_start_time, meta_end_time, meta_frames, meta_duration, meta_data_size, meta_file_type, meta_file_name, meta_file_path, meta_topic, meta_etag, data_data_type, data_data_value, data_storage_type, data_endpoint, data_bucket, data_ak, data_sk) VALUES ('{rowkey}', {sys_create_time}, {sys_update_time}, '{sys_update_user}', '{sys_original_ip}', '{sys_original_type}', '{sys_original_path}', '{meta_task_id}', {meta_date}, '{meta_car_id}', '{meta_nt_version}', '{meta_model_type}', '{meta_region}', {meta_start_time}, {meta_end_time}, {meta_frames}, {meta_duration}, {meta_data_size}, '{meta_file_type}', '{meta_file_name}', '{meta_file_path}', '{meta_topic}', '{meta_etag}', {data_data_type}, '{data_data_value}', '{data_storage_type}', '{data_endpoint}', '{data_bucket}', '{data_ak}', '{data_sk}')"
    cursor.execute(insert_query)
    # 每一千行打印一条日志
    if (i + 1) % 1000 == 0:
        conn.commit()
        print(f"已插入 {i + 1} 行数据")

# 提交并关闭连接
conn.commit()
cursor.close()
conn.close()
