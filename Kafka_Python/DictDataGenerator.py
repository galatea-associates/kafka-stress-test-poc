import argparse
import csv
import os
from functools import partial
from Kafka_Python.Runnable import Runnable
from DataGenerator import DataGenerator

ddc = DataGenerator()
data_template = {
    'inst_ref': {
        'inst_id': {'func': ddc.generate_new_inst_id, 'args': ['asset_class']},
        'ric': {'func': ddc.generate_ric, 'args': ['ticker', 'asset_class']},
        'isin': {'func': ddc.generate_isin,
                 'args': ['coi', 'cusip', 'asset_class']},
        'sedol': {'func': ddc.generate_sedol,
                  'args': ['ticker', 'asset_class']},
        'ticker': {'func': ddc.generate_ticker, 'args': ['asset_class']},
        'cusip': {'func': ddc.generate_cusip,
                  'args': ['ticker', 'asset_class']},
        'asset_class': {'func': partial(ddc.generate_asset_class,
                                        generating_inst=True)},
        'coi': {'func': ddc.generate_coi, 'args': ['asset_class']},
        # 'event-time': {'func': ddc.generate_time_stamp}
    },
    'price': {
        'inst_id': {'func': ddc.generate_inst_id, 'args': ['asset_class']},
        'ric': {'func': partial(ddc.generate_ric, no_cash=True),
                'args': ['ticker', 'asset_class']},
        'price': {'func': ddc.generate_price, 'args': ['inst_id']},
        'curr': {'func': ddc.generate_currency}
    },
    'front_office_position': {
        'ric': {'func': partial(ddc.generate_ric, no_cash=True),
                'args': ['ticker', 'asset_class']},
        'position_type': {'func': ddc.generate_position_type},
        'knowledge_date': {'func': ddc.generate_knowledge_date},
        'effective_date': {'func': ddc.generate_effective_date,
                           'args': ['knowledge_date', 'position_type']},
        'account': {'func': partial(ddc.generate_account, no_ecp=True)},
        'direction': {'func': ddc.generate_direction},
        'qty': {'func': ddc.generate_qty},
        'purpose': {'func': partial(ddc.generate_purpose, data_type='FOP')},
    },
    'back_office_position': {
        'cusip': {'func': partial(ddc.generate_cusip, no_cash=True),
                  'args': ['ticker', 'asset_class']},
        'position_type': {'func': ddc.generate_position_type},
        'knowledge_date': {'func': ddc.generate_knowledge_date},
        'effective_date': {'func': partial(ddc.generate_effective_date,
                                           n_days_to_add=3),
                           'args': ['knowledge_date', 'position_type']},
        'account': {'func': ddc.generate_account},
        'direction': {'func': ddc.generate_direction},
        'qty': {'func': ddc.generate_qty},
        'purpose': {'func': partial(ddc.generate_purpose, data_type='BOP')},
    },
    'depot_position': {
        'isin': {'func': partial(ddc.generate_isin, no_cash=True),
                 'args': ['coi', 'cusip', 'asset_class']},
        'position_type': {'func': partial(ddc.generate_position_type,
                                          no_td=True)},
        'knowledge_date': {'func': ddc.generate_knowledge_date},
        'effective_date': {'func': ddc.generate_effective_date,
                           'args': ['knowledge_date', 'position_type']},
        'account': {'func': partial(ddc.generate_account, no_ecp=True)},
        'direction': {'func': ddc.generate_direction},
        'qty': {'func': ddc.generate_qty},
        'purpose': {'func': partial(ddc.generate_purpose, data_type='DP')},
        'depot_id': {'func': ddc.generate_depot_id}
    },
    'order_execution': {
        'order_id': {'func': ddc.generate_order_id, 'args': ['asset_class']},
        'account_num': {'func': ddc.generate_account_number},
        'direction': {'func': ddc.generate_direction},
        'sto_id': {'func': ddc.generate_sto_id, 'args': ['asset_class']},
        'agent_id': {'func': ddc.generate_agent_id, 'args': ['asset_class']},
        'price': {'func': ddc.generate_price, 'args': ['inst_id']},
        'curr': {'func': ddc.generate_currency},
        'ric': {'func': partial(ddc.generate_ric, no_cash=True),
                'args': ['ticker', 'asset_class']},
        'qty': {'func': ddc.generate_qty}
    },
    'stock_loan_position': {
        'stock_loan_contract_id': {
            'func': ddc.generate_new_stock_loan_contract_id
        },
        'ric': {'func': partial(ddc.generate_ric, no_cash=True),
                'args': ['ticker', 'asset_class']},
        'knowledge_date': {'func': ddc.generate_knowledge_date},
        'effective_date': {'func': ddc.generate_effective_date,
                           'args': ['knowledge_date', 'position_type']},
        'purpose': {'func': partial(ddc.generate_purpose, data_type='SL')},
        'td_qty': {'func': ddc.generate_qty},
        'sd_qty': {'func': ddc.generate_qty},
        'collateral_type': {'func': ddc.generate_collateral_type},
        'haircut': {'func': ddc.generate_haircut, 'args': ['collateral_type']},
        'collateral_margin': {'func': ddc.generate_collateral_margin,
                              'args': ['collateral_type']},
        'rebate_rate': {'func': ddc.generate_rebate_rate,
                        'args': ['collateral_type']},
        'borrow_fee': {'func': ddc.generate_borrow_fee,
                       'args': ['collateral_type']},
        'termination_date': {'func': ddc.generate_termination_date},
        'account': {'func': ddc.generate_account},
        'is_callable': {'func': ddc.generate_is_callable},
        'return_type': {'func': ddc.generate_return_type}
    },
    'swap_contract': {
        'swap_contract_id': {'func': ddc.generate_new_swap_contract_id},
        'status': {'func': ddc.generate_status},
        'start_date': {'func': ddc.generate_swap_start_date},
        'end_date': {'func': ddc.generate_swap_end_date,
                     'args': ['status', 'start_date']},
        'swap_type': {'func': ddc.generate_swap_type},
        'reference_rate': {'func': ddc.generate_reference_rate},
        'field1': {'func': ddc.generate_rdn},
        'field2': {'func': ddc.generate_rdn},
        'field3': {'func': ddc.generate_rdn},
        'field4': {'func': ddc.generate_rdn},
        'field5': {'func': ddc.generate_rdn},
        'field6': {'func': ddc.generate_rdn},
        'field7': {'func': ddc.generate_rdn},
        'field8': {'func': ddc.generate_rdn},
    },
    'swap_position': {
        'ric': {'func': partial(ddc.generate_ric, no_cash=True),
                'args': ['ticker', 'asset_class']},
        'swap_contract_id': {'func': ddc.generate_swap_contract_id},
        'position_type': {'func': ddc.generate_position_type},
        'knowledge_date': {'func': ddc.generate_knowledge_date},
        'effective_date': {'func': partial(ddc.generate_effective_date,
                                           n_days_to_add=3),
                           'args': ['knowledge_date', 'position_type']},
        'account': {'func': ddc.generate_account},
        'direction': {'func': ddc.generate_direction},
        'qty': {'func': ddc.generate_qty},
        'purpose': {'func': partial(ddc.generate_purpose, data_type='ST')},
    },
    'cash': {
        'amount': {'func': ddc.generate_qty},
        'curr': {'func': ddc.generate_currency},
        'account_num': {'func': ddc.generate_account_number},
        'purpose': {'func': partial(ddc.generate_purpose, data_type='C')}
    }
}


