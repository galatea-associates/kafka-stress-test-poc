import random
import string
import datetime

# TODO: merge sedol and cusip dictionaries
# TODO: check inst_id is unique

class DictDataClasses:

    def __init__(self, n_inst_ref=14000, n_values=500):
        self.__n_inst_ref = n_inst_ref
        self.__n_values = n_values
        self.__stock_inst_ids = {}
        self.__cash_inst_ids = {}
        self.__stock_to_cusip = {}
        self.__stock_to_sedol = {}
        self.__state = {}

    def get_dict(self):
        return {
            # 'inst_id_stock': self.__get_inst_ids(prefix='ABC'),
            # 'inst_id_cash': self.__get_inst_ids(prefix='BCD'),
            # 'asset_class': self.__get_asset_classes(),
            # 'COI': self.__get_COIs(),
            # 'price': self.__get_prices(),
            # 'curr': self.__get_currencies(),
            # 'qty': self.__get_quantities(),
            # 'type': self.__get_types(),
            # 'date': self.__get_dates(),
            # 'account': self.__get_accounts(),
            # 'cash_inst': self.__get_cash_insts(),
            # 'stock_inst': self.__get_stock_insts(),
            # 'direction': self.__get_directions(),
            # 'cusip': self.__get_cusips(),
            # 'ticker': self.__get_tickers(),
            # 'sedol': self.__get_sedols(),
            # 'exchange_code': self.__get_exchange_codes(),
            # 'purpose': self.__get_purposes(),
            # 'depot_id': self.__get_depot_ids(),
            # 'account_number': self.__get_account_numbers()
        }

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

    def generate_inst_id(self, asset_class=None):
        if asset_class is None:
            asset_class = self.__get_preemptive_generation('asset_class', self.generate_asset_class())

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


    def __get_inst_ids(self, prefix='ABC', n_chars=5):
        possible_chars = string.ascii_uppercase + string.digits
        return [prefix + ''.join([random.choice(possible_chars) for _ in range(n_chars)]) for _ in range(self.__n_inst_ref)]

    def __get_asset_classes(self):
        return ['Stock', 'Cash']

    def __get_COIs(self):
        return ['US', 'GB', 'CA', 'FR', 'DE', 'CH', 'SG', 'JP']

    def __get_directions(self):
        return ['Credit', 'Debit']

    def __get_accounts(self):
        accounts = []
        account_types = ['ICP', 'ECP']
        for _ in range(self.__n_values):
            accounts.append(random.choice(account_types) + ''.join([random.choice(string.digits) for _ in range(4)]))
        return accounts

    def __get_stock_insts(self):
        return self.__stock_ticker

    def __get_cash_insts(self):
        return ['USD', 'CAD', 'EUR', 'GBP']

    def __get_dates(self):
        dates = []
        from_year = 2016
        to_year = 2017
        from_month = 1
        to_month = 12
        from_day = 1
        to_day = 28
        for _ in range(self.__n_values):
            year = random.randint(from_year, to_year)
            month = random.randint(from_month, to_month)
            day = random.randint(from_day, to_day)
            dates.append(datetime.datetime(year, month, day).date())
        return dates

    def __get_quantities(self, min=1, max=21):
        return [n * 100 for n in range(min, max)]

    def __get_types(self):
        return ['SD']

    def __get_prices(self):
        min = 10
        max = 1000
        num_decimal_points = 2
        prices = []
        for _ in range(self.__n_values):
            # Generate random price between min and max with 2 decimal points
            prices.append(round(random.uniform(min, max), num_decimal_points))
        return prices

    def __get_currencies(self):
        return ['USD', 'CAD', 'EUR', 'GBP']

    def __get_cusips(self, n_digits=9):
        return [''.join([random.choice(string.digits) for _ in range(n_digits)]) for _ in range(self.__n_inst_ref)]

    def __get_tickers(self):
        return self.__stock_ticker

    def __get_sedols(self, n_digits=7):
        return [''.join([random.choice(string.digits) for _ in range(n_digits)]) for _ in range(self.__n_inst_ref)]

    def __get_exchange_codes(self):
        return ['L', 'N', 'OQ']

    def __get_purposes(self):
        return ['Outright', '']

    def __get_depot_ids(self, n_digits=5):
        return [''.join([random.choice(string.digits) for _ in range(n_digits)]) for _ in range(self.__n_inst_ref)]

    def __get_account_numbers(self, n_digits=8):
        return [''.join([random.choice(string.digits) for _ in range(n_digits)]) for _ in range(self.__n_inst_ref)]

    def state_contains_field(self, field_to_generate):
        return field_to_generate in self.__state

    def get_state_value(self, field_to_generate):
        return self.__state[field_to_generate]
