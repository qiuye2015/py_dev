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
CREATE TABLE orders (
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
use mgdb;

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
```bash
export version="1.17.1"
wget "https://mirrors.tuna.tsinghua.edu.cn/apache/flink/flink-${version}/flink-${version}-bin-scala_2.12.tgz"
tar -xzvf "flink-${version}-bin-scala_2.12.tgz"

wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-elasticsearch7/3.0.1-1.17/flink-sql-connector-elasticsearch7-3.0.1-1.17.jar
wget https://repo1.maven.org/maven2/com/ververica/flink-sql-connector-mysql-cdc/2.4.2/flink-sql-connector-mysql-cdc-2.4.2.jar
wget https://repo1.maven.org/maven2/com/ververica/flink-sql-connector-tidb-cdc/2.4.2/flink-sql-connector-tidb-cdc-2.4.2.jar
wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/1.17.1/flink-sql-connector-kafka-1.17.1.jar
# Starting Flink cluster and Flink SQL CLI
export JAVA_HOME=/opt/homebrew/opt/openjdk@11
./bin/start-cluster.sh
# http://localhost:8081/
./bin/stop-cluster.sh
```
## demo启动
```bash
#使用下面的命令启动 Flink SQL CLI
./bin/sql-client.sh

# 设置间隔时间为3秒
SET execution.checkpointing.interval = 3s;
# 设置本地时区为 Asia/Shanghai
SET table.local-time-zone = Asia/Shanghai;

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


CREATE TABLE enriched_orders (
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
     'index' = 'enriched_orders'
 );

INSERT INTO enriched_orders SELECT o.* FROM orders AS o;

# MongoDB CDC 导入 Elasticsearch
CREATE TABLE orders_mongodb (
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
   'database' = 'mgdb',
   'collection' = 'orders'
 );

 CREATE TABLE enriched_orders_mongodb (
   order_id INT,
   order_date TIMESTAMP_LTZ(3),
   customer_id INT,
   price DECIMAL(10, 5),
   product ROW<name STRING, description STRING>,
   order_status BOOLEAN,
   PRIMARY KEY (order_id) NOT ENFORCED
 ) WITH (
     'connector' = 'elasticsearch-7',
     'hosts' = 'http://localhost:9200',
     'index' = 'enriched_orders_mongodb'
 );

INSERT INTO enriched_orders_mongodb
SELECT o.order_id,
        o.order_date,
        o.customer_id,
        o.price,
        o.product,
        o.order_status
FROM orders_mongodb AS o;

# MongoDB CDC 导入 kakfa

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

# MongoDB CDC 导入 console

CREATE TABLE print_table WITH ('connector' = 'print')
LIKE orders_mongodb (EXCLUDING ALL);

INSERT INTO print_table
SELECT * FROM orders_mongodb AS o;
```
- mongodb2kafka update操作转为两条kafka数据，先删d,后建c

## 测试启动
## 报错

# BitSail
## install
```bash
```
## demo启动
## 测试启动
## 报错

# debezium
## install
```bash
```
## demo启动
## 测试启动
## 报错

