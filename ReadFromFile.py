import os
from builtins import StopIteration

import pandas as pd
from DataGenerator import DataGenerator

import csv
from multiprocessing import Lock


class ReadFromFile(DataGenerator):
    def __init__(self):
        self.__file_reader = None
        self.__lock = Lock()

    def __setup_file_reader(self, file, chunksize):
        self.__file_reader = pd.read_csv(file, chunksize=chunksize, low_memory=False)

    def __get_next_chunk(self):
        with self.__lock:
            try:
                return self.__file_reader.get_chunk().to_dict(orient='records')

            #If EOF a StopIteration exception occurs
            except StopIteration:
                return None

    # In DataConfiguration.py, 'Data Args' field should look like:
    # {'File': './out/prices.csv',
    #  'Format' : 'CSV',
    #  'Chunk Size': 1,
    #  'Loop on end': True}
    def run(self, args):
        with self.__lock:
            if self.__file_reader is None:
                self.__setup_file_reader(file=args["File"], chunksize=args["Chunk Size"])

        data = self.__get_next_chunk()
        
        #Data will be None if EOF occured
        if data is None:
            if args["Loop on end"]:
                
                #If loop on EOF then start reader again at beginning
                self.__setup_file_reader(file=args["File"], chunksize=args["Chunk Size"])
                data = self.__get_next_chunk()
            else:
                return None

        return data

    