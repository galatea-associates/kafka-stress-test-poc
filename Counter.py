from multiprocessing import Lock, Value

class Counter(object):
    def __init__(self, init_val=0):
        self.val = Value('i', init_val)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def value(self):
        with self.lock:
            return self.val.value

    def reset(self):
        with self.lock:
            self.val.value = 0
