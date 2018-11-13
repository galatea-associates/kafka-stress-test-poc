import random
import string
import datetime

class DictDataClasses:

    def __init__(self):
        self.__n_inst_ref = 14000
        self.__n_values = 500

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

    def __get_inst_ids(self):
        possible_chars = string.ascii_uppercase + string.digits
        return ['ABC' + ''.join([random.choice(possible_chars) for _ in range(5)]) for _ in range(self.__n_inst_ref)]

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
        for _ in range(self.__n_values):
            year = random.randint(2016, 2017)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            dates.append(datetime.datetime(year, month, day).date())
        return dates

    def __get_quantities(self):
        return [n * 100 for n in range(1, 21)]

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
