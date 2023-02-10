import threading
import logging
import time
from kafka import KafkaConsumer

logger = logging.getLogger(__name__)


class Consumer(threading.Thread):
    daemon = True

    def __init__(self, topic, group_id, bootstrap_servers):
        threading.Thread.__init__(self)
        self.topic = topic
        self.group_id = group_id
        self.bootstrap_servers = bootstrap_servers
        self.consumer = KafkaConsumer(
            self.topic, group_id=self.group_id, bootstrap_servers=self.bootstrap_servers
        )

    def run(self):
        while True:
            for message in self.consumer:
                # do something with the message
                print(message.value)


if __name__ == '__main__':
    topic = "test"
    group_id = "my_group"
    bootstrap_servers = ["localhost:9092"]

    threads = [Consumer(topic, group_id, bootstrap_servers) for _ in range(4)]
    for thread in threads:
        thread.start()

    time.sleep(100)
