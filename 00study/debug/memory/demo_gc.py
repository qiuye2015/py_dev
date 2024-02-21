def demo_gc():
    from collections import defaultdict
    from gc import get_objects

    before = defaultdict(int)
    after = defaultdict(int)

    for i in get_objects():
        before[type(i)] += 1

    leaked_things = [[x] for x in range(10)]

    for i in get_objects():
        after[type(i)] += 1

    print([(k, after[k] - before[k]) for k in after if after[k] - before[k]])


def show_memory():
    import gc
    import sys
    print("*" * 60)

    objects_list = []
    for obj in gc.get_objects():
        size = sys.getsizeof(obj)
        objects_list.append((obj, size))

    sorted_values = sorted(objects_list, key=lambda x: x[1], reverse=True)
    for obj, size in sorted_values[:10]:
        print(f"OBJ: {id(obj)}, "
              f"TYPE: {type(obj)}, "
              f"SIZE: {size / 1024 / 1024:.2f}MB, "
              f"REPR: {str(obj)[:100]}")
    # 返回直接引用任意一个 ojbs 的对象列表
    # gc.get_referrers(objs)
    print("*" * 60)


def dump_garbage():
    """
    show us what's the garbage about
    """
    import gc
    # force collection
    print("\nGARBAGE:")
    gc.collect()

    print("\nGARBAGE OBJECTS:")
    for x in gc.garbage:
        s = str(x)
        if len(s) > 80:
            s = s[:80]
        print(type(x), "\n  ", s)


def demo_dump_garbage():
    import gc
    gc.enable()
    gc.set_debug(gc.DEBUG_LEAK)
    # make a leak
    l = []
    l.append(l)
    del l

    # show the dirt ;-)
    dump_garbage()


if __name__ == '__main__':
    demo_gc()  # [(<class 'list'>, 11)]
    show_memory()
    demo_dump_garbage()
