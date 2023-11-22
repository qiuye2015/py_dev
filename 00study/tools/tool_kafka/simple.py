from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import sys
import threading
import time
from typing import List

from kafka import KafkaProducer
from loguru import logger

# Kafka 服务器地址和主题名
BOOTSTRAP_SERVERS = "localhost:9092"  # 替换成你的 Kafka 服务器地址
SASL_PLAIN_USERNAME = ""
SASL_PLAIN_PASSWORD = ""
TOPIC = "million_data_producer_topic"  # 替换成你的 Kafka 主题名

###
_g_kafka_producer = None
_lock = threading.Lock()


def get_kafka_producer(bootstrap_servers=BOOTSTRAP_SERVERS):
    global _g_kafka_producer
    with _lock:
        if not _g_kafka_producer:
            _g_kafka_producer = KafkaMsgProducer(bootstrap_servers=bootstrap_servers)
            _g_kafka_producer.connect()
    return _g_kafka_producer


def get_default_config():
    return {
        "bootstrap_servers": BOOTSTRAP_SERVERS.split(","),
        "security_protocol": "PLAINTEXT",
        "sasl_mechanism": "PLAIN",
        "sasl_plain_username": SASL_PLAIN_USERNAME,
        "sasl_plain_password": SASL_PLAIN_PASSWORD,
    }


class KafkaMsgProducer:
    def __init__(self, bootstrap_servers=None, config=None):
        self.producer = None
        self.bootstrap_servers = bootstrap_servers
        self.config = config

    def connect(self):
        if self.producer is None:
            if not self.config:
                producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
            else:
                producer = KafkaProducer(**self.config)
            self.producer = producer
            print(producer.metrics())
        return self

    def send(
            self,
            topic,
            msg,
            auto_flush=False,
            key=None,
            headers=None,
            partition=None,
            timestamp_ms=None,
    ):
        if self.producer is not None:
            if not isinstance(msg, bytes):
                msg = msg.encode("utf-8")
            if key and not isinstance(key, bytes):
                key = key.encode("utf-8")

            if auto_flush:
                self.producer.send(
                    topic=topic,
                    value=msg,
                    key=key,
                    headers=headers,
                    partition=partition,
                    timestamp_ms=timestamp_ms,
                )
                logger.debug(f"==>send to topic={topic}, msg={msg}, key={key}")
                self.producer.flush()
            else:
                self.producer.send(
                    topic=topic,
                    value=msg,
                    key=key,
                    headers=headers,
                    partition=partition,
                    timestamp_ms=timestamp_ms,
                ).add_callback(self.on_send_success, msg).add_errback(self.on_send_error, msg)

    def async_send(self, topic, msg, key=None):
        self.send(topic=topic, msg=msg, key=key, auto_flush=False)

    def syn_send(self, topic, msg, key=None):
        self.send(topic=topic, msg=msg, key=key, auto_flush=True)

    def close(self):
        if self.producer:
            self.producer.close()
        else:
            logger.warning("producer is none, not need to close")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, t, v, traceback):
        self.close()

    @staticmethod
    def on_send_success(msg, record_metadata):
        logger.info(f"message send to topic: {record_metadata.topic} of partition: {record_metadata.partition} at offset: {record_metadata.offset} at time: {record_metadata.timestamp}, msg={msg}")

    @staticmethod
    def on_send_error(msg_key, excp):
        logger.error("Message: {} delivery failed: {}".format(msg_key, excp))


def send_message(bootstrap_servers: List[str], topic: str, msg: str):
    with KafkaMsgProducer(bootstrap_servers=bootstrap_servers) as producer:
        logger.info(f"send kafka msg, topic={topic}, msg={msg}")
        producer.send(topic, msg, auto_flush=True)


def main(max_workers=32, debug=True):
    logger.debug(f"debug={debug}")
    # 生成 1000000 条数据
    data = [f"Message {i}" for i in range(1000000)]

    try:
        task_queue = Queue(maxsize=max_workers)
        futures = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for idx in range(0, len(data)):  # 批量大小为 1000 条消息
                item = data[idx]
                key = item
                task_queue.put(None)  # 等待队列中有空位
                if debug:
                    # get_kafka_producer().send(topic=TOPIC, msg=item, auto_flush=False)
                    get_kafka_producer().async_send(topic=TOPIC, msg=item, key=key)
                    task_queue.get()  # 任务已提交，从队列中移除一个元素
                    continue
                future = executor.submit(get_kafka_producer().async_send, TOPIC, item, key)
                future.add_done_callback(lambda x: task_queue.get())  # 任务完成后，从队列中移除一个元素
                # futures.append(future)
                # for future in futures:
                #     try:
                #         future.result()
                #     except Exception as e:
                #         logger.error(f'Producer error: {e}')
    except Exception as e:
        logger.error(f"Producer error: {e}")
    finally:
        get_kafka_producer().close()


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")

    start = time.time()
    main(debug=False)
    print(f"Total time taken: {time.time() - start} seconds")
