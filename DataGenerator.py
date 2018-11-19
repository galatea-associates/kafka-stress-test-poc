import random
import string
import datetime

# TODO: merge sedol and cusip dictionaries
# TODO: check inst_id is unique

class DataGenerator:

    def __init__(self):
        self.__stock_inst_ids = {}
        self.__cash_inst_ids = {}
        self.__stock_to_cusip = {}
        self.__stock_to_sedol = {}
        self.__state = {}

    def state_contains_field(self, field_to_generate):
        return field_to_generate in self.__state

    def get_state_value(self, field_to_generate):
        return self.__state[field_to_generate]

    def clear_state(self):
        self.__state = {}

    def __get_preemptive_generation(self, field_name, field_value):
        if field_name not in self.__state:
            asset_class = field_value
            self.__state[field_name] = field_value
        else:
            asset_class = self.__state[field_name]
        return asset_class

    def generate_new_inst_id(self, n_chars=5, asset_class=None):
        if asset_class is None:
            asset_class = self.__get_preemptive_generation('asset_class', self.generate_asset_class())

        possible_chars = string.ascii_uppercase + string.digits
        if asset_class == 'Stock':
            inst_id = 'ABC' + ''.join([random.choice(possible_chars) for _ in range(n_chars)])
            self.__stock_inst_ids[inst_id] = {}
        else:
            inst_id = 'BCD' + ''.join([random.choice(possible_chars) for _ in range(n_chars)])
            self.__cash_inst_ids[inst_id] = {}
        return inst_id

    def generate_inst_id(self, only=None, asset_class=None):
        if only is None:
            if asset_class is None:
                asset_class = self.__get_preemptive_generation('asset_class', self.generate_asset_class())
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
            asset_class = self.__get_preemptive_generation('asset_class', self.generate_asset_class())

        if asset_class is 'Cash':
            return ''

        if ticker is None:
            ticker = self.__get_preemptive_generation('ticker', self.generate_ticker(asset_class))

        if ticker in self.__stock_to_cusip:
            cusip = self.__stock_to_cusip[ticker]
        else:
            cusip = ''.join([random.choice(string.digits) for _ in range(n_digits)])
            self.__stock_to_cusip[ticker] = cusip

        return cusip

    def generate_sedol(self, n_digits=7, asset_class=None, ticker=None):
        if asset_class is None:
            asset_class = self.__get_preemptive_generation('asset_class', self.generate_asset_class())

        if asset_class == 'Cash':
            return ''

        if ticker is None:
            ticker = self.__get_preemptive_generation('ticker', self.generate_ticker(asset_class))

        if ticker in self.__stock_to_sedol:
            sedol = self.__stock_to_sedol[ticker]
        else:
            sedol = ''.join([random.choice(string.digits) for _ in range(n_digits)])
            self.__stock_to_sedol[ticker] = sedol

        return sedol

    def generate_isin(self, coi=None, cusip=None, asset_class=None):
        if asset_class is None:
            asset_class = self.__get_preemptive_generation('asset_class', self.generate_asset_class())

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
            asset_class = self.__get_preemptive_generation('asset_class', self.generate_asset_class())

        if asset_class is 'Cash':
            return ''

        if ticker is None:
            ticker = self.__get_preemptive_generation('ticker', self.generate_ticker(asset_class))

        return ticker + '.' + random.choice(['L', 'N', 'OQ'])

    def generate_ticker(self, asset_class=None):
        if asset_class is None:
            asset_class = self.__get_preemptive_generation('asset_class', self.generate_asset_class())

        if asset_class == 'Stock':
            return random.choice(['IBM', 'APPL', 'TSLA', 'AMZN', 'DIS', 'F', 'GOOGL', 'FB'])
        else:
            return random.choice(['USD', 'CAD', 'EUR', 'GBP'])

    def generate_asset_class(self):

        return random.choice(['Stock', 'Cash'])

    def generate_coi(self):
        return random.choice(['US', 'GB', 'CA', 'FR', 'DE', 'CH', 'SG', 'JP'])

    def generate_price(self, inst_id=None):
        if inst_id is None:
            inst_id = self.__get_preemptive_generation('inst_id', self.generate_inst_id())

        if inst_id.startswith('ABC'):
            min = 10
            max = 10000
            num_decimal_points = 2
            return round(random.uniform(min, max), num_decimal_points)
        else:
            return 1.00

    def generate_currency(self):
        return random.choice(['USD', 'CAD', 'EUR', 'GBP'])

    def generate_type(self):
        return random.choice(['SD'])

    def generate_knowledge_date(self, from_year=2016, to_year=2017, from_month=1, to_month=12, from_day=1, to_day=28):
        year = random.randint(from_year, to_year)
        month = random.randint(from_month, to_month)
        day = random.randint(from_day, to_day)
        return datetime.datetime(year, month, day).date()

    def generate_effective_date(self, n_days_to_add=3, knowledge_date=None):
        if knowledge_date is None:
            knowledge_date = self.__get_preemptive_generation('knowledge_date', self.generate_knowledge_date())

        return knowledge_date + datetime.timedelta(days=n_days_to_add)

    # TODO: see if you have to merge the account and account number fields
    def generate_account(self, n_digits=4):
        account_types = ['ICP', 'ECP']
        return random.choice(account_types) + ''.join([random.choice(string.digits) for _ in range(n_digits)])

    def generate_direction(self):
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
        else:
            choices = ['']

        return random.choice(choices)

    def generate_depot_id(self, n_digits=5):
        return ''.join([random.choice(string.digits) for _ in range(n_digits)])

    def generate_account_number(self, n_digits=8):
        return ''.join([random.choice(string.digits) for _ in range(n_digits)])

    def generate_order_id(self, n_digits=8):
        return ''.join([random.choice(string.digits) for _ in range(n_digits)])

    def generate_customer_id(self, n_digits=8):
        return ''.join([random.choice(string.digits) for _ in range(n_digits)])

    def generate_sto_id(self, n_digits=7):
        return ''.join([random.choice(string.digits) for _ in range(n_digits)])

    def generate_agent_id(self, n_digits=7):
        return ''.join([random.choice(string.digits) for _ in range(n_digits)])

    def generate_haircut(self):
        return '2.00%'

    def generate_collateral_type(self):
        return random.choice(['Cash', 'Non Cash'])

    def generate_is_callable(self):
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
            collateral_type = self.__get_preemptive_generation('collateral_type', self.generate_collateral_type())

        if collateral_type == 'Cash':
            return '5.75%'
        else:
            return ''

    def generate_contract_id(self, n_digits=8):
        return ''.join([random.choice(string.digits) for _ in range(n_digits)])
