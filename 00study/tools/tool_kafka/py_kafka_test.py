from concurrent.futures.thread import ThreadPoolExecutor
import json
import threading

from kafka import KafkaProducer

from ftimes import current_milliseconds
from tools.tool_kafka.conflunet_kafka_test import CountDownLatch


class PyKafkaProducer(object):
    def __init__(self):
        super(PyKafkaProducer, self).__init__()
        self._producer = KafkaProducer(bootstrap_servers='localhost:9092')

    def send_json_msg(self, topic, data: dict):
        key = data.get('type')
        json_value = json.dumps(data)
        self._producer.send(topic, key=key.encode('utf-8'), value=json_value.encode('utf-8'))
        self._producer.flush()


py_kafka_producer = PyKafkaProducer()


def send_new_kafka_msg_v1():
    """
        100 msg  cost: 3242
        1000 msg  cost: 37781
    """
    start_time = current_milliseconds()
    msg = test_dict_data()
    # 预热
    py_kafka_producer.send_json_msg(topic='hc_kafka_test', data=msg)

    type = 'log_manager'
    for i in range(0, 1000):
        msg['type'] = type + '_' + str(i)
        py_kafka_producer.send_json_msg(topic='hc_kafka_test', data=msg)
        print(msg.get('type'))
    end_time = current_milliseconds()
    print('total cost time:{}'.format(end_time - start_time))


def execute_job(msg: dict, count_down_latch: CountDownLatch):
    print("current thread name:{} send msg:{}".format(threading.current_thread().name, msg.get('type')))
    py_kafka_producer.send_json_msg(topic='hc_kafka_test', data=msg)
    count_down_latch.countDown()
    print("current thread name:{} send msg:{} end....".format(threading.current_thread().name, msg.get('type')))


def send_new_kafka_msg_v2():
    """
        100 msg, 10 thread, cost: 460
        1000 msg, 10 thread, cost: 4017
        6000 msg  10 thread, cost: 22901
    """
    start_time = current_milliseconds()
    msg = test_dict_data()
    # 预热
    py_kafka_producer.send_json_msg(topic='hc_kafka_test', data=msg)
    executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix='job_thread')
    count_down_latch = CountDownLatch(6000)
    type = 'snapshot'
    for i in range(0, 6000):
        msg['type'] = type + '_' + str(i)
        new_msg = dict(msg)
        executor.submit(execute_job, new_msg, count_down_latch)
        print(msg.get('type'))
    count_down_latch.wait()
    end_time = current_milliseconds()
    print('total cost time:{}'.format(end_time - start_time))


def test_dict_data():
    meta = {"app_id": 100512, "file_size": 93}
    return meta


if __name__ == "__main__":
    send_new_kafka_msg_v1()
    # send_new_kafka_msg_v2()

    # consumer = KafkaConsumer('my-topic',
    #                          group_id='my-group',
    #                          bootstrap_servers=['localhost:9092'])
