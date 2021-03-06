# coding=utf-8

import threading
import time
from time import sleep

class MyData:
    def __init__(self):
        self._locker = threading.Lock()
        self._count = 0
        
    def increase(self):
        self._locker.acquire(True)
        try:
            self._count += 1
        finally:
            self._locker.release()
            
    def getCount(self):
        self._locker.acquire(True)
        try:
            return self._count
        finally:
            self._locker.release()

class MyThread(threading.Thread):
    
    def __init__(self, theId, data):
        super(MyThread, self).__init__()
        self._theId = theId
        self._data = data
    
    def run(self):
        #time.sleep(1)
        for i in range(10000):
            self._data.increase()
            sleep(0.001)
            #print ('the _data is:%s\r' % self._data)
            print ('the thread is:%s, index is: %d\r' % (threading.get_ident(), i))
        print ('the count=' + str(self._data.getCount()))

    def wait(self, timeout):
        self.join(timeout)

if __name__=="__main__":
    
    data = MyData()
    tList = []
    for i in range(5):
        t = MyThread(i, data)
        tList.append(t)
        t.start()
    
    for t in tList:
        t.wait(3000)
        print ('wait ok')
    
    print ('the final count=' + str(data.getCount()))
    
    print ('main thread end!')
