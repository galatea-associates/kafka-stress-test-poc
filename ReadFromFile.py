import csv
import os
import pandas as pd
from DataGenerator import DataGenerator
from multiprocessing import Lock

class ReadFromFile(DataGenerator):
    def __init__(self):
        self.__file_reader = None
        self.__lock = Lock()

    def __setup_file_reader(self, file, chunksize):
        self.__file_reader = pd.read_csv(file, chunksize=chunksize, low_memory=False)

    def __get_next_chunk(self):
        with self.__lock:
            self.__file_reader.get_chunk().to_dict(orient='records')

    def __is_EOF(self):
        return False

    # In DataConfiguration.py, 'Data Args' field should look like:
    # {'File': './out/prices.csv',
    #  'Format' : 'CSV',
    #  'Chunk Size': 1,
    #  'Loop on end': True}
    def run(self, args):
        with self.__lock:
            if self.__setup_file_reader is None:
                self.__setup_file_reader(file=args["File"], chunksize=args["Chunk Size"])
            if self.__is_EOF():
                if args["Loop on end"]:
                    self.__setup_file_reader(file=args["File"], chunksize=args["Chunk Size"])
                else:
                    return None

        return self.__get_next_chunk()

    