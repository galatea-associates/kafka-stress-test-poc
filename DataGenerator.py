import random
import string
import datetime
import argparse
import csv

class DataGenerator:

    def run(self):
        args = self.__get_args()
        if args.prices > 0:
            self.create_data_file('out/prices.csv', args.prices, self.generate_price_entity)
        if args.positions > 0:
            self.create_data_file('out/positions.csv', args.positions, self.generate_position_entity)
        if args.inst_ref > 0:
            self.create_data_file('out/inst-ref.csv', args.inst_ref, self.generate_inst_ref_entity)

    def __get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--prices', nargs='?', type=int, default=0)
        parser.add_argument('--positions', nargs='?', type=int, default=0)
        parser.add_argument('--inst-ref', nargs='?', type=int, default=0)
        return parser.parse_args()

    # file_name corresponds to the name of the CSV file the function will write to
    # n is the number of data entities to write to the CSV file
    # data_generator is the function reference that generates the data entity of interest
    def create_data_file(self, file_name, n, data_generator):
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

    def generate_price_entity(self):
        min = 100
        max = 1000000
        num_decimal_points = 2
        # Generate random price between min and max with 2 decimal points
        price = round(random.uniform(min, max), num_decimal_points)
        bank_id = "ABC"
        # Generate random inst id with the prefix of the bank (ABC) and a random string composed of numbers and letters
        inst_id = bank_id + ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(5)])
        return {'inst_id': inst_id, 'price': price}

    def generate_position_entity(self):
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
        knowledge_date = self.__generate_date()
        # Add 3 days to get the effective date
        effective_date = knowledge_date + datetime.timedelta(days=3) if type == 'SD' else knowledge_date
        return {'type': type,
                'knowledge_date': str(knowledge_date),
                'effective_date': str(effective_date),
                'account': account,
                'instrument': random.choice(instruments),
                'direction': random.choice(directions),
                'qty': qty}

    def generate_inst_ref_entity(self):
        bank_id = "ABC"
        # Generate random inst id with the prefix of the bank (ABC) and a random string composed of numbers and letters
        inst_id = bank_id + ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(5)])
        # Possible instruments
        instruments = ['Stock', 'Bond', 'Cash']
        # Possible countries
        countries = ['USA', 'UK', 'Canada', 'France', 'Germany', 'Switzerland', 'Singapore', 'Japan']
        return {'inst_id': inst_id, 'asset_class': random.choice(instruments), 'COI': random.choice(countries)}

    # Random date generator
    def __generate_date(self):
        year = random.randint(2016, 2017)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return datetime.datetime(year, month, day).date()


DataGenerator().run()