class DictRunnable(Runnable):

    # In DataConfiguration.py, 'Data Args' field should look like:
    # {'Type': 'position'}
    def run(self, args):
        pass

    @staticmethod
    def main():
        args = get_args()
        dict_data_generator = DictRunnable()
        dict_data_generator .__generate_data_files(args)

    def __generate_data_files(self, args):
        # Create out directory if it does not yet exist
        if not os.path.exists('out'):
            os.makedirs('out')
        if args.inst_refs > 0:
            self.__create_data_file('out/inst-refs.csv',
                                    args.inst_refs,
                                    'inst_ref')
        if args.prices > 0:
            self.__create_data_file('out/prices.csv', args.prices, 'price')
        if args.front_office_positions > 0:
            self.__create_data_file('out/front_office_positions.csv',
                                    args.front_office_positions,
                                    'front_office_position')
        if args.back_office_positions > 0:
            self.__create_data_file('out/back_office_positions.csv',
                                    args.back_office_positions,
                                    'back_office_position')
        if args.depot_positions > 0:
            self.__create_data_file('out/depot_positions.csv',
                                    args.depot_positions,
                                    'depot_position')
        if args.order_executions > 0:
            self.__create_data_file('out/order_executions.csv',
                                    args.order_executions,
                                    'order_execution')
        if args.stock_loan_positions > 0:
            self.__create_data_file('out/stock_loan_positions.csv',
                                    args.stock_loan_positions,
                                    'stock_loan_position')
        if args.swap_contracts > 0:
            self.__create_data_file('out/swap_contracts.csv',
                                    args.swap_contracts,
                                    'swap_contract')
        if args.swap_positions > 0:
            self.__create_data_file('out/swap_positions.csv',
                                    args.swap_positions,
                                    'swap_position')
        if args.cash > 0:
            self.__create_data_file('out/cash.csv', args.cash, 'cash')

    # file_name corresponds to the name of the CSV file the function will write
    # to n is the number of data entities to write to the CSV file
    # data_generator is the function reference that generates the data entity
    # of interest
    def __create_data_file(self, file_name, n, data_type):
        # w+ means create file first if it does not already exist
        with open(file_name, mode='w+', newline='') as file:
            data = self.__generate_data(data_template[data_type])
            writer = csv.DictWriter(file, fieldnames=list(data))
            writer.writeheader()
            writer.writerow(data)
            # n - 1 because we already wrote to the file once with the entity
            # variable - we do this to get the keys of the dictionary in order
            # to get the field names of the CSV file
            for _ in range(n - 1):
                entity = self.__generate_data(data_template[data_type])
                writer.writerow(entity)

    def __generate_data(self, template):
        data = {}
        for field, generator_function in template.items():
            if field not in data:
                if ddc.state_contains_field(field):
                    data[field] = ddc.get_state_value(field)
                elif 'args' in generator_function:
                    args = {}
                    for arg in generator_function['args']:
                        if arg in data:
                            args[arg] = data[arg]
                        elif ddc.state_contains_field(arg):
                            args[arg] = ddc.get_state_value(arg)
                    data[field] = generator_function['func'](**args)
                else:
                    data[field] = generator_function['func']()
        ddc.clear_state()

        return data


def get_args():
    parser = argparse.ArgumentParser()
    optional_args = {'nargs': '?', 'type': int, 'default': 0}
    parser.add_argument('--prices', **optional_args)
    parser.add_argument('--front-office-positions', **optional_args)
    parser.add_argument('--back-office-positions', **optional_args)
    parser.add_argument('--inst-refs', **optional_args)
    parser.add_argument('--depot-positions', **optional_args)
    parser.add_argument('--order-executions', **optional_args)
    parser.add_argument('--stock-loan-positions', **optional_args)
    parser.add_argument('--swap-contracts', **optional_args)
    parser.add_argument('--swap-positions', **optional_args)
    parser.add_argument('--cash', **optional_args)
    return parser.parse_args()


if __name__ == '__main__':
    DictRunnable.main()
