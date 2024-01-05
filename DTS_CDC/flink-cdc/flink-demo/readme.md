```bash
mvn archetype:generate \
 -DarchetypeGroupId=org.apache.flink \
 -DarchetypeArtifactId=flink-walkthrough-datastream-java \
 -DarchetypeVersion=1.18.0 \
 -DgroupId=frauddetection \
 -DartifactId=frauddetection \
 -Dversion=0.1 \
 -Dpackage=spendreport \
 -DinteractiveMode=false
```

```bash
mvn archetype:generate                \
  -DarchetypeGroupId=org.apache.flink   \
  -DarchetypeArtifactId=flink-quickstart-java \
  -DarchetypeVersion=1.18.0
# 或者
# curl https://flink.apache.org/q/quickstart.sh | bash -s 1.18.0

cd quickstart
mvn clean package
```

## Flink 程序剖析

1. 获取一个执行环境（execution environment）

   1. `StreamExecutionEnvironment` 是所有 Flink 程序的基础。

   2. ```java
      getExecutionEnvironment();
      createLocalEnvironment();
      createRemoteEnvironment(String host, int port, String... jarFiles);
      ```

   3. 通常，你只需要使用 `getExecutionEnvironment()` 即可，因为该方法会根据上下文做正确的处理：如果你在 IDE 中执行你的程序或将其作为一般的 Java 程序执行，那么它将创建一个本地环境，该环境将在你的本地机器上执行你的程序。如果你基于程序创建了一个 JAR 文件，并通过命令行运行它，Flink 集群管理器将执行程序的 main 方法，同时 `getExecutionEnvironment()` 方法会返回一个执行环境以在集群上执行你的程序

2. 加载/创建初始数据；

3. 指定数据相关的转换；

4. 指定计算结果的存储位置；

5. 触发程序执行

> 所有 Flink 程序都是延迟执行的：
>
> > 当程序的 main 方法被执行时，数据加载和转换不会直接发生。
> >
> > 相反，每个算子都被创建并添加到 dataflow 形成的有向图。
> >
> > 当执行被执行环境的 `execute()` 方法显示地触发时，这些算子才会真正执行。
> >
> > 程序是在本地执行还是在集群上执行取决于执行环境的类型

### 本地执行环境

```java
final StreamExecutionEnvironment env = StreamExecutionEnvironment.createLocalEnvironment();

DataStream<String> lines = env.addSource(/* some source */);
// 构建你的程序

env.execute();


// 从元素列表创建一个 DataStream
DataStream<Integer> myInts = env.fromElements(1, 2, 3, 4, 5);

// 从任何 Java 集合创建一个 DataStream
List<Tuple2<String, Integer>> data = ...
DataStream<Tuple2<String, Integer>> myTuples = env.fromCollection(data);

// 从迭代器创建一个 DataStream
Iterator<Long> longIt = ...
DataStream<Long> myLongs = env.fromCollection(longIt, Long.class);
```

## 配置批执行模式 

执行模式可以通过 `execute.runtime-mode` 设置来配置。有三种可选的值：

- `STREAMING`: 经典 DataStream 执行模式（默认)
- `BATCH`: 在 DataStream API 上进行批量式执行
- `AUTOMATIC`: 让系统根据数据源的边界性来决定

这可以通过 `bin/flink run ...` 的命令行参数进行配置，或者在创建/配置 `StreamExecutionEnvironment` 时写进程序。

```bash
 bin/flink run -Dexecution.runtime-mode=BATCH <jarFile>
```

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.setRuntimeMode(RuntimeExecutionMode.BATCH);
```

**不建议**用户在程序中设置运行模式，而是在提交应用程序时使用命令行进行设置
