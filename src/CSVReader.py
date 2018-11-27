from builtins import StopIteration
import dask.dataframe as dd
from DataGenerator import DataGenerator
from multiprocessing import Lock


class CSVReader(DataGenerator):
    def __init__(self):
        self.__file_reader = None
        self.__lock = Lock()

    def __setup_file_reader(self, file, chunksize):
        self.__file_reader = dd.read_csv(file)

    def convert_to_dict(self, row):
        dict = {}
        for key, value in row.iteritems():
            dict[key] = value
        return dict

    def __get_next_chunk(self):
        with self.__lock:
            return self.__file_reader.head(n=100).to_dict(orient='records')

    # In DataConfiguration.py, 'Data Args' field should look like:
    # {'File': './out/prices.csv',
    #  'Format' : 'CSV',
    #  'Chunk Size': 1,
    #  'Loop on end': True}
    def run(self, args):
        with self.__lock:
            if self.__file_reader is None:
                self.__setup_file_reader(file=args["File"],
                                         chunksize=args["Chunk Size"])

        data = self.__get_next_chunk()
        
        #Data will be None if EOF occured
        if data is None:
            if args["Loop on end"]:
                
                #If loop on EOF then start reader again at beginning
                data = self.__get_next_chunk()
            else:
                return None

        return data

    @staticmethod
    def main():
        reader = CSVReader()
        reader._CSVReader__setup_file_reader('out/prices.csv', 100)
        reader._CSVReader__get_next_chunk()


if __name__ == "__main__":
    CSVReader.main()
