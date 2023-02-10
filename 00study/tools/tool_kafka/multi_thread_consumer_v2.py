import logging
import threading
import time
from kafka import KafkaConsumer

logger = logging.getLogger(__name__)


class Consumer(threading.Thread):
    def __init__(self, topic, group_id, bootstrap_servers):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.topic = topic
        self.group_id = group_id
        self.bootstrap_servers = bootstrap_servers
        self.consumer = KafkaConsumer(
            self.topic, group_id=self.group_id, bootstrap_servers=self.bootstrap_servers
        )

    def stop(self):
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            for message in self.consumer:
                # Do something with the message, such as processing and storing it
                print(message.value)

                if self.stop_event.is_set():
                    break


if __name__ == '__main__':
    topic = "test"
    group_id = "my_group"
    bootstrap_servers = ["localhost:9092"]
    num_threads = 4

    consumers = [
        Consumer(topic, group_id, bootstrap_servers) for _ in range(num_threads)
    ]
    for consumer in consumers:
        consumer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for consumer in consumers:
            consumer.stop()

    for consumer in consumers:
        consumer.join()
