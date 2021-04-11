# coding:utf-8
import threading
import time

# 死锁

mutexA = threading.Lock()
mutexB = threading.Lock()


class MyThread1(threading.Thread):
    def run(self):
        mutexA.acquire()
        #time.sleep(1)
        print(self.name+'A lock')

        mutexB.acquire()
        print(self.name+'A unlock')

        print(self.name+'B lock')
        mutexB.release()
        print(self.name+'B unlock')

        mutexA.release()

class MyThread2(threading.Thread):
    def run(self):
        mutexB.acquire()
        print(self.name+'B lock')
        #time.sleep(1)

        mutexA.acquire()
        print(self.name+'A lock')
        mutexA.release()
        print(self.name+'A unlock')

        mutexB.release()
        print(self.name+'B unlock')


def main():
    t1 = MyThread1()
    t2 = MyThread2()
    t1.start()
    t2.start()


if __name__ == '__main__':
    main()
