import json

from pyflink.table import DataTypes, EnvironmentSettings, TableEnvironment
from pyflink.table.udf import udf


def log_processing():
    env_settings = EnvironmentSettings.in_streaming_mode()
    t_env = TableEnvironment.create(env_settings)
    # source_ddl = """
    #                 CREATE TABLE source_mongo_yunfan_vehicle (
    #                     _id STRING,
    #                     rowkey	STRING,
    #                     meta	MAP<STRING, STRING>,
    #                     sys		MAP<STRING, STRING>,
    #                     CONSTRAINT id PRIMARY KEY (_id) NOT ENFORCED
    #                 ) WITH (
    #                    'connector' = 'mongodb-cdc',
    #                    'hosts' = 'localhost:37017',
    #                    'username' = 'fjp',
    #                    'password' = 'fjp',
    #                    'database' = 'mydb',
    #                    'collection' = 'yunfan_vehicle'
    #                  );
    #                 """

    # sink_ddl = """
    #                 CREATE TABLE sink_mongo_es_yunfan_vehicle (
    #                     rowkey	STRING,
    #                     meta	MAP<STRING, STRING>,
    #                     sys		MAP<STRING, STRING>,
    #                     CONSTRAINT id PRIMARY KEY (rowkey) NOT ENFORCED
    #                  ) WITH (
    #                      'connector' = 'elasticsearch-7',
    #                      'hosts' = 'http://localhost:9200',
    #                      'index' = 'flink_sink_mongo_es_yunfan_vehicle'
    #                  );
    #         """

    # 上面类型不对

    # source_ddl = """CREATE TABLE source_mongo_yunfan_vehicle (
    #                     _id STRING,
    #                     rowkey	STRING,
    #                     meta	ROW<basic_info STRING, vehicle_id STRING, cdm_config STRING, dlb_config STRING,heartbeat_time BIGINT>,
    #                     sys		ROW<create_time INT, data_name STRING, data_id BIGINT, table_name STRING>,
    #                     CONSTRAINT id PRIMARY KEY (_id) NOT ENFORCED
    #                 ) WITH (
    #                    'connector' = 'mongodb-cdc',
    #                    'hosts' = 'localhost:37017',
    #                    'username' = 'fjp',
    #                    'password' = 'fjp',
    #                    'database' = 'mydb',
    #                    'collection' = 'yunfan_vehicle'
    #                  );
    #                 """

    #
    # sink_ddl = """CREATE TABLE sink_mongo_es_yunfan_vehicle (
    #                     rowkey	STRING,
    #                     meta	ROW<basic_info STRING, vehicle_id STRING, cdm_config STRING, dlb_config STRING,heartbeat_time BIGINT>,
    #                     sys		ROW<create_time INT, data_name STRING, data_id BIGINT, table_name STRING>,
    #                     CONSTRAINT id PRIMARY KEY (rowkey) NOT ENFORCED
    #                  ) WITH (
    #                      'connector' = 'elasticsearch-7',
    #                      'hosts' = 'http://localhost:9200',
    #                      'index' = 'flink_sink_mongo_es_yunfan_vehicle_v2'
    #                  );
    #         """

    # basic_info string to dict
    source_ddl = """CREATE TABLE source_mongo_yunfan_vehicle (
                        _id STRING,
                        rowkey	STRING,
                        meta	ROW<basic_info STRING, vehicle_id STRING, version BIGINT, modified_time BIGINT>,
                        sys		ROW<create_time INT, data_name STRING, data_id BIGINT, table_name STRING>,
                        CONSTRAINT id PRIMARY KEY (_id) NOT ENFORCED
                    ) WITH (
                       'connector' = 'mongodb-cdc',
                       'hosts' = 'localhost:37017',
                       'username' = 'fjp',
                       'password' = 'fjp',
                       'database' = 'mydb',
                       'collection' = 'yunfan_vehicle'
                     );
                    """

    sink_ddl = """CREATE TABLE sink_mongo_es_yunfan_vehicle (
                        rowkey	STRING,
                        meta    ROW<basic_info MAP<STRING, STRING>, vehicle_id STRING, version BIGINT, modified_time BIGINT>,
                        sys		ROW<create_time INT, data_name STRING, data_id BIGINT, table_name STRING>,
                        CONSTRAINT id PRIMARY KEY (rowkey) NOT ENFORCED
                     ) WITH (
                         'connector' = 'elasticsearch-7',
                         'hosts' = 'http://localhost:9200',
                         'index' = 'flink_sink_mongo_es_yunfan_vehicle_v3'
                     );
            """
    t_env.execute_sql(source_ddl)
    t_env.execute_sql(sink_ddl)

    print("fjp", "*" * 20)
    # transform_dml = """
    #     INSERT INTO sink_mongo_es_yunfan_vehicle
    #     SELECT rowkey, meta, sys
    #     FROM source_mongo_yunfan_vehicle;
    # """

    t_env.register_function("string_to_dict", string_to_dict)
    transform_dml = """
        INSERT INTO sink_mongo_es_yunfan_vehicle
        SELECT rowkey, 
        ROW(string_to_dict(meta.basic_info), meta.vehicle_id, meta.version, meta.modified_time),
        sys
        FROM source_mongo_yunfan_vehicle;
    """
    t_env.execute_sql(transform_dml)


# 定义自定义的 UDF 函数
@udf(
    input_types=[DataTypes.STRING()],
    result_type=DataTypes.MAP(DataTypes.STRING(), DataTypes.STRING()),
)
def string_to_dict(s):
    res = {}
    content = json.loads(s)
    if "brand" in content:
        res["brand"] = content["brand"]
    if "platform" in content:
        res["platform"] = content["platform"]
    return res


if __name__ == "__main__":
    log_processing()
