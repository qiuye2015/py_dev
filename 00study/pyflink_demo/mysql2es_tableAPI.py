from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment, TableEnvironment
from pyflink.table.udf import udf
from pyflink.table.descriptors import Schema, Rowtime
from pyflink.table.window import Tumble
from pyflink.common import Configuration
from pyflink.table import TableEnvironment, EnvironmentSettings

# # 创建执行环境
# env_settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
# env = StreamExecutionEnvironment.get_execution_environment()
# t_env = StreamTableEnvironment.create(env, environment_settings=env_settings)

# t_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())

# create a streaming TableEnvironment
config = Configuration()
config.set_string("python.fn-execution.bundle.size", "1000")
env_settings = EnvironmentSettings.new_instance().in_streaming_mode().with_configuration(config).build()
t_env = TableEnvironment.create(env_settings)

# or directly pass config into create method
# table_env = TableEnvironment.create(config)

# https://nightlies.apache.org/flink/flink-docs-release-1.16/zh/docs/dev/python/dependency_management/#java-dependency-in-python-program
# filepath = "file:///my/jar/path/connector.jar;file:///my/jar/path/udf.jar"
filepath = "file:///Users/leo.fu1/workspace/gitlab/mysql_mongodb_cdc/flink-1.16.2/flink-sql-connector-mysql-cdc-2.3.0.jar;file:///Users/leo.fu1/workspace/gitlab/mysql_mongodb_cdc/flink-1.16.2/mysql-connector-java-8.0.26.jar;file:///Users/leo.fu1/workspace/gitlab/mysql_mongodb_cdc/flink-1.16.2/flink-sql-connector-elasticsearch7-3.0.1-1.17.jar"
# 注意：仅支持本地文件URL（以"file:"开头）。
t_env.get_config().set("pipeline.jars", filepath)

# 注意：路径必须指定协议（例如：文件——"file"），并且用户应确保在客户端和群集上都可以访问这些URL。
t_env.get_config().set("pipeline.classpaths", filepath)

# 定义MySQL和Elasticsearch的连接信息
mysql_conn = {
    "hostname": "localhost",
    "port": 13306,
    "username": "root",
    "password": "123456",
    "database": "test_flink_cdc",
    "tablename": "table_33",
}

es_conn = {
    "cluster_name": "your_cluster_name",
    "hosts": "localhost:9200",
    "index": "your_index",
}

# 创建MySQL表
t_env.execute_sql(
    """
    CREATE TABLE mysql_source (
        id INT,
        meta_uuid STRING
    ) WITH (
        'connector' = 'mysql-cdc',
        'url' = 'jdbc:mysql://{hostname}:{port}/{database}',
        'table-name' = '{tablename}',
        'username' = '{username}',
        'password' = '{password}',
        'driver' = 'com.mysql.jdbc.Driver',
        'scan.incremental.snapshot.enabled' = 'true',
        'scan.incremental.snapshot.last' = '0'
    )
""".format(
        **mysql_conn
    )
)

# 创建Elasticsearch索引
t_env.execute_sql(
    """
    CREATE TABLE es_sink (
        id INT,
        meta_uuid STRING,
        PRIMARY KEY (id) NOT ENFORCED
    ) WITH (
        'connector' = 'elasticsearch-7',
        'hosts' = '{hosts}',
        'index' = '{index}',
        'format' = 'json'
    )
""".format(
        **es_conn
    )
)

# 定义查询
t_env.execute_sql(
    """
    INSERT INTO es_sink
    SELECT id, meta_uuid
    FROM mysql_source
"""
)

# 执行作业
t_env.execute("Flink CDC Service")
