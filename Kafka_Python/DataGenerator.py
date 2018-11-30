import random
from functools import partial
import string
import datetime
import time
# from pandas import Timestamp
import pandas
# TODO: merge sedol and cusip dictionaries
# TODO: check inst_id is unique


class DataGenerator:

    def __init__(self):
        self.__curr_in_inst = []
        self.__stock_loan_contract_ids = []
        self.__swap_contract_ids = []
        self.__stock_inst_ids = {}
        self.__cash_inst_ids = {}
        self.__stock_to_cusip = {}
        self.__stock_to_sedol = {}
        self.__state = {}
        self.__possible_curr = ['USD', 'CAD', 'EUR', 'GBP']

    def state_contains_field(self, field_to_generate):
        return field_to_generate in self.__state

    def get_state_value(self, field_to_generate):
        return self.__state[field_to_generate]

    def clear_state(self):
        self.__state = {}

    # TODO: change this to function calls, don't pass actual value
    def __get_preemptive_generation(self, field_name, field_value):
        if field_name not in self.__state:
            self.__state[field_name] = field_value
            return field_value
        else:
            return self.__state[field_name]

    def generate_new_inst_id(self, n_chars=5, asset_class=None):
        """
        Generates a new instrument ID that is not used by any other instrument.
        ID will start with 'ABC' is the asset_class ia 'Stock' and 'BC" if it is
        'Cash'

        Args:
            n_chars: number of characters after prefix ('ABC' or 'BCD')

            asset_class: asset class of the instrument for which the instrument
            ID is being created
            If the asset_class is None, we generate it and save the generated
            value in the state class variable op it can be fetched later on

        Return: string comprised of a prefix and a random suffix
        """
        if asset_class is None:
            asset_class = self.__get_preemptive_generation(
                'asset_class',
                self.generate_asset_class(generating_inst=True))

        possible_chars = string.ascii_uppercase + string.digits
        suffix = [random.choice(possible_chars) for _ in range(n_chars)]
        if asset_class == 'Stock':
            inst_id = 'ABC' + ''.join(suffix)
            self.__stock_inst_ids[inst_id] = {}
        else:
            inst_id = 'BCD' + ''.join(suffix)
            self.__cash_inst_ids[inst_id] = {}
        return inst_id

    def generate_inst_id(self, only=None, asset_class=None):
        """
        Generates an existing instrument ID from __stock_inst_ids if the asset
        class of interest in 'Stock' or __cash_inst_ids if the asset class of
        interest is 'Cash'

        Args:
            only:

        Return: string comprised of n_digits digits
        """

        if only is None:
            if asset_class is None:
                asset_class = self.__get_preemptive_generation(
                    'asset_class',
                    self.generate_asset_class(generating_inst=True))
        elif only == 'S':
            asset_class = 'Stock'
        else:
            asset_class = 'Cash'

        if asset_class == 'Stock':
            return random.choice(list(self.__stock_inst_ids))
        else:
            return random.choice(list(self.__cash_inst_ids))

    def generate_cusip(self,  n_digits=9, ticker=None, asset_class=None):
        if asset_class is None:
            asset_class = self.__get_preemptive_generation(
                'asset_class',
                self.generate_asset_class(generating_inst=True))

        if asset_class is 'Cash':
            return ''

        if ticker is None:
            ticker = self.__get_preemptive_generation(
                'ticker',
                self.generate_ticker(asset_class))

        if ticker in self.__stock_to_cusip:
            cusip = self.__stock_to_cusip[ticker]
        else:
            digits = [random.choice(string.digits) for _ in range(n_digits)]
            cusip = ''.join(digits)
            self.__stock_to_cusip[ticker] = cusip

        return cusip

    def generate_sedol(self, n_digits=7, asset_class=None, ticker=None):
        if asset_class is None:
            asset_class = self.__get_preemptive_generation(
                'asset_class',
                self.generate_asset_class(generating_inst=True))

        if asset_class == 'Cash':
            return ''

        if ticker is None:
            ticker = self.__get_preemptive_generation(
                'ticker',
                self.generate_ticker(asset_class))

        if ticker in self.__stock_to_sedol:
            sedol = self.__stock_to_sedol[ticker]
        else:
            digits = [random.choice(string.digits) for _ in range(n_digits)]
            sedol = ''.join(digits)
            self.__stock_to_sedol[ticker] = sedol

        return sedol

    def generate_isin(self, coi=None, cusip=None, asset_class=None):
        if asset_class is None:
            asset_class = self.__get_preemptive_generation(
                'asset_class',
                self.generate_asset_class(generating_inst=True))

        if asset_class == 'Cash':
            return ''

        if coi is None:
            coi = self.generate_coi()
            self.__state['coi'] = coi

        if cusip is None:
            cusip = self.generate_cusip()
            self.__state['cusip'] = cusip

        return coi + cusip + '4'

    def generate_ric(self, ticker=None, asset_class=None):
        if asset_class is None:
            asset_class = self.__get_preemptive_generation(
                'asset_class',
                self.generate_asset_class(generating_inst=True))

        if asset_class is 'Cash':
            return ''

        if ticker is None:
            ticker = self.__get_preemptive_generation(
                'ticker',
                self.generate_ticker(asset_class))

        return ticker + '.' + random.choice(['L', 'N', 'OQ'])

    def generate_ticker(self, asset_class=None):
        if asset_class is None:
            asset_class = self.__get_preemptive_generation(
                'asset_class',
                self.generate_asset_class(generating_inst=True))

        if asset_class == 'Stock':
            return random.choice(['IBM', 'APPL', 'TSLA', 'AMZN', 'DIS', 'F',
                                  'GOOGL', 'FB'])
        else:
            possibles_curr_tickers = [c for c in self.__possible_curr
                                      if c not in self.__curr_in_inst]
            curr = random.choice(possibles_curr_tickers)
            self.__curr_in_inst.append(curr)
            return curr

    def generate_asset_class(self, generating_inst=False):
        if generating_inst:
            if len(self.__curr_in_inst) == len(self.__possible_curr):
                return 'Stock'
            return random.choice(['Stock', 'Cash'])
        else:
            return random.choice(['Stock', 'Cash'])

    def generate_coi(self, asset_class=None):
        """
        Generates a country of issuer

        Args:

        Return: one of the following strings ['US', 'GB', 'CA', 'FR', 'DE',
                                              'CH', 'SG', 'JP']
        """
        if asset_class is None:
            asset_class = self.__get_preemptive_generation(
                'asset_class',
                self.generate_asset_class())

        if asset_class == 'Cash':
            return ''

        return random.choice(['US', 'GB', 'CA', 'FR', 'DE', 'CH', 'SG', 'JP'])

    def generate_price(self, inst_id=None):
        if inst_id is None:
            inst_id = self.__get_preemptive_generation(
                'inst_id',
                self.generate_inst_id())

        if inst_id.startswith('ABC'):
            min = 10
            max = 10000
            num_decimal_points = 2
            return round(random.uniform(min, max), num_decimal_points)
        else:
            return 1.00

    def generate_currency(self):
        """
        Generates a country of issuer

        Args:

        Return: one of the following strings ['USD', 'CAD', 'EUR', 'GBP']
        """
        return random.choice(self.__possible_curr)

    def generate_position_type(self, no_sd=False, no_td=False):
        choices = ['SD', 'TD']
        if no_sd:
            choices.remove('SD')
        if no_td:
            choices.remove('TD')
        return random.choice(choices)

    def generate_knowledge_date(self,
                                from_year=2016, to_year=2017,
                                from_month=1, to_month=12,
                                from_day=1, to_day=28):
        year = random.randint(from_year, to_year)
        month = random.randint(from_month, to_month)
        day = random.randint(from_day, to_day)
        return datetime.datetime(year, month, day).date()

    def generate_effective_date(self, n_days_to_add=3,
                                knowledge_date=None, position_type=None):
        if position_type is None:
            position_type = self.__get_preemptive_generation(
                'position_type',
                self.generate_position_type())

        if knowledge_date is None:
            knowledge_date = self.__get_preemptive_generation(
                'knowledge_date',
                self.generate_knowledge_date())

        if position_type == 'TD':
            return knowledge_date
        else:
            return knowledge_date + datetime.timedelta(days=n_days_to_add)

    # TODO: see if you have to merge the account and account number fields
    def generate_account(self, n_digits=4, no_ecp=False, no_icp=False):
        choices = ['ICP', 'ECP']
        if no_ecp:
            choices.remove('ECP')
        if no_icp:
            choices.remove('ICP')

        account_type = random.choice(choices)
        digits = [random.choice(string.digits) for _ in range(n_digits)]
        return account_type + ''.join(digits)

    def generate_direction(self):
        """
        Generates a direction

        Args:

        Return: one of the following strings ['Credit', 'Debit']
        """
        return random.choice(['Credit', 'Debit'])

    def generate_qty(self, min_qty=1, max_qty=21):
        return random.choice([n * 100 for n in range(min_qty, max_qty)])

    def generate_purpose(self, data_type=None):
        if data_type == 'FOP' or data_type == 'BOP' or data_type == 'ST':
            choices = ['Outright']
        elif data_type == 'DP':
            choices = ['Holdings', 'Seg']
        elif data_type == 'SL':
            choices = ['Borrow', 'Loan']
        elif data_type == 'C':
            choices = ['Cash Balance', 'P&L', 'Fees']
        else:
            choices = ['']

        return random.choice(choices)

    def generate_depot_id(self, n_digits=5):
        """
        Generates a depot ID, here the ID is a sequence of numbers, no
        letters. This is why we pick characters from string.digits only

        Args:
            n_digits: the number of digits to have in the ID, i.e. the length of
            the ID

        Return: a string comprised of n_digits digits
        """
        return ''.join([random.choice(string.digits) for _ in range(n_digits)])

    def generate_account_number(self, n_digits=8):
        """
        Generates an account number, here the ID is a sequence of numbers, no
        letters. This is why we pick characters from string.digits only

        Args:
            n_digits: the number of digits to have in the ID, i.e. the length of
            the ID

        Return: a string comprised of n_digits digits
        """
        return ''.join([random.choice(string.digits) for _ in range(n_digits)])

    def generate_order_id(self, n_digits=8):
        """
        Generates an order ID, here the ID is a sequence of numbers, no letters.
        This is why we pick characters from string.digits only

        Args:
            n_digits: the number of digits to have in the ID, i.e. the length of
            the ID

        Return: a string comprised of n_digits digits
        """
        return ''.join([random.choice(string.digits) for _ in range(n_digits)])

    def generate_customer_id(self, n_digits=8):
        """
        Generates a customer ID, here the ID is a sequence of numbers, no
        letters. This is why we pick characters from string.digits only

        Args:
            n_digits: the number of digits to have in the ID, i.e. the length of
            the ID

        Return: a string comprised of n_digits digits
        """
        return ''.join([random.choice(string.digits) for _ in range(n_digits)])

    def generate_sto_id(self, n_digits=7):
        """
        Generates a STO ID, here the ID is a sequence of numbers, no letters.
        This is why we pick characters from string.digits only

        Args:
            n_digits: the number of digits to have in the ID, i.e. the length of
            the ID

        Return: a string comprised of n_digits digits
        """
        return ''.join([random.choice(string.digits) for _ in range(n_digits)])

    def generate_agent_id(self, n_digits=7):
        """
        Generates an agent ID, here the ID is a sequence of numbers, no letters.
        This is why we pick characters from string digits only

        Args:
            n_digits: the number of digits to have in the ID, i.e. the length of
            the ID

        Return: a string comprised of n_digits digits
        """
        return ''.join([random.choice(string.digits) for _ in range(n_digits)])

    def generate_haircut(self):
        """
        Generates a haircut value, typically this is 2% so that is the value
        we are using

        Args:

        Return: a string representing 2.00%
        """
        return '2.00%'

    def generate_collateral_type(self):
        """
        Generates a collateral type

        Args:

        Return: one of the following strings ['Cash', 'Non Cash']
        """
        return random.choice(['Cash', 'Non Cash'])

    def generate_is_callable(self):
        """
        Generates a is_callable value: 'Yes' means it is and 'No' means it isn't

        Args:

        Return: one of the following strings ['Yes', 'No']
        """
        return random.choice(['Yes', 'No'])

    # TODO: change knowledge date function name
    def generate_termination_date(self):
        does_exist = random.choice([True, False])
        if not does_exist:
            return ''
        else:
            return self.generate_knowledge_date(from_year=2019, to_year=2020)

    # TODO: generate percentages, not just hard code
    def generate_rebate_rate(self, collateral_type=None):
        if collateral_type is None:
            collateral_type = self.__get_preemptive_generation(
                'collateral_type',
                self.generate_collateral_type())

        if collateral_type == 'Cash':
            return '5.75%'
        else:
            return ''

    def generate_new_stock_loan_contract_id(self, n_digits=8):
        """
        Generates a new swap contract ID that is not used by any other current
        swap contracts. Adds new ID to __swap_contract_ids in order to keep
        keep track of all the current ones (so we avoid clashes)

        Args:
            n_digits: number of digits in the ID, i.e. the length of the ID
            since it contains only digits

        Return: string comprised of n_digits digits
        """
        id = ''.join([random.choice(string.digits) for _ in range(n_digits)])
        self.__stock_loan_contract_ids.append(id)
        return id

    def generate_new_swap_contract_id(self, n_digits=8):
        """
        Generates a new swap contract ID that is not used by any other current
        swap contracts. Adds new ID to __swap_contract_ids in order to keep
        keep track of all the current ones (so we avoid clashes)

        Args:
            n_digits: number of digits in the ID, i.e. the length of the ID
            since it contains only digits

        Return: string comprised of n_digits digits
        """
        id = ''.join([random.choice(string.digits) for _ in range(n_digits)])
        self.__swap_contract_ids.append(id)
        return id

    # TODO: what happens if __swap_contract_ids is empty?
    def generate_swap_contract_id(self):
        """
        Generates an existing swap contract ID from __swap_contract_ids

        Args:

        Return: string comprised of n_digits digits
        """
        return random.choice(self.__swap_contract_ids)

    def generate_status(self):
        """
        Generates a status

        Args:

        Return: one of the following strings ['Live', 'Dead']
        """
        return random.choice(['Live', 'Dead'])

    # TODO: merge knowledge_date with swap_start_date maybe even effective_date
    # and swap_end_date
    def generate_swap_start_date(self,
                                 from_year=2016, to_year=2017,
                                 from_month=1, to_month=12,
                                 from_day=1, to_day=28):
        year = random.randint(from_year, to_year)
        month = random.randint(from_month, to_month)
        day = random.randint(from_day, to_day)
        return datetime.datetime(year, month, day).date()

    def generate_swap_end_date(self, n_years_to_add=5,
                               start_date=None, status=None):
        if status is None:
            status = self.__get_preemptive_generation(
                'status',
                self.generate_status())

        if status == 'Live':
            return ''
        else:
            if start_date is None:
                start_date = self.__get_preemptive_generation(
                    'start_date',
                    self.generate_swap_start_date())

            return start_date + datetime.timedelta(days=365*n_years_to_add)

    def generate_swap_type(self):
        """
        Generates a swap type

        Args:

        Return: one of the following strings ['Equity', 'Portfolio']
        """
        return random.choice(['Equity', 'Portfolio'])

    def generate_reference_rate(self):
        """
        Generates a reference rate

        Args:

        Return: one of the following strings ['LIBOR']
        """
        return random.choice(['LIBOR'])

    def generate_return_type(self):
        """
        Generates a return type

        Args:

        Return: one of the following strings
        ['Outstanding', 'Pending Return', 'Pending Recall', 'Partial Return',
         'Partial Recall', 'Settled']
        """
        return random.choice(['Outstanding', 'Pending Return', 'Pending Recall',
                              'Partial Return', 'Partial Recall', 'Settled'])

    def generate_rdn(self):
        """
        Returns same value, used for mock fields, i.e. fields used just to make
        the data type more realistic in therms of number of of fields it has

        Args:

        Return: 'Rdn'
        """
        return 'Rdn'

    def generate_time_stamp(self):
        """
        Returns timestamp

        Args:

        Return: timestamp
        """

        now = Timestamp.utcnow()
        return now.to_datetime64()
        # return datetime.datetime.utcnow()
