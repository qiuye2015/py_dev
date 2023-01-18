# example of stopping daemon thread background task at exit
from time import sleep
from threading import Thread
from threading import Event
import atexit


# background task
def task(event):
    # run forever
    while not event.is_set():
        # run every 2 seconds
        sleep(2)
        # perform task
        print('Background performing task')
    print('Background done')


# stop the background task gracefully before exit
def stop_background(stop_event, thread):
    print('At exit stopping')
    # request the background thread stop
    stop_event.set()
    # wait for the background thread to stop
    thread.join()
    print('At exit done')


# prepare state for stopping the background
stop_event = Event()
# create and start the background thread
thread = Thread(target=task, args=(stop_event,), daemon=True, name="Background")
thread.start()

# register the at exit
atexit.register(stop_background, stop_event, thread)
# run the main thread for a while
print('Main thread running...')
sleep(10)
print('Main thread stopping')
