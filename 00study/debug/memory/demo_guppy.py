import guppy
from guppy import hpy


def demo_guppy():
    hp = hpy()
    before = hp.heap()
    # critical section here

    after = hp.heap()
    leftover = after - before
    print(leftover)
    import pdb;
    pdb.set_trace()
    # leftover
    # leftover.byrcs[0].byid


def use_guppy():
    # init heapy
    heapy = guppy.hpy()

    # Print memory statistics
    def update():
        print(heapy.heap())

    # Print relative memory consumption since last sycle
    def update():
        print(heapy.heap(), heapy.setref())

    # Print relative memory consumption w/heap traversing
    def update():
        print(heapy.heap().get_rp(40))
        heapy.setref()


if __name__ == '__main__':
    demo_guppy()
