from pyflink.table import EnvironmentSettings, TableEnvironment

# 1. 创建 TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

# 2. 创建 source 表
table_env.execute_sql("""
    CREATE TABLE datagen (
        id INT,
        data STRING
    ) WITH (
        'connector' = 'datagen',
        'fields.id.kind' = 'sequence',
        'fields.id.start' = '1',
        'fields.id.end' = '10'
    )
""")

# 3. 创建 sink 表
table_env.execute_sql("""
    CREATE TABLE print (
        id INT,
        data STRING
    ) WITH (
        'connector' = 'print'
    )
""")

# 4. 查询 source 表，同时执行计算
# 通过 Table API 创建一张表：
source_table = table_env.from_path("datagen")
# 或者通过 SQL 查询语句创建一张表：
# source_table = table_env.sql_query("SELECT * FROM datagen")

result_table = source_table.select(source_table.id + 1, source_table.data)

# 5. 将计算结果写入给 sink 表
# 将 Table API 结果表数据写入 sink 表：
result_table.execute_insert("print").wait()
# 或者通过 SQL 查询语句来写入 sink 表：
# table_env.execute_sql("INSERT INTO print SELECT * FROM datagen").wait()

"""
TableEnvironment 可以用来:
    Table 管理：创建表、列举表、Table 和 DataStream 互转等。
    自定义函数管理：自定义函数的注册、删除、列举等。
    执行 SQL 语句
    作业配置管理：
    Python 依赖管理：
    作业提交：
"""