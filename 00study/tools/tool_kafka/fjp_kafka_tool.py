"""
pip install kafka-python
from kafka import KafkaConsumer,KafkaProducer,TopicPartition

pip install confluent-kafka
from confluent_kafka import Consumer,Producer
from confluent_kafka.admin import AdminClient, NewTopic

Consumer: kafka-python
Producer: confluent-kafka
"""
import argparse
from collections import defaultdict
from datetime import datetime
import json
import time

from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer, TopicPartition
from loguru import logger


# 创建Kafka客户端
def create_consumer_client(bootstrap_servers, group_id, username=None, password=None):
    if not bootstrap_servers or not group_id:
        raise ValueError("bootstrap_servers and group_id must be a non-empty string")

    config = {
        'bootstrap_servers': bootstrap_servers,
        'group_id': group_id,
        'client_id': 'fjp_kafka_tool_consumer',

        'session_timeout_ms': 10000,
        'max_poll_records': 500,
        'max_poll_interval_ms': 300000,
        'max_partition_fetch_bytes': 1 * 1024 * 1024,

        'auto_offset_reset': 'earliest',  # Default: 'latest'
        'enable_auto_commit': False,  # Default: True.
        'auto_commit_interval_ms': 5000,

        'key_deserializer': lambda k: k.decode("utf-8") if k is not None else k,
        'value_deserializer': lambda v: json.loads(v.decode('utf-8')) if v is not None else v,
    }

    if username is not None and password is not None:
        config.update({
            'security_protocol': 'SASL_PLAINTEXT',
            'sasl_mechanism': 'PLAIN',
            'sasl_plain_username': username,
            'sasl_plain_password': password,
        })

    return KafkaConsumer(**config)


def create_producer_client(bootstrap_servers, username=None, password=None):
    config = {
        'bootstrap_servers': bootstrap_servers,
        'api_version': (1, 1),
        'client_id': 'fjp_kafka_tool_producer',

        'acks': 1,

        'retries': 0,  # 重试次数
        'retry_backoff_ms': 100,  # 重试间隔

        'batch_size': 16384,  # 发往每个分区（Partition）的消息缓存量
        'linger_ms': 0,  # 每条消息在缓存中的最长时间。若超过这个时间，Producer客户端就会忽略`batch.size`的限制，立即把消息发往服务器
        'buffer_memory': 33554432,  # 所有缓存消息的总体大小超过这个数值后，就会触发把消息发往服务器。此时会忽略`batch.size`和`linger.ms`的限制

        'value_serializer': lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'),
        'key_serializer': str.encode,
    }

    if username is not None and password is not None:
        config.update({
            'security_protocol': 'SASL_PLAINTEXT',
            'sasl_mechanism': 'PLAIN',
            'sasl_plain_username': username,
            'sasl_plain_password': password,
        })

    return KafkaProducer(**config)


# 创建 AdminClient
def create_admin_client(bootstrap_servers, username=None, password=None):
    if not bootstrap_servers:
        raise ValueError("bootstrap_servers must be a non-empty string")

    config = {
        'bootstrap_servers': bootstrap_servers,
    }

    if username is not None and password is not None:
        config.update({
            'security_protocol': 'SASL_PLAINTEXT',
            'sasl_mechanism': 'PLAIN',
            'sasl_plain_username': username,
            'sasl_plain_password': password,
        })

    return KafkaAdminClient(**config)


def get_consumer_speed_and_lag(bootstrap_servers, topic_name, group_id,
                               username=None, password=None, sampling_interval=3.0, max_speed_entries=20, **kwargs):
    """
        Monitor Kafka topic consumer lag and speed.
        https://medium.com/@satadru1998/monitoring-kafka-topic-consumer-lag-efficiently-using-python-airflow-435e9651c4f1
    """
    # 创建一个Kafka消费者实例
    consumer = create_consumer_client(bootstrap_servers=bootstrap_servers, group_id=group_id, username=username, password=password)
    consumer.subscribe([topic_name])

    # 获取指定主题的可用分区
    partitions = consumer.partitions_for_topic(topic_name)
    logger.info(f"Partitions: {partitions}")

    # 为每个分区创建一个TopicPartition实例的列表
    topic_partitions = [TopicPartition(topic_name, partition) for partition in partitions]

    last_partition_offsets = {}
    speed_list = defaultdict(list)
    try:
        while True:
            time.sleep(sampling_interval)
            logger.debug("")
            # 获取由broker存储的每个分区的最后偏移量
            topic_partition_last_offset = consumer.end_offsets(topic_partitions)
            logger.debug(topic_partition_last_offset)

            # Loop through each partition and calculate lag
            for tp in topic_partitions:
                # 获取消费者对当前分区提交的偏移量
                consumer_committed_offset = consumer.committed(tp) or 0

                # 获取broker在当前分区存储的最后偏移量
                last_broker_offset = topic_partition_last_offset[tp]

                # 计算当前分区的滞后
                lag = last_broker_offset - consumer_committed_offset

                pre_committed_offset = last_partition_offsets.get(tp)
                last_partition_offsets[tp] = consumer_committed_offset
                if pre_committed_offset is None:
                    continue
                consumer_speed = (consumer_committed_offset - pre_committed_offset) / sampling_interval
                speed_list[tp].append(consumer_speed)
                # Keep only the last max_speed_entries speed entries
                if len(speed_list[tp]) > max_speed_entries:
                    speed_list[tp] = speed_list[tp][-max_speed_entries:]
                max_seed = max(speed_list[tp])
                left_seconds = int(lag / (max_seed + 1))

                # Print information about the current partition's lag
                logger.info(f"Topic: {topic_name} - Partition: {tp.partition} - Current Consumer Offset: {consumer_committed_offset} -  Last Offset: {last_broker_offset} - Lag : {lag} - Consumer Speed: {consumer_speed} m/s, Max Speed: {max_seed} m/s, Left Seconds: {left_seconds} s")
                # messages per second (m/s)
    except Exception as e:
        logger.error(f"Error while monitoring Kafka consumer: {e}")
        raise
    finally:
        if consumer is not None:
            consumer.close()


