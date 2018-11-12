import abc

class DataGenerator(abc.ABC):

    @abc.abstractmethod
    def run(self):
        pass