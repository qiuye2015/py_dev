import logging
import signal
import json
import time

from abc import abstractmethod
from kafka import KafkaConsumer


class ConsumerWorkerInf(object):
    def __init__(self, consumer):
        self._running = False
        self._consumer = consumer

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, *args):
        logging.info('got signal: {}. Consumer will exit.'.format(signum))
        self._running = False

    def start(self):
        logging.info('start consume message...')
        self._running = True
        while self._running:
            self._consume()

    def join(self):
        self._consumer.close()

    @abstractmethod
    def _process(self, value, **kwargs):
        pass

    def _consume(self):
        records = self._consumer.poll(max_records=1)
        time.sleep(1)
        if len(records) > 0:
            for messages in records.values():
                for message in messages:
                    try:
                        value = message.value.decode('utf-8')
                        topic = message.topic
                        partition = message.partition
                        offset = message.offset
                        # print(message)
                        print("topic", topic, "partition", partition, "offset", offset)
                        # self._process(json.loads(value))
                        self._process(value)
                    except Exception as e:
                        logging.error('msg decode or json loads error: {}'.format(e))
            self._consumer.commit()


def demo_main():
    class TestConsumer(ConsumerWorkerInf):
        def __init__(self, _consumer):
            super().__init__(_consumer)

        def _process(self, value, **kwargs):
            print("****", value, kwargs)

    servers = ["127.0.0.1:9092"]
    topic_name = "test_10_partition"
    group_id = "group_test_2"
    config = {
        'bootstrap_servers': servers,
        'group_id': group_id,
        'enable_auto_commit': False,
        'max_poll_records': 3,
        'session_timeout_ms': 300 * 1000,
        'auto_offset_reset': 'earliest',
    }

    consumer = KafkaConsumer(topic_name, **config)
    topics = consumer.topics()
    print(consumer.config)
    print(topics)
    print(consumer.partitions_for_topic(topic_name))
    # for message in consumer:
    #     print("t=%s,p=%d,o=%d: key=%s value=%s" % (
    #         message.topic, message.partition, message.offset, message.key, message.value))
    # records = consumer.poll(2)
    # print(records)
    c = TestConsumer(consumer)
    c.start()
    c.join()


if __name__ == '__main__':
    demo_main()
