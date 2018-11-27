from multiprocessing import Lock, Value

class Counter(object):
    def __init__(self, init_val=0, limit_val=0):
        self.__val = Value('i', init_val)
        self.__limit = limit_val

    def increment(self):
        with self.__val.get_lock():
            self.__val.value += 1

    def value(self):
        with self.__val.get_lock():
            return self.__val.value

    def reset(self):
        with self.__val.get_lock():
            self.__val.value = 0

    def check_value_and_increment(self):
        with self.__val.get_lock():
            value_beneath_limit = self.__val.value < self.__limit
            if value_beneath_limit:
                self.__val.value += 1
            return value_beneath_limit