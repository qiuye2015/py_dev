from collections import Counter
import linecache
import os
from time import sleep
import tracemalloc


def display_top(snapshot, key_type='lineno', limit=3):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB" % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


def count_prefixes():
    sleep(2)  # Start up time.
    counts = Counter()
    fname = '/Users/leo.fu1/workspace/github/icoding/py_dev/00study/debug/memory/pprof.py'
    with open(fname) as words:
        words = list(words)
        for word in words:
            prefix = word[:3]
            counts[prefix] += 1
            sleep(0.0001)
    most_common = counts.most_common(3)
    sleep(3)  # Shut down time.
    return most_common


def demo_tracemalloc():
    tracemalloc.start()

    most_common = count_prefixes()
    print('Top prefixes:', most_common)

    snapshot = tracemalloc.take_snapshot()
    display_top(snapshot)


###########
from queue import Empty, Queue
from datetime import datetime
from resource import getrusage, RUSAGE_SELF
from threading import Thread


def memory_monitor(command_queue: Queue, poll_interval=1):
    tracemalloc.start()
    old_max = 0
    snapshot = None
    while True:
        try:
            command_queue.get(timeout=poll_interval)
            if snapshot is not None:
                print(datetime.now())
                display_top(snapshot)
            return
        except Empty:
            max_rss = getrusage(RUSAGE_SELF).ru_maxrss
            if max_rss > old_max:
                old_max = max_rss
                snapshot = tracemalloc.take_snapshot()
                # print(datetime.now(), 'max RSS', max_rss)
                print(datetime.now(), 'max RSS', f"{max_rss / 1024 / 1024:.2f}", 'MB')


def demo_thread_monitor():
    queue = Queue()
    poll_interval = 0.1
    monitor_thread = Thread(target=memory_monitor, args=(queue, poll_interval))
    monitor_thread.start()
    try:
        most_common = count_prefixes()
        print('Top prefixes:', most_common)
    finally:
        queue.put('stop')
        monitor_thread.join()


if __name__ == '__main__':
    demo_thread_monitor()
