from multiprocessing import Lock, Value

class Counter(object):
    def __init__(self, init_val=0, limit_val=0):
        self.val = Value('i', init_val)
        self.limit = limit_val
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

    def check_value_and_increment(self):
        with self.lock:
            value_beneath_limit = self.val.value < self.limit
            if value_beneath_limit:
                self.val.value += 1
            return value_beneath_limit

    def get_limit(self):
        return self.limit