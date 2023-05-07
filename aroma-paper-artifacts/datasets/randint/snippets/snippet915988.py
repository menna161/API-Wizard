from __future__ import print_function
import random
import Queue
import threading
import time

if (__name__ == '__main__'):

    class MyJob():

        def __init__(self, id, countdown):
            self.cntdwn = countdown
            self.myid = id

        def __call__(self):
            with glck:
                print(('[Job] ID: %s Starts.' % str(self.myid)))
            while (self.cntdwn >= 0):
                with glck:
                    print(('[Job] ID: %s, CountDown: %d' % (str(self.myid), self.cntdwn)))
                self.cntdwn -= 1
                time.sleep(1.0)
            with glck:
                print(('[Job] ID: %s Ends.' % str(self.myid)))
    wp = WorkPool()
    wp.start()
    glck = threading.Lock()
    random.seed()
    for i in range(50):
        j = MyJob(i, random.randint(1, 10))
        wp.append_job(j)
    dj = set()
    while (len(dj) < 50):
        r = wp.retrieve_job()
        if (None == r):
            time.sleep(0.5)
            continue
        dj.add(r.myid)
    print('[Main] All job done. Joining work pool...')
    wp.join()
    print('[Main] Work pool has joined.')
