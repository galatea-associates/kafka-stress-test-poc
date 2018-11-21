from multiprocessing import Lock, Value

class Counter(object):
    def __init__(self, init_val=0, limit_val=0):
        self.__val = Value('i', init_val)
        self.__limit = limit_val
        self.__lock = Lock()

    def value(self):
        with self.__lock:
            return self.__val.value

    def reset(self):
        with self.__lock:
            self.__val.value = 0

    def check_value_and_increment(self):
        with self.__lock:
            value_beneath_limit = self.__val.value < self.__limit
            if value_beneath_limit:
                self.__val.value += 1
            return value_beneath_limit