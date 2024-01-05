# from pyflink.table import EnvironmentSettings, TableEnvironment

# # 创建 批 TableEnvironment
# env_settings = EnvironmentSettings.in_batch_mode()
# table_env = TableEnvironment.create(env_settings)
#
# table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
# # 默认情况下，“id” 列的类型是 64 位整型
# print('By default the type of the "id" column is %s.' % table.get_schema().get_field_data_type("id"))
#
# from pyflink.table import DataTypes
#
# table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')],
#     DataTypes.ROW([DataTypes.FIELD("id", DataTypes.TINYINT()),
#                    DataTypes.FIELD("data", DataTypes.STRING())]))
# # 现在 “id” 列的类型是 8 位整型
# print('Now the type of the "id" column is %s.' % table.get_schema().get_field_data_type("id"))
#
# table.execute().print()

######### 通过 DDL 创建

# from pyflink.table import EnvironmentSettings, TableEnvironment
#
# # 创建 流 TableEnvironment
# env_settings = EnvironmentSettings.in_streaming_mode()
# table_env = TableEnvironment.create(env_settings)
#
# table_env.execute_sql("""
#     CREATE TABLE random_source (
#         id BIGINT,
#         data TINYINT
#     ) WITH (
#         'connector' = 'datagen',
#         'fields.id.kind'='sequence',
#         'fields.id.start'='1',
#         'fields.id.end'='3',
#         'fields.data.kind'='sequence',
#         'fields.data.start'='4',
#         'fields.data.end'='6'
#     )
# """)
# table = table_env.from_path("random_source")
# table.execute().print()

######## 通过 TableDescriptor 创建
# from pyflink.table import DataTypes, EnvironmentSettings, Schema, TableDescriptor, TableEnvironment
#
# # create a stream TableEnvironment
# env_settings = EnvironmentSettings.in_streaming_mode()
# table_env = TableEnvironment.create(env_settings)
#
# table_env.create_temporary_table(
#     'random_source',
#     TableDescriptor.for_connector('datagen')
#     .schema(Schema.new_builder()
#     .column('id', DataTypes.BIGINT())
#     .column('data', DataTypes.TINYINT())
#     .build())
#     .option('fields.id.kind', 'sequence')
#     .option('fields.id.start', '1')
#     .option('fields.id.end', '3')
#     .option('fields.data.kind', 'sequence')
#     .option('fields.data.start', '4')
#     .option('fields.data.end', '6')
#     .build())
#
# table = table_env.from_path("random_source")
# table.execute().print()


# from pyflink.table import EnvironmentSettings, TableEnvironment
# from pyflink.table.expressions import call, col
#
# # 通过 batch table environment 来执行查询
# env_settings = EnvironmentSettings.in_batch_mode()
# table_env = TableEnvironment.create(env_settings)
#
# orders = table_env.from_elements([
#     ('Jack', 'FRANCE', 10),
#     ('Rose', 'ENGLAND', 30),
#     ('Jack', 'FRANCE', 20)],
#     ['name', 'country', 'revenue'])
#
# # 计算所有来自法国客户的收入
# revenue = orders \
#     .select(col("name"), col("country"), col("revenue")) \
#     .where(col("country") == 'FRANCE') \
#     .group_by(col("name")) \
#     .select(col("name"), call("sum", col("revenue")).alias('rev_sum'))

# revenue.execute().print()


# from pyflink.table import EnvironmentSettings, TableEnvironment
# from pyflink.table import DataTypes
# from pyflink.table.udf import udf
# import pandas as pd

# # 通过 batch table environment 来执行查询
# env_settings = EnvironmentSettings.in_batch_mode()
# table_env = TableEnvironment.create(env_settings)

# orders = table_env.from_elements([('Jack', 'FRANCE', 10), ('Rose', 'ENGLAND', 30), ('Jack', 'FRANCE', 20)],
#                                  ['name', 'country', 'revenue'])

# map_function = udf(lambda x: pd.concat([x.name, x.revenue * 10], axis=1),
#                    result_type=DataTypes.ROW(
#                                [DataTypes.FIELD("name", DataTypes.STRING()),
#                                 DataTypes.FIELD("revenue", DataTypes.BIGINT())]),
#                    func_type="pandas")

# orders.map(map_function).execute().print()


# from pyflink.table import EnvironmentSettings, TableEnvironment

# # 通过 stream table environment 来执行查询
# env_settings = EnvironmentSettings.in_streaming_mode()
# table_env = TableEnvironment.create(env_settings)


# table_env.execute_sql(
#     """
#     CREATE TABLE random_source (
#         id BIGINT, 
#         data TINYINT
#     ) WITH (
#         'connector' = 'datagen',
#         'fields.id.kind'='sequence',
#         'fields.id.start'='1',
#         'fields.id.end'='8',
#         'fields.data.kind'='sequence',
#         'fields.data.start'='4',
#         'fields.data.end'='11'
#     )
# """
# )

