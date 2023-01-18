# example of a pipeline with threads and queues
from random import random
from time import sleep
from threading import Thread
from queue import Queue
import logging
import sys


# first task in the pipeline
def task1(queue_out):
    logging.info(f'Started')
    # add items
    for i in range(10):
        # generate a value
        value = random()
        # block to simulate work
        sleep(value)
        # create item
        item = [i, value]
        # add to the queue
        queue_out.put(item)
        # report progress
        logging.info(f'Generated {item}')
    # add signal that we are done
    queue_out.put(None)
    logging.info(f'Done')


# second task in the pipeline
def task2(queue_in, queue_out):
    logging.info(f'Started')
    # process values
    while True:
        # retrieve from queue
        item = queue_in.get()
        # check for stop
        if item is None:
            # pass on message
            queue_out.put(item)
            break
        # generate a value
        value = random()
        # block to simulate work
        sleep(value)
        # add to item
        new_item = item + [value]
        # pass it on
        queue_out.put(new_item)
        # report progress
        logging.info(f'Got {item} generated {new_item}')
    logging.info(f'Done')


# third task in the pipeline
def task3(queue_in):
    logging.info(f'Started')
    # process values
    while True:
        # retrieve from queue
        item = queue_in.get()
        # check for stop
        if item is None:
            break
        logging.info(f'Got {item}')
    logging.info(f'Done')


# configure the log handler
handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('[%(levelname)s] [%(threadName)s] %(message)s'))
# add the log handler
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# create queue between first two tasks
queue1_2 = Queue()
# create thread for first task
thread1 = Thread(target=task1, args=(queue1_2,), name='Task1')
thread1.start()

# create queue between second and third tasks
queue2_3 = Queue()
# create thread for second task
thread2 = Thread(target=task2, args=(queue1_2, queue2_3), name='Task2')
thread2.start()

# create thread for third task
thread3 = Thread(target=task3, args=(queue2_3,), name='Task3')
thread3.start()
# wait for all threads to finish
thread1.join()
thread2.join()
thread3.join()
