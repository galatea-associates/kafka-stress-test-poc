# Modified from - https://github.com/WeiTang114/FMQ
import queue as python_queue
from threading import Thread
import _multiprocessing as _mp


class Queue:
    def __init__(self, maxsize=0, spawn_fast=False, slow_queue=None):
        if maxsize <= 0:
            # same as mp.Queue
            maxsize = _mp.SemLock.SEM_VALUE_MAX

        self.mpq = slow_queue
        self.maxsize = maxsize
        self.spawn_fast = spawn_fast
        if spawn_fast:
            self.qq = python_queue.Queue(maxsize=maxsize)
            self._steal_daemon()

    def put(self, item):
        """
        TODO: maybe support "block" and "timeout"
        """
        self.mpq.put(item)

    def get_nowait(self):
        if not self.spawn_fast:
            return None
        return self.qq.get_nowait()

    def get(self):
        if not self.spawn_fast:
            return None
        return self.qq.get()

    def qsize(self):
        """
        can be 2*(maxsize), because this is the sum of qq.size and mpq.size
        """
        if not self.spawn_fast:
            return self.mpq.qsize()
        return self.qq.qsize() + self.mpq.qsize()

    def empty(self):
        if not self.spawn_fast:
            return self.mpq.empty()
        return self.qq.empty() and self.mpq.empty()

    def full(self):
        if not self.spawn_fast:
            return self.mpq.full()
        return self.qq.full() and self.mpq.full()

    def _steal_daemon(self):

        def steal(self):
            while True:
                # block here
                self.qq.put(self.mpq.get())
            print('daemon done')

        # when the FastMyQueue object is GCed, stop the thread
        # by the stop() callback
        stealer = [Thread(target=steal, args=(self,)) for _ in range(1, 3)]
        for steal in stealer:
            steal.daemon = True
            steal.start()
