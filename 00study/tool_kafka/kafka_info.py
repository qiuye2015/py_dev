from kafka import KafkaConsumer
from kafka.structs import TopicPartition
import time

bootstrap_servers = ['localhost:9092']
topic = "test_py_client"
group_id = "group2"

consumer = KafkaConsumer(topic, group_id=group_id,
                         bootstrap_servers=bootstrap_servers)
print("all topics is {}".format(consumer.topics()))
print("partitions of this {} is {}".format(
    topic, consumer.partitions_for_topic(topic)))

partitions = [
    TopicPartition(topic, p) for p in consumer.partitions_for_topic(topic)
]
print("TopicPartition:", partitions)

old = 0
while 1:
    toff = consumer.end_offsets(partitions)
    toff = [(key.partition, toff[key], key) for key in toff.keys()]
    toff.sort()
    for p in toff:
        cur = consumer.committed(p[2])
        if not cur:
            cur = 0
        if p[0] == 0:
            newLeft = p[1] - cur
            print(
                '------partition:{}, left:{}, new add {}'.format(p[0], p[1] - cur, newLeft - old))
            old = newLeft
        print('partition:{}, left:{}'.format(p[0], p[1] - cur))

    time.sleep(20)
