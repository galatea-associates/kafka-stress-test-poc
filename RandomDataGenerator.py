import random
import string
import datetime
import argparse
import csv
import os
from DataGenerator import DataGenerator

class RandomDataGenerator(DataGenerator):

    def run(self):
        print("Run method exists")

    @staticmethod
    def main():
        args = RandomDataGenerator.__get_args()
        RandomDataGenerator.__generate_data_files(args)

    @staticmethod
    def __generate_data_files(args):
        # Create out directory if it does not yet exist
        if not os.path.exists('out'):
            os.makedirs('out')

        if args.prices > 0:
            RandomDataGenerator.create_data_file('out/prices.csv', args.prices, RandomDataGenerator.generate_price_entity)
        if args.positions > 0:
            RandomDataGenerator.create_data_file('out/positions.csv', args.positions, RandomDataGenerator.generate_position_entity)
        if args.inst_ref > 0:
            RandomDataGenerator.create_data_file('out/inst-ref.csv', args.inst_ref, RandomDataGenerator.generate_inst_ref_entity)

    @staticmethod
    def __get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--prices', nargs='?', type=int, default=0)
        parser.add_argument('--positions', nargs='?', type=int, default=0)
        parser.add_argument('--inst-ref', nargs='?', type=int, default=0)
        return parser.parse_args()

    # file_name corresponds to the name of the CSV file the function will write to
    # n is the number of data entities to write to the CSV file
    # data_generator is the function reference that generates the data entity of interest
    @staticmethod
    def create_data_file(file_name, n, data_generator):
        # w+ means create file first if it does not already exist
        with open(file_name, mode='w+', newline='') as file:
            entity = data_generator()
            writer = csv.DictWriter(file, fieldnames=list(entity))
            writer.writeheader()
            writer.writerow(entity)
            # n - 1 because we already wrote to the file once with the entity variable
            # We do this to get the keys of the dictionary in order to get the field names of the CSV file
            for _ in range(n - 1):
                entity = data_generator()
                writer.writerow(entity)

    @staticmethod
    def generate_price_entity():
        min = 100
        max = 1000000
        num_decimal_points = 2
        # Generate random price between min and max with 2 decimal points
        price = round(random.uniform(min, max), num_decimal_points)
        bank_id = "ABC"
        # Generate random inst id with the prefix of the bank (ABC) and a random string composed of numbers and letters
        inst_id = bank_id + ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(5)])
        return {'inst_id': inst_id, 'price': price}

    @staticmethod
    def generate_position_entity():
        # Possible types of a position
        types = ['SD']
        type = random.choice(types)
        # Possible instruments
        instruments = ['IBM', 'APPL', 'TSLA']
        # Possible position directions
        directions = ['Credit', 'Debit']
        # Here we represent account with 'ACC00' + random integers
        account_types = ['ICP', 'ECP']
        account = random.choice(account_types) + ''.join([random.choice(string.digits) for _ in range(4)])
        # Random quantity between 100 and 10,000
        qty = random.randint(100, 10000)
        # Assign random date to knowledge date
        knowledge_date = RandomDataGenerator.__generate_date()
        # Add 3 days to get the effective date
        effective_date = knowledge_date + datetime.timedelta(days=3) if type == 'SD' else knowledge_date
        return {'type': type,
                'knowledge_date': str(knowledge_date),
                'effective_date': str(effective_date),
                'account': account,
                'instrument': random.choice(instruments),
                'direction': random.choice(directions),
                'qty': qty}

    @staticmethod
    def generate_inst_ref_entity():
        bank_id = "ABC"
        # Generate random inst id with the prefix of the bank (ABC) and a random string composed of numbers and letters
        inst_id = bank_id + ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(5)])
        # Possible instruments
        instruments = ['Stock', 'Bond', 'Cash']
        # Possible countries
        countries = ['USA', 'UK', 'Canada', 'France', 'Germany', 'Switzerland', 'Singapore', 'Japan']
        return {'inst_id': inst_id, 'asset_class': random.choice(instruments), 'COI': random.choice(countries)}

    # Random date generator
    @staticmethod
    def __generate_date():
        year = random.randint(2016, 2017)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return datetime.datetime(year, month, day).date()

if __name__ == '__main__':
    RandomDataGenerator.main()