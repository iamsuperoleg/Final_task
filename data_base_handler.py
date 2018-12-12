import sqlite3
import json


class Configuration(object):
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config_data = None
        self.load_data()

    def load_data(self):
        try:
            with open(self.config_file) as file_:
                self.config_data = json.load(file_)
        except Exception as exc:
            return 'loading config file {}'.format(self.config_file), exc,

    def staff_tuple(self):
        for staff in self.config_data['STAFF']:
            yield tuple(staff)

    def coffee_price_tuple(self):
        for coffee_price in self.config_data['COFFEE_PRICE']:
            yield tuple(coffee_price)

    def additive_price_tuple(self):
        for additive_price in self.config_data['ADDITIVE_PRICE']:
            yield tuple(additive_price)


class DataBaseHandler(object):

    def __init__(self):
        self.database = sqlite3.connect("coffee.db")
        self.cur = self.database.cursor()

    def create_tables(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS STAFF (NAME TEXT, POSITION TEXT)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS COFFEE_PRICE (COFFEE TEXT, PRICE INTEGER FLOAT)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS ADDITIVE_PRICE (ADDITIVE TEXT, PRICE INTEGER FLOAT)""")
        self.cur.execute(
            '''CREATE TABLE  IF NOT EXISTS SALES(NAME TEXT, \"NUMBER OF SALES\" INTEGER FLOAT, \"TOTAL VALUE\" REAL)''')

    def update_table_staff(self, user_tuple):
        self.cur.execute("INSERT INTO STAFF VALUES (?,?)", user_tuple)
        self.database.commit()

    def update_table_coffee_price(self, coffee_price):
        self.cur.execute("INSERT INTO COFFEE_PRICE VALUES (?,?)", coffee_price)
        self.database.commit()

    def update_table_additive_price(self, additive_price):
        self.cur.execute("INSERT INTO ADDITIVE_PRICE VALUES (?,?)", additive_price)
        self.database.commit()

    def update_table_sales(self, user_tuple):
        name, position = user_tuple
        if not position == 'MANAGER':
            self.cur.execute("INSERT INTO SALES VALUES (?,?,?)", (name, 0, 0,))
            self.database.commit()

    def init_tables(self, config_object):

        self.create_tables()

        for user_tuple in config_object.staff_tuple():
            self.update_table_staff(user_tuple)
            self.update_table_sales(user_tuple)

        for coffee_price_tuple in config_object.coffee_price_tuple():
            self.update_table_coffee_price(coffee_price_tuple)

        for additive_price_tuple in config_object.additive_price_tuple():
            self.update_table_additive_price(additive_price_tuple)


configuration = Configuration()
coffee_for_me = DataBaseHandler()
coffee_for_me.init_tables(configuration)
