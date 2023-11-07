import concurrent.futures
import datetime
import queue
import random
import signal
import threading
import time
import logging


def current_milliseconds() -> int:
    return int(datetime.datetime.now().timestamp() * 1000)


class ProducerConsumer:
    def __init__(self, num_producers, num_consumers, task_name="Demo"):
        if not isinstance(num_producers, int) or num_producers <= 0:
            raise ValueError("num_producers must be a positive integer.")
        if not isinstance(num_consumers, int) or num_consumers <= 0:
            raise ValueError("num_consumers must be a positive integer.")

        self.queue = queue.Queue()
        self.num_producers = num_producers
        self.num_consumers = num_consumers
        self.task_name = task_name
        self.exit_event = threading.Event()
        self._t = None

        self.logger = logging.getLogger(f"{task_name}Logger")
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        signal.signal(signal.SIGINT, lambda signum, _: self._signal_handler(signum))
        signal.signal(signal.SIGTERM, lambda signum, _: self._signal_handler(signum))

    def _signal_handler(self, signum):
        self.logger.info(f'[{self.task_name}] Handle signal {signum}. ProducerConsumer will be terminated.')
        self.stop()

    def start(self):
        self._event_loop()

    def start_async(self):
        self._t = threading.Thread(target=self._event_loop, daemon=True)
        self._t.start()

    def stop(self):
        if self.exit_event.is_set():
            self.logger.info(f"[{self.task_name}] exit_event has been set.")
            return
        self.exit_event.set()

        if self._t is not None:
            self.logger.info(f"[{self.task_name}] event_loop thread waiting to stop...")
            start_time = current_milliseconds()
            self._t.join()
            time_cost = current_milliseconds() - start_time
            self.logger.info(f"[{self.task_name}] event_loop thread ended! Stop event cost: {time_cost} ms")

    # def _event_loop(self):
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_producers + self.num_consumers) as executor:
    #         producer_futures = [executor.submit(self.producer_task) for _ in range(self.num_producers)]
    #         consumer_futures = [executor.submit(self.consumer_task) for _ in range(self.num_consumers)]
    #
    #         try:
    #             # Wait for all producer tasks to complete
    #             for future in concurrent.futures.as_completed(producer_futures):
    #                 future.result()
    #
    #             # Wait for all consumer tasks to complete
    #             for future in concurrent.futures.as_completed(consumer_futures):
    #                 future.result()
    #
    #             self.logger.info(f"[{self.task_name}] event_loop finish, self.queue.qsize()={self.queue.qsize()}")
    #             # Wait for all items in the queue to be consumed
    #             # self.queue.join()
    #         except Exception as e:
    #             self.logger.error(
    #                 f'[{self.task_name}] self.queue.qsize()={self.queue.qsize()}, Error in task execution: {e}'
    #             )
    #
    #     self.logger.info(f'[{self.task_name}] > Main done.')
    #
    # def producer_task(self):
    #     cnt = 5
    #     while not self.exit_event.is_set() and cnt > 0:
    #         try:
    #             value = random.random() * 5
    #             time.sleep(value)
    #             self.queue.put(value)
    #             self.logger.info(f'[{self.task_name}] Producer produced: {value}')
    #             cnt -= 1
    #         except Exception as e:
    #             self.logger.error(f'[{self.task_name}] Error in producer task: {e}')
    #             break
    #
    #     self.logger.info(f"[{self.task_name}] producer_task Done queue.put")
    #     self.queue.put(None)
    #     # for _ in range(self.num_consumers):
    #     #     self.queue.put(None)
    #
    # def consumer_task(self):
    #     while not self.exit_event.is_set():
    #         try:
    #             value = self.queue.get()
    #             if value is None:
    #                 self.queue.task_done()
    #                 self.queue.put(value)
    #                 self.logger.info(f"[{self.task_name}] consumer_task queue.task_done")
    #                 break
    #             time.sleep(value)
    #             self.logger.info(f'[{self.task_name}] Consumer consumed: {value}')
    #             self.queue.task_done()
    #
    #             # if self.queue.empty():
    #             #     self.logger.info("consumer_task queue.empty")
    #             #     break
    #         except Exception as e:
    #             self.logger.error(f'[{self.task_name}] Error in consumer task: {e}')
    #             break

    def _event_loop(self):
        consumer = threading.Thread(target=self.consumer_manager)
        producer = threading.Thread(target=self.producer_manager)
        consumer.start()
        producer.start()
        producer.join()
        consumer.join()
        self.logger.info(f'[{self.task_name}] >main done.')

    # producer manager task
    def producer_manager(self, parallel=False):
        if not parallel:
            self.producer_task()
        else:
            # create thread pool
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_producers) as executor:
                producer_futures = [executor.submit(self.producer_task) for _ in range(self.num_producers)]
                try:
                    # Wait for all producer tasks to complete
                    for future in concurrent.futures.as_completed(producer_futures):
                        future.result()
                    self.logger.info(
                        f"[{self.task_name}] producer_manager finish, self.queue.qsize()={self.queue.qsize()}"
                    )
                except Exception as e:
                    self.logger.error(
                        f'[{self.task_name}] self.queue.qsize()={self.queue.qsize()}, Error in task execution: {e}'
                    )

        self.queue.put(None)  # put a signal to expect no further tasks
        self.logger.info(f'[{self.task_name}] >producer_manager done.')

    # consumer manager
    def consumer_manager(self):
        # create thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_consumers) as executor:
            consumer_futures = [executor.submit(self.consumer_task) for _ in range(self.num_consumers)]
            try:
                # Wait for all producer tasks to complete
                for future in concurrent.futures.as_completed(consumer_futures):
                    future.result()
                self.logger.info(f"[{self.task_name}] consumer_manager finish, self.queue.qsize()={self.queue.qsize()}")
            except Exception as e:
                self.logger.error(
                    f'[{self.task_name}] self.queue.qsize()={self.queue.qsize()}, Error in task execution: {e}'
                )
        self.logger.info(f'[{self.task_name}] >consumer_manager done.')

    # producer task
    def producer_task(self):
        cnt = 5
        while not self.exit_event.is_set() and cnt > 0:
            value = random.random() * 5
            time.sleep(value)
            # push data into queue
            self.queue.put(value)
            self.logger.info(f'[{self.task_name}] Producer produced: {value}')
            cnt -= 1

    # consumer task
    def consumer_task(self):
        # run until there is no more work
        while not self.exit_event.is_set():
            # retrieve one item from the queue
            value = self.queue.get()
            # check for signal of no more work
            if not value:
                # put back on the queue for other consumers
                self.queue.put(value)
                return  # shutdown
            time.sleep(value)
            self.logger.info(f'[{self.task_name}] Consumer consumed: {value}')


# # 示例用法
# template = ProducerConsumer(num_producers=1, num_consumers=3)
# template.start()
# time.sleep(10)
# template.stop()

if __name__ == '__main__':
    import uuid

    print(uuid.uuid4())
    a = ""
    a = str(uuid.uuid4())
    print(a)
    # from pydantic import BaseModel
    #
    # class Animal(BaseModel):
    #     name: str = None
    #     age: int = None
    #
    # class Dog(Animal):
    #     breed: str = None
    #
    # a = Animal(name="zhangsan", age=12)
    # print(a.json())
    # b = Dog(**a.dict())
    # print(b.json())

    # pydantic.BaseModel 如何实现用父类对象创建子类对象
