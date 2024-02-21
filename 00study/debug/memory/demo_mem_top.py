def demo_mem_top():
    from mem_top import mem_top
    # From time to time:
    # logging.debug(mem_top())
    print(mem_top())
    # Notice which counters keep increasing over time - they are the suspects.

    # Notice which counters keep increasing over time - they are the suspects.
    # refs - 从此对象到其他对象的直接引用数，例如 dict 的键和值
    # bytes - 此对象的大小（以字节为单位）
    # types — 垃圾回收后仍保留在内存中的此类型的对象数


demo_mem_top()
