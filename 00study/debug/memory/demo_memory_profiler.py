import gc

from memory_profiler import memory_usage


def memory_used(func, *args, **kwargs):
    """Compute memory usage of func."""
    if memory_usage is None:
        return None

    gc.collect()
    mem_use = memory_usage((func, args, kwargs), interval=.001)

    return max(mem_use) - min(mem_use)

# memory_used()
