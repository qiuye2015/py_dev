import threading
import queue

"""
方案一
"""


def my_thread_function(queue):
    try:
        # Thread code that may raise an exception
        raise ValueError("An error occurred in the thread")
    except Exception as e:
        # Put the exception into the queue
        queue.put(e)


def demo1():
    # Create a queue to store the exception
    exception_queue = queue.Queue()

    # Create and start the thread
    t = threading.Thread(target=my_thread_function, args=(exception_queue,))
    t.start()

    # Wait for the thread to finish
    t.join()

    # Check if there is an exception in the queue
    if not exception_queue.empty():
        # Get the exception from the queue
        exception = exception_queue.get()
        # Handle the exception in the caller thread
        print(f"Exception in thread: {exception}")


def demo2():
    import concurrent.futures

    def task1():
        # Thread 1 code
        raise ValueError("Error in thread 1")

    def task2():
        # print("======")
        # return 666
        # Thread 2 code
        raise RuntimeError("Error in thread 2")

    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix="fjp") as executor:
        # Submit the tasks to the executor
        futures = [executor.submit(task1), executor.submit(task2)]
        # Wait for the threads to finish and handle exceptions
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                print(result, "++++")

            except Exception as e:
                # Handle the exception for each thread separately
                if future == futures[0]:
                    print(f"Exception in thread 1: {e}")
                elif future == futures[1]:
                    print(f"Exception in thread 2: {e}")

        print("save======")


if __name__ == '__main__':
    demo2()
