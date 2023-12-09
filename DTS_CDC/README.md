# DTS

> 数据传输服务（Data Transfer Service，DTS）
>
> 数据复制服务（Data Replication Service，DRS）
>
> 变更数据捕获 （Change Data Capture，CDC）

- [腾讯云](https://cloud.tencent.com/document/product/571)
- [阿里云](https://help.aliyun.com/zh/dts/)
- [华为云](https://www.huaweicloud.com/product/drs.html)
- [百度云](https://cloud.baidu.com/doc/DTS/index.html)
- [火山引擎](https://www.volcengine.com/product/dts)
- [金山云](https://www.ksyun.com/nv/product/DTS.html)
- [天翼云](https://www.ctyun.cn/products/dts)
- [联通云](https://www.cucloud.cn/product/dts.html)

# DB 监控

- [mongodb](http://localhost:3000/d/f9520905-2c31-4688-9b63-48f3bc917787/mongodb?orgId=1&refresh=5s)
- [mysql](http://localhost:3000/d/MQWgroiiz/mysql-overview?orgId=1&refresh=1m)

# 数据准备

> https://ververica.github.io/flink-cdc-connectors/master/content/quickstart/mysql-postgres-tutorial.html

## Preparing data in mysql

```bash
CREATE DATABASE mydb;
USE mydb;
CREATE TABLE IF NOT EXISTS orders (
  order_id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  order_date DATETIME NOT NULL,
  customer_name VARCHAR(255) NOT NULL,
  price DECIMAL(10, 5) NOT NULL,
  product_id INTEGER NOT NULL,
  order_status BOOLEAN NOT NULL -- Whether order has been placed
) AUTO_INCREMENT = 10001;

INSERT INTO orders
VALUES (default, '2020-07-30 10:08:22', 'Jark', 50.50, 101, false),
       (default, '2020-08-30 10:11:09', 'Sally', 15.00, 102, false),
       (default, '2020-09-30 12:00:30', 'Edward', 25.25, 103, false);
# change
INSERT INTO orders
VALUES (default, '2023-07-30 15:22:00', 'Jark', 29.71, 104, false);
UPDATE orders SET order_status = true WHERE order_id = 10004;
DELETE FROM orders WHERE order_id = 10004;
```

## Preparing data in mongodb

```bash
// 1. initialize replica set
rs.initiate();
rs.status();

// 2. switch database
use mydb;

// 3. initialize data
db.orders.insertMany([
  {
    order_id: 101,
    order_date: ISODate("2020-07-30T10:08:22.001Z"),
    customer_id: 1001,
    price: NumberDecimal("50.50"),
    product: {
      name: 'scooter',
      description: 'Small 2-wheel scooter'
    },
    order_status: false
  },
  {
    order_id: 102, 
    order_date: ISODate("2020-07-30T10:11:09.001Z"),
    customer_id: 1002,
    price: NumberDecimal("15.00"),
    product: {
      name: 'car battery',
      description: '12V car battery'
    },
    order_status: false
  },
  {
    order_id: 103,
    order_date: ISODate("2020-07-30T12:00:30.001Z"),
    customer_id: 1003,
    price: NumberDecimal("25.25"),
    product: {
      name: 'hammer',
      description: '16oz carpenter hammer'
    },
    order_status: false
  }
]);

# change
db.orders.insert({ 
  order_id: 104, 
  order_date: ISODate("2020-07-30T12:00:30.001Z"),
  customer_id: 1004,
  price: NumberDecimal("25.25"),
  product: { 
    name: 'rocks',
    description: 'box of assorted rocks'
  },
  order_status: false
});
db.orders.updateOne(
  { order_id: 104 },
  { $set: { order_status: true } }
);

db.orders.deleteOne(
  { order_id : 104 }
);
```

## Preparing data in tidb

```bash
CREATE DATABASE mydb;
USE mydb;
CREATE TABLE orders (
                       order_id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
                       order_date DATETIME NOT NULL,
                       customer_name VARCHAR(255) NOT NULL,
                       price DECIMAL(10, 5) NOT NULL,
                       product_id INTEGER NOT NULL,
                       order_status BOOLEAN NOT NULL -- Whether order has been placed
) AUTO_INCREMENT = 10001;

INSERT INTO orders
VALUES (default, '2020-07-30 10:08:22', 'Jark', 50.50, 102, false),
      (default, '2020-07-30 10:11:09', 'Sally', 15.00, 105, false),
      (default, '2020-07-30 12:00:30', 'Edward', 25.25, 106, false);
      
# change
INSERT INTO orders
VALUES (default, '2020-07-30 15:22:00', 'Jark', 29.71, 104, false);
UPDATE orders SET order_status = true WHERE order_id = 10004;
DELETE FROM orders WHERE order_id = 10004;
```

# SeaTunnel

## install
https://mp.weixin.qq.com/s/eNWGP_09Oh4pHdoQkmGPzg
```bash
# Step 1: 准备环境: Java（Java 8 或 11，理论上高于 Java 8 的其他版本也可以工作）安装和 JAVA_HOME 设置。
# Step 2: 下载 SeaTunnel
export version="2.3.3"
##wget "https://archive.apache.org/dist/seatunnel/${version}/apache-seatunnel-${version}-bin.tar.gz"
wget "https://mirrors.tuna.tsinghua.edu.cn/apache/seatunnel/${version}/apache-seatunnel-${version}-bin.tar.gz"
tar -xzvf "apache-seatunnel-${version}-bin.tar.gz"
# Step 3: 安装连接器插件: 从 2.2.0-beta 开始，二进制包默认不提供连接器依赖
sh bin/install-plugin.sh 2.3.3

# 运行 SeaTunnel 应用程序
cd "apache-seatunnel-${version}"

# 

sh bin/seatunnel-cluster.sh -d

# 
wget https://mirrors.tuna.tsinghua.edu.cn/apache/seatunnel/seatunnel-web/1.0.0/apache-seatunnel-web-1.0.0-bin.tar.gz
# wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.30/mysql-connector-java-8.0.30.jar -P libs/
# http://127.0.0.1:8801/ui/
```
## demo启动

```bash
# SeaTunnel
./bin/seatunnel.sh --config ./config/v2.batch.config.template -e local
# 请先下载 Flink（所需版本>= 1.12.0）
./bin/start-seatunnel-flink-13-connector-v2.sh --config ./config/v2.streaming.conf.template
./bin/start-seatunnel-flink-15-connector-v2.sh --config ./config/v2.streaming.conf.template
# 请先下载 Spark（所需版本 >= 2.4.0）
## spark3.x.x
./bin/start-seatunnel-spark-3-connector-v2.sh \
--master local[4] \
--deploy-mode client \
--config ./config/seatunnel.streaming.conf.template
```

## 测试启动

```bash
./bin/seatunnel.sh -e local --config ../mongodb2es.config
./bin/seatunnel.sh -e local --config ../mysql2es.config
```

## 报错

1. Exception in thread "main" java.lang.NoClassDefFoundError: com/mysql/cj/jdbc/Driver

```bash
mkdir -p plugins/jdbc/lib/
wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.30/mysql-connector-java-8.0.30.jar -P plugins/jdbc/lib/
# 或
wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.30/mysql-connector-java-8.0.30.jar -P lib/
```

2. The driver has not received any packets from the server.

> base-url 增加 `?serverTimezone=GMT%2b8&useSSL=false`


# flink-cdc
## install
> https://archive.apache.org/dist/flink/
> 
> https://nightlies.apache.org/flink/flink-docs-release-1.18/zh/docs/try-flink/local_installation/
> 
```bash
export version="1.17.1"
wget "https://mirrors.tuna.tsinghua.edu.cn/apache/flink/flink-${version}/flink-${version}-bin-scala_2.12.tgz"
tar -xzvf "flink-${version}-bin-scala_2.12.tgz"
cd "flink-${version}/lib"

wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-elasticsearch7/3.0.1-1.17/flink-sql-connector-elasticsearch7-3.0.1-1.17.jar
wget https://repo1.maven.org/maven2/com/ververica/flink-sql-connector-mysql-cdc/2.4.2/flink-sql-connector-mysql-cdc-2.4.2.jar
wget https://repo1.maven.org/maven2/com/ververica/flink-sql-connector-tidb-cdc/2.4.2/flink-sql-connector-tidb-cdc-2.4.2.jar
wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/1.17.1/flink-sql-connector-kafka-1.17.1.jar

wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc/3.1.0-1.17/flink-connector-jdbc-3.1.0-1.17.jar
# wget https://repo.maven.apache.org/maven2/mysql/mysql-connector-java/8.0.19/mysql-connector-java-8.0.19.jar
wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-hive-3.1.3_2.12/1.18.0/flink-sql-connector-hive-3.1.3_2.12-1.18.0.jar

# Starting Flink cluster and Flink SQL CLI
# export JAVA_HOME=/opt/homebrew/opt/openjdk@11
./bin/start-cluster.sh
# http://localhost:8081/
./bin/stop-cluster.sh
#使用下面的命令启动 Flink SQL CLI
./bin/sql-client.sh
# 使用 savepoint 停止现有的 Flink 作业。
./bin/flink stop $Existing_Flink_JOB_ID
```
## demo启动
### MySQL CDC 导入 Elasticsearch
```bash
# 设置间隔时间为3秒
SET execution.checkpointing.interval = 3s;
# 设置本地时区为 Asia/Shanghai
SET table.local-time-zone = Asia/Shanghai;

CREATE CATALOG my_catalog WITH(
    'type' = 'jdbc',
    'default-database' = 'mydb',
    'username' = 'root',
    'password' = '123456',
    'base-url' = 'jdbc:mysql://127.0.0.1:33065'
);

USE CATALOG my_catalog;
# 建表报错: java.lang.UnsupportedOperationException
# jdbc catalog不支持建表，只是打通flink和mysql的连接，可以去读写mysql现有的库表 

# MySQL CDC 导入 Elasticsearch
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
SET pipeline.name= 'mysql-to-es';

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

INSERT INTO flink_orders_mysql SELECT o.* FROM orders AS o;

SET state.savepoints.dir='file:/tmp/';
STOP JOB 'e339219e70ba92fe53a1a33514a7032d' WITH SAVEPOINT;
SET execution.savepoint.path=file:/tmp/savepoint-e33921-651a309244f6;
INSERT INTO enriched_orders SELECT o.* FROM orders AS o; # 所有以下DML语句将从指定的保存点路径中恢复
# 由于指定的保存点路径将影响以下所有 DML 语句，因此您可以使用 RESET 命令重置此配置选项，即禁用从保存点还原
RESET execution.savepoint.path;
```

### MongoDB CDC 导入 Elasticsearch
```bash
CREATE TABLE orders_mongodb (
   db_name STRING METADATA FROM 'database_name' VIRTUAL,
   collection_name STRING METADATA  FROM 'collection_name' VIRTUAL,
   operation_ts TIMESTAMP_LTZ(3) METADATA FROM 'op_ts' VIRTUAL,
   _id STRING, 
   order_id INT,
   order_date TIMESTAMP_LTZ(3),
   customer_id INT,
   price DECIMAL(10, 5),
   product ROW<name STRING, description STRING>,
   order_status BOOLEAN,
   PRIMARY KEY (_id) NOT ENFORCED
 ) WITH (
   'connector' = 'mongodb-cdc',
   'hosts' = 'localhost:37017',
   'username' = 'fjp',
   'password' = 'fjp',
   'database' = 'mydb',
   'collection' = 'orders'
 );

 CREATE TABLE sink_orders_mongodb (
   order_id INT,
   order_date TIMESTAMP_LTZ(3),
   customer_id INT,
   price DECIMAL(10, 5),
   product ROW<name STRING, description STRING>,
   order_status BOOLEAN,
   db_name STRING,
   collection_name STRING,
   operation_ts TIMESTAMP_LTZ(3),
   PRIMARY KEY (order_id) NOT ENFORCED
 ) WITH (
     'connector' = 'elasticsearch-7',
     'hosts' = 'http://localhost:9200',
     'index' = 'flink_orders_mongodb'
 );

INSERT INTO sink_orders_mongodb
SELECT  o.order_id,
        o.order_date,
        o.customer_id,
        o.price,
        o.product,
        o.order_status,
        o.db_name,
        o.collection_name,
        o.operation_ts
FROM orders_mongodb AS o;
```
### MongoDB CDC 导入 kakfa
```bash
 CREATE TABLE Kafka_Table (
   order_id INT,
   order_date TIMESTAMP_LTZ(3),
   customer_id INT,
   price DECIMAL(10, 5),
   product ROW<name STRING, description STRING>,
   order_status BOOLEAN,
   PRIMARY KEY (order_id) NOT ENFORCED
 ) WITH (
     'connector' = 'kafka',
     'properties.bootstrap.servers' = '127.0.0.1:9092',
     'properties.group.id' = 'flink-cdc-kafka-group',
     'topic' = 'test_topic',
     'format' = 'debezium-json',
     'debezium-json.ignore-parse-errors' = 'true'
 );

INSERT INTO Kafka_Table
SELECT o.order_id,
        o.order_date,
        o.customer_id,
        o.price,
        o.product,
        o.order_status
FROM orders_mongodb AS o;
```
### MongoDB CDC 导入 console
```bash
CREATE TABLE print_table WITH ('connector' = 'print')
LIKE orders_mongodb (EXCLUDING ALL);

INSERT INTO print_table
SELECT * FROM orders_mongodb AS o;
```
### TiDB CDC 导入 Elasticsearch
```bash
CREATE TABLE orders_tidb (
   order_id INT,
   order_date TIMESTAMP(3),
   customer_name STRING,
   price DECIMAL(10, 5),
   product_id INT,
   order_status BOOLEAN,
   PRIMARY KEY (order_id) NOT ENFORCED
 ) WITH (
    'connector' = 'tidb-cdc',
    'tikv.grpc.timeout_in_ms' = '20000',
    'pd-addresses' = '127.0.0.1:2379',
    'database-name' = 'mydb',
    'table-name' = 'orders'
);

CREATE TABLE enriched_orders_tidb (
   order_id INT,
   order_date DATE,
   customer_name STRING,
   order_status BOOLEAN,
   PRIMARY KEY (order_id) NOT ENFORCED
 ) WITH (
     'connector' = 'elasticsearch-7',
     'hosts' = 'http://localhost:9200',
     'index' = 'flink_enriched_orders_tidb'
 );

INSERT INTO enriched_orders_tidb
  SELECT o.order_id, o.order_date, o.customer_name, o.order_status
  FROM orders_tidb AS o;
```

- mongodb2kafka update操作转为两条kafka数据，先删d,后建c
- MongoDB CDC 默认为 全量+增量 读取；使用copy.existing=false参数设置为只读增量

## 测试启动
### 准备
```bash
SET "execution.checkpointing.interval" = "4s";
SET "table.local-time-zone" = "Asia/Shanghai";
SET "sql-client.execution.result-mode" = "tableau";
CREATE CATALOG fjp_catalog WITH(
    'type' = 'jdbc',
    'default-database' = 'mydb',
    'username' = 'root',
    'password' = '123456',
    'base-url' = 'jdbc:mysql://127.0.0.1:33065'
);
```
### mysql2es
```bash
SET pipeline.name= 'mysql-to-es' ;

CREATE TABLE source_mysql_orders (
    PRIMARY KEY (order_id) NOT ENFORCED
)
WITH (
   'connector' = 'mysql-cdc',
   'hostname' = 'localhost',
   'port' = '33065',
   'username' = 'root',
   'password' = '123456',
   'database-name' = 'mydb',
   'table-name' = 'orders',
   'scan.startup.mode' = 'initial',
   'server-time-zone' = 'Asia/Shanghai'
)
LIKE  fjp_catalog.mydb.orders (EXCLUDING ALL);

CREATE TABLE sink_mysql_es_orders  WITH (
     'connector' = 'elasticsearch-7',
     'hosts' = 'http://localhost:9200',
     'index' = 'flink_sink_mysql_es_orders'
)
LIKE  fjp_catalog.mydb.orders (EXCLUDING ALL);

INSERT INTO sink_mysql_es_orders SELECT o.* FROM source_mysql_orders AS o;
```

### mongodb2es
```bash

```

### tidb2es
```bash
```
## 报错

# BitSail
## install
```bash
```
## demo启动
```bash
# mysql 有问题，不支持cdc
bash bin/bitsail run \
    --engine flink \
  --execution-mode run \
  --deployment-mode local \
  --conf Mysql_Print_Example.json


bash bin/bitsail run \
    --engine flink \
  --execution-mode run \
  --deployment-mode local \
  --conf MongoDB_Print_Example.json

  
bash bin/bitsail run \
    --engine flink \
  --execution-mode run \
  --deployment-mode local \
  --conf Fake_Kafka_Example.json


```
## 测试启动
## 报错

# debezium

## mongodb
- 支持的 MongoDB 拓扑: 副本集/分片集
- 如果连接器在任务快照完成之前停止，则在重新启动时，连接器将再次开始快照。
## install
```bash
wget https://repo1.maven.org/maven2/io/debezium/debezium-server-dist/2.4.1.Final/debezium-server-dist-2.4.1.Final.tar.gz

```
## demo启动
```bash
export DEBEZIUM_VERSION=2.4
docker-compose up -d
# 通过 UI 创建连接器: http://localhost:8080

docker exec -it db-mysql bash -c 'mysql -u $MYSQL_USER -p$MYSQL_PASSWORD inventory'

docker exec -it db-mongo bash -c 'mongo -u admin -p admin --authenticationDatabase admin localhost:37017/inventory'

# 检查更改事件
# Open in a new terminal
# Viewing the change events in the kafka container
docker exec -it kafka bash
./bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic [TOPIC_NAME] --from-beginning

db.orders.insert([
    { _id : NumberLong("10005"), order_date : new ISODate("2023-11-27T00:00:00Z"), purchaser_id : NumberLong("1001"), quantity : NumberInt("1"), product_id : NumberLong("102") },
]);

db.orders.updateOne(
  { _id: 10005 },
  { $set: { quantity: 10 } }
);

db.orders.deleteOne(
  { _id : 10005 }
);
  
db.orders.insert([
    { _id : NumberLong("10006"), order_date : new ISODate("2023-11-27T00:00:00Z"), purchaser_id : NumberLong("1001"), quantity : NumberInt("1"), product_id : NumberLong("102"), product_desc: 
      { 
        name: 'rocks',
        description: 'box of assorted rocks'
      } 
    },
]);
  
# 停止所有服务
docker-compose down
```
## 测试启动
```bash
# docker run -it --rm --name connect -p 8083:8083 -e GROUP_ID=1 -e CONFIG_STORAGE_TOPIC=my_connect_configs -e OFFSET_STORAGE_TOPIC=my_connect_offsets -e STATUS_STORAGE_TOPIC=my_connect_statuses --link kafka:kafka --link mysql:mysql quay.io/debezium/connect:2.4
{
  "name": "inventory-connector",  # 连接器的名称
  "config": {  
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "tasks.max": "1",  # MySQL connector 任何时候都只能运行一个任务。由于 MySQL 连接器读取 MySQL 服务器的 binlog ，因此使用单个连接器任务可确保正确的顺序和事件处理
    "database.hostname": "mysql",  
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "dbz",
    "database.server.id": "184054",  
    "topic.prefix": "dbserver1",  # 唯一的主题前缀。此名称将用作所有 Kafka 主题的前缀。 
    "database.include.list": "inventory",  
    "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",  # 连接器将使用相同的brokers（发送事件的brokers）和主题名称，在Kafka中存储数据库模式的历史记录。在重新启动时，连接器将恢复在binlog中连接器应开始读取的时间点存在的数据库模式
    "schema.history.internal.kafka.topic": "schema-changes.inventory"  
  }

# snapshot.mode = initial/initial_only/when_needed/never/schema_only/schema_only_recovery

SELECT * FROM customers;
UPDATE customers SET first_name='Anne Marie' WHERE id=1004;
DELETE FROM addresses WHERE customer_id=1004;
DELETE FROM customers WHERE id=1004;
# 墓碑事件 (tombstone event) a key and an empty value
INSERT INTO customers VALUES (default, "Sarah", "Thompson", "kitt@acme.com");
INSERT INTO customers VALUES (default, "Kenneth", "Anderson", "kander@acme.com");
```
## 报错
- `Config property 'mongodb.hosts' will be removed in the future, use 'mongodb.connection.string' instead`
- https://docs.redis.com/latest/rdi/installation/debezium-server-configuration/

## MYSQL2ES -- Topology
```
                   +-------------+
                   |             |
                   |    MySQL    |
                   |             |
                   +------+------+
                          |
                          |
                          |
          +---------------v------------------+
          |                                  |
          |           Kafka Connect          |
          |    (Debezium, ES connectors)     |
          |                                  |
          +---------------+------------------+
                          |
                          |
                          |
                          |
                  +-------v--------+
                  |                |
                  | Elasticsearch  |
                  |                |
                  +----------------+


```
```bash
# Start the application
export DEBEZIUM_VERSION=2.4
docker compose -f docker-compose-mysql2es.yaml up --build
# Start Elasticsearch connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @es-sink.json
# Start MySQL connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @mysql-source.json

# Check contents of the MySQL database:
docker compose -f docker-compose-mysql2es.yaml exec mysql bash -c 'mysql -u $MYSQL_USER  -p$MYSQL_PASSWORD inventory -e "select * from customers"'
# Verify that Elasticsearch has the same content:
curl 'http://localhost:9200/customers/_search?pretty'

# Insert a new record into MySQL:
docker compose -f docker-compose-mysql2es.yaml exec mysql bash -c 'mysql -u $MYSQL_USER  -p$MYSQL_PASSWORD inventory'
insert into customers values(default, 'John', 'Doe', 'john.doe@example.com');
# Update a record in MySQL:
update customers set first_name='Jane', last_name='Roe' where last_name='Doe';
# Delete a record in MySQL:
delete from customers where email='john.doe@example.com';

# Shut down the cluster
docker compose -f docker-compose-mysql2es.yaml down
```
## MONGODB2ES
```bash
docker-compose -f docker-compose-mongodb2es.yaml up --build
# Initialize MongoDB replica set and insert some test data
docker compose exec mongodb bash -c '/usr/local/bin/init-inventory.sh'
# Current host
# if using docker-machine:
#export CURRENT_HOST=$(docker-machine ip $(docker-machine active));
# or any other host
export CURRENT_HOST='localhost'

# Start Elasticsearch connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://$CURRENT_HOST:8083/connectors/ -d @mongodb-es-sink.json
# Start Debezium MongoDB CDC connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://$CURRENT_HOST:8083/connectors/ -d @mongodb-source.json

# Check contents of the MongoDB database:
docker compose exec mongodb bash -c 'mongo -u $MONGODB_USER -p $MONGODB_PASSWORD --authenticationDatabase admin inventory --eval "db.customers.find()"'
# Insert a new record into MongoDB:
docker compose exec mongodb bash -c 'mongo -u $MONGODB_USER -p $MONGODB_PASSWORD --authenticationDatabase admin inventory'
db.customers.insert([
    { _id : NumberLong("1005"), first_name : 'Bob', last_name : 'Hopper', email : 'bob@example.com' }
]);
# Update a record in MongoDB:
db.customers.update(
   {
    _id : NumberLong("1005")
   },
   {
     $set : {
       first_name: "Billy-Bob"
     }
   }
);
db.customers.remove(
   {
    _id: NumberLong("1005")
   }
);

docker compose -f docker-compose-mongodb2es.yaml down
```