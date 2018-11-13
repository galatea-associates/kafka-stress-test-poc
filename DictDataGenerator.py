import random
import datetime
import argparse
import csv
import os
from DataGenerator import DataGenerator
from DictDataClasses import DictDataClasses

class DictDataGenerator(DataGenerator):

    def __init__(self):
        # Generate random inst ids with the prefix of the bank (ABC) and a random string composed of numbers and letters
        self.__stock_inst_ids = {}
        self.__cash_inst_ids = {}
        self.__dict = DictDataClasses().get_dict()

    # In DataConfiguration.py, 'Data Args' field should look like:
    # {'Type': 'position'}
    def run(self, args):
        type = args["Type"]
        if type == 'price':
            return self.__generate_price_entity()
        elif type == 'position':
            return self.__generate_position_entity()
        elif type == 'inst-ref':
            return self.__generate_inst_ref_entity()

    @staticmethod
    def main():
        args = DictDataGenerator.__get_args()
        dict_data_generator = DictDataGenerator()
        dict_data_generator .__generate_data_files(args)

    def __generate_data_files(self, args):
        # Create out directory if it does not yet exist
        if not os.path.exists('out'):
            os.makedirs('out')
        if args.inst_refs > 0:
            self.__create_data_file('out/inst-ref.csv', args.inst_refs, self.__generate_inst_ref_entity)
        if args.prices > 0:
            self.__create_data_file('out/prices.csv', args.prices, self.__generate_price_entity)
        if args.positions > 0:
            self.__create_data_file('out/positions.csv', args.positions, self.__generate_position_entity)

    @staticmethod
    def __get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--prices', nargs='?', type=int, default=0)
        parser.add_argument('--positions', nargs='?', type=int, default=0)
        parser.add_argument('--inst-refs', nargs='?', type=int, default=0)
        return parser.parse_args()

    # file_name corresponds to the name of the CSV file the function will write to
    # n is the number of data entities to write to the CSV file
    # data_generator is the function reference that generates the data entity of interest
    def __create_data_file(self, file_name, n, data_generator):
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

    def __generate_price_entity(self):
        asset_class = random.choice(self.__dict['asset_class'])
        if asset_class == 'Stock':
            inst_id = random.choice(list(self.__stock_inst_ids))
            price = random.choice(self.__dict['price'])
        else:
            inst_id = random.choice(list(self.__cash_inst_ids))
            price = 1.00
        curr = random.choice(self.__dict['curr'])

        return {'inst_id': inst_id,
                'price': price,
                'curr': curr}

    def __generate_position_entity(self):
        type = random.choice(self.__dict['type'])
        # Assign random date to knowledge date
        knowledge_date = random.choice(self.__dict['date'])
        # Add 3 days to get the effective date if type is SD
        effective_date = knowledge_date + datetime.timedelta(days=3) if type == 'SD' else knowledge_date
        account = random.choice(self.__dict['account'])
        direction = random.choice(self.__dict['direction'])
        qty = random.choice(self.__dict['qty'])
        asset_class = random.choice(self.__dict['asset_class'])
        if asset_class == 'Stock':
            inst_id = random.choice(list(self.__stock_inst_ids))
            inst = self.__stock_inst_ids[inst_id]
        else:
            inst_id = random.choice(list(self.__cash_inst_ids))
            inst = self.__cash_inst_ids[inst_id]

        return {'type': type,
                'knowledge_date': str(knowledge_date),
                'effective_date': str(effective_date),
                'account': account,
                'direction': direction,
                'qty': qty,
                'instrument': inst,
                'inst_id': inst_id}

    def __generate_inst_ref_entity(self):
        asset_class = random.choice(self.__dict['asset_class'])
        if asset_class == 'Stock':
            inst_id = self.__generate_inst_id(asset_class, self.__stock_inst_ids)
        else:
            inst_id = self.__generate_inst_id(asset_class, self.__cash_inst_ids)
        coi = random.choice(self.__dict['COI'])

        return {'inst_id': inst_id,
                'asset_class': asset_class,
                'COI': coi}

    def __generate_inst_id(self, asset_class, inst_ids):
        if asset_class == 'Stock':
            inst_id = random.choice(self.__dict['inst_id_stock'])
            inst = random.choice(self.__dict['stock_inst'])
        else:
            inst_id = random.choice(self.__dict['inst_id_cash'])
            inst = random.choice(self.__dict['cash_inst'])

        while inst_id in inst_ids:
            inst_id = random.choice(self.__dict['inst_id_stock']) if asset_class == 'Stock' else random.choice(
                self.__dict['inst_id_cash'])
        inst_ids[inst_id] = inst

        return inst_id

if __name__ == '__main__':
    DictDataGenerator.main()
