import json


class OpenJson(object):
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config_data = None
        self.load_data()

    def load_data(self):
        try:
            with open(self.config_file) as file_:
                self.config_data = json.load(file_)
        except Exception as exc:
            return 'loading config file {}'.format(self.config_file, exc)


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
