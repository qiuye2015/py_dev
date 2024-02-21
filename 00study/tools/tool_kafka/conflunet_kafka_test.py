from concurrent.futures.thread import ThreadPoolExecutor
import json
import threading
from threading import Condition

from confluent_kafka.cimpl import Producer
from pydantic import BaseModel

from ftimes import current_milliseconds


class FileMsg(BaseModel):
    uuid: str = None


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}] at append time:{}'.format(msg.topic(), msg.partition(), msg.timestamp()))


class CountDownLatch:
    def __init__(self, count):
        self.count = count
        self.condition = Condition()

    def wait(self):
        try:
            self.condition.acquire()
            while self.count > 0:
                self.condition.wait()
        finally:
            self.condition.release()

    def countDown(self):
        try:
            self.condition.acquire()
            self.count -= 1
            self.condition.notifyAll()
        finally:
            self.condition.release()


class MsgProducer(object):
    def __init__(self):
        super(MsgProducer, self).__init__()
        self._producer = Producer({
            'bootstrap.servers': 'localhost:9092',
            'client.id': 'test',
            "retries": 3
        })

    def send_json_msg(self, topic, data: dict):
        key = data.get('type')
        json_value = json.dumps(data)
        self._producer.produce(topic, key=key, value=json_value.encode('utf-8'), on_delivery=delivery_report)
        self._producer.flush()

    def flush_msg(self):
        self._producer.flush()


msg_test_producer = MsgProducer()


def execute_job(msg: dict, count_down_latch: CountDownLatch):
    print("current thread name:{} send msg:{}".format(threading.current_thread().name, msg.get('type')))
    msg_test_producer.send_json_msg(topic='hc_kafka_test', data=msg)
    count_down_latch.countDown()
    print("current thread name:{} send msg:{} end....".format(threading.current_thread().name, msg.get('type')))


def send_kafka_msg():
    """
        100 msg  thread 5  cost:4301
        100 msg  thread 10  cost:3809
        1000 msg  thread 10  cost:41093
        6000 msg  thread 10  cost:224127
    """
    msg = test_dict_data()
    # 预热
    msg_test_producer.send_json_msg(topic='hc_kafka_test', data=msg)

    executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix='job_thread')
    count_down_latch = CountDownLatch(6000)
    start_time = current_milliseconds()
    msg = test_dict_data()
    type = 'log_manager'
    for i in range(0, 6000):
        msg['type'] = type + '_' + str(i)
        new_msg = dict(msg)
        executor.submit(execute_job, new_msg, count_down_latch)
        print(msg.get('type'))
    count_down_latch.wait()
    end_time = current_milliseconds()
    print('total cost time:{}'.format(end_time - start_time))


def test_dict_data():
    meta = {"app_id": 4455, "vehicle_id": "1234", "type": "ll",
            "request_id": "mk-2222-H0BwAOechw", "request_time": 1652160632,
            "file_size": 93}
    return meta


if __name__ == "__main__":
    send_kafka_msg()