# table_env.execute_sql(
#     """
#     CREATE TABLE print_sink (
#         id BIGINT, 
#         data_sum TINYINT 
#     ) WITH (
#         'connector' = 'print'
#     )
# """
# )

# table_env.execute_sql(
#     """
#     INSERT INTO print_sink
#         SELECT id, sum(data) as data_sum FROM 
#             (SELECT id / 2 as id, data FROM random_source)
#         WHERE id > 1
#         GROUP BY id
# """
# ).wait()

# # 创建一张 sink 表来接收结果数据
# table_env.execute_sql("""
#     CREATE TABLE table_sink (
#         id BIGINT, 
#         data VARCHAR 
#     ) WITH (
#         'connector' = 'print'
#     )
# """)

# # 将 Table API 表转换成 SQL 中的视图
# table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
# table_env.create_temporary_view('table_api_table', table)

# # 将 Table API 表的数据写入结果表
# table_env.execute_sql("INSERT INTO table_sink SELECT * FROM table_api_table").wait()


# # 使用流模式 TableEnvironment
# from pyflink.table import EnvironmentSettings, TableEnvironment
# from pyflink.table.expressions import col
#
# env_settings = EnvironmentSettings.in_streaming_mode()
# table_env = TableEnvironment.create(env_settings)
# # table_env.get_config().set("pipeline.jars", "file:///my/jar/path/connector.jar;file:///my/jar/path/udf.jar")
#
# table1 = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
# table2 = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
# table = table1 \
#     .where(col("data").like('H%')) \
#     .union_all(table2)
# print(table.explain())
# # table.execute().print()
#
# # TypeError: Could not found the Java class 'org.apache.flink.table.api.ExplainFormat.TEXT._get_object_id'.
# # The Java dependencies could be specified via command line argument '--jarfile' or the config option 'pipeline.jars'


# # 使用流模式 TableEnvironment
# from pyflink.table import EnvironmentSettings, TableEnvironment
# from pyflink.table.expressions import col
#
# env_settings = EnvironmentSettings.in_streaming_mode()
# table_env = TableEnvironment.create(environment_settings=env_settings)
#
# table1 = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
# table2 = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
# table_env.execute_sql("""
#     CREATE TABLE print_sink_table (
#         id BIGINT,
#         data VARCHAR
#     ) WITH (
#         'connector' = 'print'
#     )
# """)
# table_env.execute_sql("""
#     CREATE TABLE black_hole_sink_table (
#         id BIGINT,
#         data VARCHAR
#     ) WITH (
#         'connector' = 'blackhole'
#     )
# """)
#
# statement_set = table_env.create_statement_set()
#
# statement_set.add_insert("print_sink_table", table1.where(col("data").like('H%')))
# statement_set.add_insert("black_hole_sink_table", table2)
#
# print(statement_set.explain())

# from pyflink.table import EnvironmentSettings, TableEnvironment
#
# env_settings = EnvironmentSettings.in_streaming_mode()
# table_env = TableEnvironment.create(environment_settings=env_settings)
# # 设置重启策略为 "fixed-delay"
# table_env.get_config().set("restart-strategy.type", "fixed-delay")
# table_env.get_config().set("restart-strategy.fixed-delay.attempts", "3")
# table_env.get_config().set("restart-strategy.fixed-delay.delay", "30s")
#
# # 设置 checkpoint 模式为 EXACTLY_ONCE
# table_env.get_config().set("execution.checkpointing.mode", "EXACTLY_ONCE")
# table_env.get_config().set("execution.checkpointing.interval", "3min")
#
# # 设置 statebackend 类型为 "rocksdb"，其他可选项有 "filesystem" 和 "jobmanager"
# # 你也可以将这个属性设置为 StateBackendFactory 的完整类名
# # e.g. org.apache.flink.contrib.streaming.state.RocksDBStateBackendFactory
# table_env.get_config().set("state.backend.type", "rocksdb")
#
# # 设置 RocksDB statebackend 所需要的 checkpoint 目录
# table_env.get_config().set("state.checkpoints.dir", "file:///tmp/checkpoints/")
#
#
# # set to UTC time zone
# table_env.get_config().set_local_timezone("UTC")
#
# # set to Shanghai time zone
# table_env.get_config().set_local_timezone("Asia/Shanghai")
#
# # requirements_cache_dir is optional
# table_env.set_python_requirements(
#     requirements_file_path="/path/to/requirements.txt",
#     requirements_cache_dir="cached_dir")
#
# table_env.add_python_archive(archive_path="/path/to/archive_file", target_dir=None)
# table_env.get_config().set_python_executable("/path/to/python")
#
# ## Python Table API
# # Specify `PROCESS` mode
# table_env.get_config().set("python.execution-mode", "process")
#
# # Specify `THREAD` mode
# table_env.get_config().set("python.execution-mode", "thread")

from pyflink.table import EnvironmentSettings, TableEnvironment

# 创建 TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')])

# 使用 logging 模块
import logging

logging.warning(table.get_schema())

# 使用 print 函数
print(table.get_schema())
