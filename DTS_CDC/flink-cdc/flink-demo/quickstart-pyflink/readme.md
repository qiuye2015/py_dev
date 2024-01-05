# prepare
```bash
python --version
# the version printed here must be 3.7, 3.8, 3.9 or 3.10
python -m pip install apache-flink==1.18.0
python -m pip install apache-flink==1.17.1
# 准备Python虚拟环境
# sh setup-pyflink-virtual-env.sh 1.18.0
```

# backup
```python

from pyflink.table import EnvironmentSettings, TableEnvironment
#  TODO:del
"""
FLINK_BIN_DIR=/opt/flink/bin
PYFLINK_GATEWAY_PORT=46005
FLINK_CONF_DIR=/opt/flink/conf

export FLINK_PLUGINS_DIR="/Users/leo.fu1/workspace/github/icoding/py_dev/DTS_CDC/flink-cdc/flink-1.17/plugins"
export PYTHONPATH="/Users/leo.fu1/workspace/github/icoding/py_dev/DTS_CDC/flink-cdc/flink-1.17.1/opt/python/pyflink.zip:/Users/leo.fu1/workspace/github/icoding/py_dev/DTS_CDC/flink-cdc/flink-1.17.1/opt/python/cloudpickle-2.1.0-src.zip:/Users/leo.fu1/workspace/github/icoding/py_dev/DTS_CDC/flink-cdc/flink-1.17.1/opt/python/py4j-0.10.9.3-src.zip:."
export FLINK_LIB_DIR="/Users/leo.fu1/workspace/github/icoding/py_dev/DTS_CDC/flink-cdc/flink-1.17.1/lib"
export FLINK_HOME="/Users/leo.fu1/workspace/github/icoding/py_dev/DTS_CDC/flink-cdc/flink-1.17.1"
export FLINK_OPT_DIR="/Users/leo.fu1/workspace/github/icoding/py_dev/DTS_CDC/flink-cdc/flink-1.17.1/opt"


jars = []
for file in os.listdir(os.path.abspath(os.path.dirname(__file__))):
    if file.endswith('.jar'):
        jars.append(os.path.abspath(file))
str_jars = ';'.join(['file://' + jar for jar in jars])
t_env.get_config().get_configuration().set_string("pipeline.jars", str_jars)
"""


def log_processing():
    env_settings = EnvironmentSettings.in_streaming_mode()
    t_env = TableEnvironment.create(env_settings)
    # # specify connector and format jars
    # base_path = '/Users/leo.fu1/workspace/github/icoding/py_dev/DTS_CDC/flink-cdc/flink-1.17.1/lib'
    # # t_env.get_config().set("pipeline.jars", f"file://{base_path}/connector.jar;file://{base_path}/json.jar")
    # jar_str = f"file://{base_path}/flink-sql-connector-kafka-1.17.1.jar"
    # jar_str += f";file://{base_path}/flink-json-1.17.1.jar"
    # jar_str += f";file://{base_path}/flink-table-runtime-1.17.1.jar"
    # jar_str += f";file://{base_path}/flink-table-planner-loader-1.17.1.jar"
    #
    # cur_path = os.path.abspath(os.path.dirname(__file__))
    # jar_str += f";file://{cur_path}/flink-clients-1.17.1.jar"
    # # jar_str += f";file://{base_path}/flink-table-runtime-1.17.1.jar"
    # print(jar_str)
    # t_env.get_config().set("pipeline.jars", jar_str)

    source_ddl = """
              CREATE TABLE orders (
               order_id INT,
               order_date TIMESTAMP(0),
               customer_name STRING,
               price DECIMAL(10, 5),
               product_id INT,
               order_status BOOLEAN,
               PRIMARY KEY (order_id) NOT ENFORCED
             ) WITH (
               'connector' = 'mysql-cdc',
               'hostname' = 'localhost',
               'port' = '33065',
               'username' = 'root',
               'password' = '123456',
               'database-name' = 'mydb',
               'table-name' = 'orders'
             );
            """
    #
    # sink_ddl = """
    #              CREATE TABLE print (
    #                order_id INT,
    #                order_date TIMESTAMP(0),
    #                customer_name STRING,
    #                price DECIMAL(10, 5),
    #                product_id INT,
    #                order_status BOOLEAN,
    #                PRIMARY KEY (order_id) NOT ENFORCED
    #             ) WITH (
    #                 'connector' = 'print'
    #             )
    #         """

    sink_ddl = """
     CREATE TABLE flink_orders_mysql (
       order_id INT,
       order_date TIMESTAMP(0),
       customer_name STRING,
       price DECIMAL(10, 5),
       product_id INT,
       order_status BOOLEAN,
       PRIMARY KEY (order_id) NOT ENFORCED
     ) WITH (
         'connector' = 'elasticsearch-7',
         'hosts' = 'http://localhost:9200',
         'index' = 'flink_orders_mysql'
     );
            """

    t_env.execute_sql(source_ddl)
    t_env.execute_sql(sink_ddl)
    print("fjp", "*" * 20)

    t_env.sql_query("SELECT * FROM orders") \
        .execute_insert("flink_orders_mysql").wait()

    # t_env.sql_query("SELECT * FROM orders") \
    #     .execute_insert("print").wait()


if __name__ == '__main__':
    log_processing()

```