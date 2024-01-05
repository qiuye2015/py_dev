import json

from pyflink.common import Row
from pyflink.table import DataTypes, EnvironmentSettings, TableEnvironment
from pyflink.table.udf import udf


# 定义自定义的 UDF 函数
@udf(
    input_types=[DataTypes.STRING()],
    result_type=DataTypes.ROW([DataTypes.FIELD("app_version", DataTypes.STRING()),
                               DataTypes.FIELD("ptp_timestamp", DataTypes.BIGINT())]),
)
def string_to_dict(s):
    res = {}
    content = {}
    try:
        content = json.loads(s)
    except Exception as e:
        print(f"LDD------> {s},{e}")
    app_version = None
    ptp_timestamp = None
    print(f"FJP------>{s}")
    if "app_version" in content:
        app_version = content["app_version"]
        res["app_version"] = app_version
    if "ptp_timestamp" in content:
        ptp_timestamp = content["ptp_timestamp"]
        res["ptp_timestamp"] = ptp_timestamp
    return Row(app_version=app_version, ptp_timestamp=ptp_timestamp)


namespace_map = {
    "table_33": "production/log"
}


@udf(
    input_types=[DataTypes.STRING()],
    result_type=DataTypes.STRING(),
)
def add_namespace_by_table_name(table_name):
    print(f"FJP---->{table_name}")
    ns = namespace_map.get(table_name, 'empty_namespace')
    return ns


def log_processing():
    env_settings = EnvironmentSettings.in_streaming_mode()
    t_env = TableEnvironment.create(env_settings)

    # db_name STRING METADATA FROM 'database_name' VIRTUAL,
    # table_name STRING METADATA  FROM 'table_name' VIRTUAL,
    # operation_ts TIMESTAMP_LTZ(3) METADATA FROM 'op_ts' VIRTUAL,
    source_ddl = """
              CREATE TABLE source_mysql_table_33 (
                   table_name STRING METADATA  FROM 'table_name' VIRTUAL,
                   rowkey STRING,
                   meta_uuid STRING,
                   meta_storage_state INT,
                   meta_extra_data STRING,
                   meta_trigger_time BIGINT,
                   sys_data_name STRING,
                   sys_data_id  BIGINT,
                   sys_create_time INT,
                   PRIMARY KEY (meta_uuid) NOT ENFORCED
             ) WITH (
                   'connector' = 'mysql-cdc',
                   'hostname' = 'localhost',
                   'port' = '33065',
                   'username' = 'root',
                   'password' = '123456',
                   'database-name' = 'mydb',
                   'table-name' = 'table_33'
             );
            """

    # sink_ddl = """
    #     CREATE TABLE sink_mysql_es_table_33 (
    #         PRIMARY KEY (meta_uuid) NOT ENFORCED
    #      ) WITH (
    #          'connector' = 'elasticsearch-7',
    #          'hosts' = 'http://localhost:9200',
    #          'index' = 'flink_sink_mysql_es_table_33'
    #      )
    #     LIKE source_mysql_table_33 (EXCLUDING ALL);
    # """

    # sink_ddl = """CREATE TABLE sink_mysql_es_table_33 (
    #                     rowkey	STRING,
    #                     meta    ROW<uuid STRING, storage_state INT, extra_data STRING,trigger_time BIGINT>,
    #                     sys		ROW<create_time INT, data_name STRING, data_id BIGINT>,
    #                     CONSTRAINT id PRIMARY KEY (rowkey) NOT ENFORCED
    #                  ) WITH (
    #                      'connector' = 'elasticsearch-7',
    #                      'hosts' = 'http://localhost:9200',
    #                      'index' = 'flink_sink_mysql_es_table_33_v2'
    #                  );
    #         """

    sink_ddl = """CREATE TABLE sink_mysql_es_table_33 (
                        rowkey	STRING,
                        meta    ROW<uuid STRING, storage_state INT, extra_data ROW<app_version STRING,ptp_timestamp BIGINT>,trigger_time BIGINT,namespace STRING>,
                        sys		ROW<create_time INT, data_name STRING, data_id BIGINT>,
                        CONSTRAINT id PRIMARY KEY (rowkey) NOT ENFORCED
                     ) WITH (
                         'connector' = 'elasticsearch-7',
                         'hosts' = 'http://localhost:9200',
                         'index' = 'flink_sink_mysql_es_table_33_v4'
                     );
            """
    #  'sink.flush-on-checkpoint' = true
    #  -{meta_trigger_time|yyyy-MM}

    t_env.execute_sql(source_ddl)
    t_env.execute_sql(sink_ddl)
    print("fjp", "*" * 20)

    # t_env.sql_query("SELECT * FROM source_mysql_table_33") \
    #     .execute_insert("sink_mysql_es_table_33")
    #
    # transform_dml = """
    #     INSERT INTO sink_mysql_es_table_33
    #     SELECT * FROM source_mysql_table_33;
    # """

    t_env.register_function("string_to_dict", string_to_dict)
    t_env.register_function("add_namespace", add_namespace_by_table_name)
    transform_dml = """
        INSERT INTO sink_mysql_es_table_33
        SELECT rowkey, 
        ROW(meta_uuid, meta_storage_state, string_to_dict(meta_extra_data), meta_trigger_time,add_namespace(table_name)), 
        ROW(sys_create_time,sys_data_name,sys_data_id)
        FROM source_mysql_table_33;
    """
    t_env.execute_sql(transform_dml)


if __name__ == '__main__':
    log_processing()
