from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import logging
import time


def wtp_send(d):
    print(f"{d}, before")
    time.sleep(3)
    print(f"{d}, after")


all_tasks = []
with ThreadPoolExecutor(2) as executor:
    for data in [1, 2, 3]:
        all_tasks.append(executor.submit(wtp_send, data))

    print("wait before")
    wait(all_tasks, return_when=ALL_COMPLETED)
    print("wait after")

print("end")
