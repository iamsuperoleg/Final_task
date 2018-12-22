import json
from configured_logger import *

CONFIG_FILE_NAME = 'config.json'


class OpenJson(object):
    def __init__(self, config_file=CONFIG_FILE_NAME):
        self.config_file = config_file
        self.config_data = None
        self.load_data()

    def load_data(self):
        try:
            with open(self.config_file) as file_:
                self.config_data = json.load(file_)
        except Exception as exc:
            logger.error("'{}' while executing the method 'return_statistic'".format(exc))
            quit()


class InfoForTables(OpenJson):

    def staff_tuple(self):
        for staff in self.config_data['STAFF']:
            yield tuple(staff)

    def coffee_price_tuple(self):
        for coffee_price in self.config_data['COFFEE_PRICE']:
            yield tuple(coffee_price)

    def additive_price_tuple(self):
        for additive_price in self.config_data['ADDITIVE_PRICE']:
            yield tuple(additive_price)
