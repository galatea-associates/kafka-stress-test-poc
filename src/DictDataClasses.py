import random
import string
import datetime

class DictDataClasses:

    def __init__(self, n_inst_ref=14000, n_values=500):
        self.__n_inst_ref = n_inst_ref
        self.__n_values = n_values
        self.__stock_ticker = ['IBM', 'APPL', 'TSLA', 'AMZN', 'DIS', 'F', 'GOOGL', 'FB']

    def get_dict(self):
        return {
            'inst_id_stock': self.__get_inst_ids(prefix='ABC'),
            'inst_id_cash': self.__get_inst_ids(prefix='BCD'),
            'asset_class': self.__get_asset_classes(),
            'COI': self.__get_COIs(),
            'price': self.__get_prices(),
            'curr': self.__get_currencies(),
            'qty': self.__get_quantities(),
            'type': self.__get_types(),
            'date': self.__get_dates(),
            'account': self.__get_accounts(),
            'cash_inst': self.__get_cash_insts(),
            'stock_inst': self.__get_stock_insts(),
            'direction': self.__get_directions(),
            'cusip': self.__get_cusips(),
            'ticker': self.__get_tickers(),
            'sedol': self.__get_sedols(),
            'exchange_code': self.__get_exchange_codes(),
            'purpose': self.__get_purpose()
        }

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

    def __get_purpose(self):
        return ['Outright']

