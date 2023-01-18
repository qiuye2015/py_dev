# example of logging to file from multiple threads
from random import random
from time import sleep
from threading import Thread
import logging


# task to be executed by worker threads
def task(threshold):
    logging.info(f'Thread starting.')
    # simulate doing work
    for i in range(5):
        # generate value
        value = random()
        # log all values generated
        logging.debug(f'Thread got {value}.')
        # block
        sleep(value)
        # check if is a problem
        if value < threshold:
            logging.warning(f'Thread value less than {threshold}, stopping.')
            break
    logging.info(f'Thread completed successfully.')


# configure log handler to report all messages to file with thread names
handler = logging.FileHandler('application2.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('[%(levelname)s] %(name)s: [%(threadName)s] %(message)s'))
# set the new log handler
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# start the threads
threads = [Thread(target=task, args=(0.1,)) for i in range(5)]
# start threads
for thread in threads:
    thread.start()
# wait for threads to finish
for thread in threads:
    thread.join()