# 查看某个消费者组详情
def get_consumer_group_details(bootstrap_servers, group_id=None, username=None, password=None, **kwargs):
    admin_client = create_admin_client(bootstrap_servers=bootstrap_servers, username=username, password=password)
    group_description = admin_client.describe_consumer_groups([group_id])[0]
    logger.info(f"Group ID: {group_id}, State: {group_description.state}, Protocol Type: {group_description.protocol_type}, Protocol: {group_description.protocol}, Members: {len(group_description.members)}")
    for member in group_description.members:
        logger.info(f"Group ID: {group_id}, Member ID: {member.member_id}, Client ID: {member.client_id}, Client Host: {member.client_host} Topic: {member.member_assignment.assignment}")
    admin_client.close()


# 查看某个topic下存在哪些消费者组以及每个消费组的详情
def get_consumer_group_details_by_topic(bootstrap_servers, topic_name=None, username=None, password=None, **kwargs):
    """
    需要权限ListGroupsRequest
    """
    # 创建 AdminClient
    admin_client = create_admin_client(bootstrap_servers=bootstrap_servers, username=username, password=password)
    topic_consumer_groups = {}
    try:
        consumer_groups = admin_client.describe_consumer_groups(
            group_ids=[
                group_id
                for group_id, _ in admin_client.list_consumer_groups()
            ]
        )

        for desc_group in consumer_groups:
            if len(desc_group.members) > 0 and desc_group.members[0].member_metadata.subscription[0] == topic_name:
                topic_consumer_groups[desc_group.group] = desc_group
    except Exception as e:
        logger.error(f"Error getting consumer group details: {e}")
        raise
    finally:
        if admin_client is not None:
            admin_client.close()

    logger.info(f"Topic: {topic_name} 下的消费组详情, 共 {len(topic_consumer_groups)} 个消费组:")
    for desc_group in topic_consumer_groups.values():
        logger.info(f"  消费组名称: {desc_group.group}, 状态: {desc_group.state}, 协议类型: {desc_group.protocol_type}, 均衡算法: {desc_group.protocol}, 成员数量: {len(desc_group.members)}")
        for member in desc_group.members:
            logger.info(f"      Member ID: {member.member_id}, Client ID: {member.client_id}, Client Host: {member.client_host} Topic: {member.member_assignment.assignment}")
    return topic_consumer_groups


# 查看某个topic的详细信息
def get_topic_details(bootstrap_servers, topic_name, username=None, password=None, **kwargs):
    admin_client = create_admin_client(bootstrap_servers=bootstrap_servers, username=username, password=password)
    desc_topic = admin_client.describe_topics([topic_name])[0]
    partitions = desc_topic.get('partitions')
    partitions = sorted(partitions, key=lambda x: x.get('partition'))
    for partition in partitions:
        logger.info(f"Partition ID: {partition.get('partition')}, Leader: {partition.get('leader')}, Replicas: {partition.get('replicas')}, ISR: {partition.get('isr')}")
    admin_client.close()


def send_message(bootstrap_servers, topic_name, message="Hello World! Hello kafka!", key=None, partition=None,
                 headers=None, timestamp_ms=None, username=None, password=None, **kwargs):
    producer = create_producer_client(bootstrap_servers=bootstrap_servers, username=username, password=password)
    # msg = json.dumps(message, ensure_ascii=False).encode()
    if headers is None:
        headers = [("Header Key", b"Header Value")]
    if key is None:
        key = "Simple key"

    # messages_and_futures = [] # [(message, produce_future),]
    futures = []
    future = producer.send(topic_name, value=message, key=key, partition=partition, headers=headers, timestamp_ms=timestamp_ms)
    # messages_and_futures.append((message, future))
    futures.append(future)

    ret = [f.get(timeout=30) for f in futures]
    print(f"produce message {message} success. {ret}")
    producer.close()


