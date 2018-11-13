import random
import string
import datetime

class DictDataClasses:

    def __init__(self, n_inst_ref=14000, n_values=500):
        self.__n_inst_ref = n_inst_ref
        self.__n_values = n_values

    def get_dict(self):
        return {
            'inst_id': self.__get_inst_ids(),
            'asset_class': self.__get_asset_classes(),
            'COI': self.__get_COIs(),
            'price': self.__get_prices(),
            'curr': self.__get_currencies(),
            'qty': self.__get_quantities(),
            'type': self.__get_types(),
            'date': self.__get_dates(),
            'account': self.__get_accounts(),
            'inst': self.__get_insts(),
            'direction': self.__get_directions()
        }

    def __get_inst_ids(self, n_chars=5):
        possible_chars = string.ascii_uppercase + string.digits
        return ['ABC' + ''.join([random.choice(possible_chars) for _ in range(n_chars)]) for _ in range(self.__n_inst_ref)]

    def __get_asset_classes(self):
        return ['Stock', 'Cash']

    def __get_COIs(self):
        return ['USA', 'UK', 'Canada', 'France', 'Germany', 'Switzerland', 'Singapore', 'Japan']

    def __get_directions(self):
        return ['Credit', 'Debit']

    def __get_accounts(self):
        accounts = []
        account_types = ['ICP', 'ECP']
        for _ in range(self.__n_values):
            accounts.append(random.choice(account_types) + ''.join([random.choice(string.digits) for _ in range(4)]))
        return accounts

    def __get_insts(self):
        return ['IBM', 'APPL', 'TSLA']

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
