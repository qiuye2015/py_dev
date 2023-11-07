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
## demo启动

```bash
# SeaTunnel
./bin/seatunnel.sh --config ./config/v2.batch.config.template -e local
./bin/start-seatunnel-flink-13-connector-v2.sh --config ./config/v2.streaming.conf.template
./bin/start-seatunnel-flink-15-connector-v2.sh --config ./config/v2.streaming.conf.template
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
## demo启动
## 测试启动
## 报错

# BitSail
## demo启动
## 测试启动
## 报错

# debezium
## demo启动
## 测试启动
## 报错