def consume_messages(bootstrap_servers, topic_name, group_id, username=None, password=None, **kwargs):
    consumer = create_consumer_client(bootstrap_servers=bootstrap_servers, group_id=group_id, username=username, password=password)
    consumer.subscribe([topic_name])
    for message in consumer:
        timestamp_str = datetime.fromtimestamp(message.timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"Topic:[{message.topic}] Partition:[{message.partition}] Offset:[{message.offset}] timestamp:[{message.timestamp} ({timestamp_str})] Key:[{message.key}] Headers:[{message.headers}] value:[{message.value}]")


def demo(*args, **kwargs):
    bootstrap_servers = kwargs.get('bootstrap_servers')
    topic_name = kwargs.get('topic_name')
    group_id = kwargs.get('group_id')
    username = kwargs.get('username')
    password = kwargs.get('password')
    sampling_interval = kwargs.get('sampling_interval')

    get_topic_details(bootstrap_servers, topic_name, username=username, password=password)
    get_consumer_group_details(bootstrap_servers, group_id, username=username, password=password)
    get_consumer_group_details_by_topic(bootstrap_servers, topic_name, username=username, password=password)
    get_consumer_speed_and_lag(bootstrap_servers, topic_name, group_id, username=username, password=password, sampling_interval=sampling_interval)


def sasl_demo():
    # SASL_PLAINTEXT
    bootstrap_servers = ["127.0.0.1:9092"]
    username = ""
    password = ""
    topic = "test"
    group = "group_yunfan"

    # get_topic_details(bootstrap_servers, topic_name=topic, username=username, password=password)
    get_consumer_group_details(bootstrap_servers, group_id=group, username=username, password=password)
    # get_consumer_group_details_by_topic(bootstrap_servers, topic_name=topic, username=username, password=password)
    # get_consumer_speed_and_lag(bootstrap_servers, topic, group, sampling_interval=5, username=username, password=password)


def main():
    function_map = {
        'speed_and_lag': get_consumer_speed_and_lag,
        'group_details': get_consumer_group_details,
        'group_details_by_topic': get_consumer_group_details_by_topic,
        'topic_details': get_topic_details,
        'send_message': send_message,
        'consume_messages': consume_messages,
        'demo': demo,
    }
    parser = argparse.ArgumentParser(description='Kafka tool script.')
    parser.add_argument('--function', type=str, required=True, help='Function to run')
    parser.add_argument('--bootstrap_servers', type=str, required=True, help='Bootstrap servers')
    parser.add_argument('--topic', type=str, help='Topic name')
    parser.add_argument('--group_id', type=str, help='Group ID')
    parser.add_argument('--sampling_interval', type=float, default=5.0, help='Sampling interval')
    parser.add_argument('--username', type=str, help='Username for SASL_PLAINTEXT')
    parser.add_argument('--password', type=str, help='Password for SASL_PLAINTEXT')
    parser.add_argument('-m', '--message', type=str, help='Message to send')

    args = parser.parse_args()

    bootstrap_servers = args.bootstrap_servers.split(',')
    topic = args.topic
    group_id = args.group_id
    sampling_interval = args.sampling_interval
    username = args.username
    password = args.password
    message = args.message

    function_to_run = function_map.get(args.function)
    if function_to_run is None:
        raise ValueError(f"Unknown function: {args.function}")
    function_to_run(bootstrap_servers=bootstrap_servers, topic_name=topic, group_id=group_id, username=username, password=password, sampling_interval=sampling_interval, message=message)
    return
    # if args.function == 'get_consumer_speed_and_lag':
    #     get_consumer_speed_and_lag(bootstrap_servers, topic, group_id, username=username, password=password, sampling_interval=sampling_interval)
    # elif args.function == 'get_consumer_group_details':
    #     get_consumer_group_details(bootstrap_servers, group_id, username=username, password=password )
    # elif args.function == 'get_consumer_group_details_by_topic':
    #     get_consumer_group_details_by_topic(bootstrap_servers, topic, username=username, password=password)
    # elif args.function == 'get_topic_details':
    #     get_topic_details(bootstrap_servers, topic, username=username, password=password)
    # else:
    #     print(f"Unknown function: {args.function}")
    #
    # exit(1)


if __name__ == "__main__":
    # Kafka配置
    kafka_servers = ["127.0.0.1:9092"]
    topic = 'fjp_test_topic'
    group = 'fjp_test_group'

    # get_consumer_speed_and_lag(kafka_servers, topic, group, sampling_interval=2)
    # get_consumer_group_details(kafka_servers, group_id=group)
    # get_consumer_group_details_by_topic(kafka_servers, topic_name=topic)
    # get_topic_details(kafka_servers, topic)
    # send_message(bootstrap_servers=kafka_servers, topic_name=topic)
    # send_message(bootstrap_servers=kafka_servers, topic_name=topic, message={"fjp": "test"})
    # consume_messages(bootstrap_servers=kafka_servers, topic_name=topic, group_id='fjp_test_group')

    # sasl_demo()
    main()
    # py3 fjp_kafka_tool.py --bootstrap_servers 127.0.0.1:9092 --function demo --topic aa-test-production-cdm-data --group_id test_consume_dlb_checker
    # python3 fjp_kafka_tool.py --bootstrap_servers 127.0.0.1:9092 --function demo --topic fjp_test_topic --group_id fjp_test_group
