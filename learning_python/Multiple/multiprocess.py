import os
import time
import random
from multiprocessing import Process
from multiprocessing import Pool
import subprocess


#-----------------------------------------------------------------------------------------------
def linux_platform():
    print('Process (%s) start...' % os.getpid())
    pid = os.fork()
    if pid==0:
        print('I am child process (%s) and my parent is %s.' % (os.getpid(),os.getppid()))
    else:
        print('I(%s) just created a child process (%s)' % (os.getpid(),pid))
#-----------------------------------------------------------------------------------------------

def run_proc(name):
    print('Run child process %s(%s)...' % (name,os.getpid()))

def multi_platform():
    print('parent process %s.' % os.getpid())
    p = Process(target=run_proc,args=('test',))
    print('child process will start')
    p.start()
    p.join()
    print('child process end.')

#-----------------------------------------------------------------------------------------------
def long_time_task(name):
    print('Run task %s (%s)' % (name,os.getpid()))
    start = time.time()
    time.sleep(random.random()*3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' %(name,(end-start)))
def pool_platform():
    print('Parent process %s.' % os.getpid())
    p = Pool(5)
    for i in range(5):
        p.apply_async(long_time_task,args=(i,))
    print('waiting for all subprocesss done')
    p.close()
    p.join()
    print('All subprocesses done.')

#-----------------------------------------------------------------------------------------------
def subprocess_test():
    print('$ nslookup www.python.org')
    r = subprocess.call(['nslookup','www.python.org'])
    print('Exit code:',r)
#-----------------------------------------------------------------------------------------------
if __name__ =='__main__':
    #linux_platform()
    #multi_platform()
    #pool_platform()
    subprocess_test()
#-----------------------------------------------------------------------------------------------
