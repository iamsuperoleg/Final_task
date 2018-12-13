# -*- coding: utf-8 -*-


import sqlite3
from tabulate import tabulate
from configuration import Configuration
from beverage import Beverage


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

    def rewrite_table_sales(self, name, sale_list):
        price = self.get_overall_price(sale_list)
        self.cur.execute('SELECT \"NUMBER OF SALES\", \"TOTAL VALUE\" FROM SALES WHERE NAME = ?', (name,))
        number_of_sales, total_value = self.cur.fetchone()
        number_of_sales += 1
        total_value += price
        self.cur.execute(
            'UPDATE SALES SET \"NUMBER OF SALES\" = ?, \"TOTAL VALUE\" = ? WHERE NAME = ?', (number_of_sales,
                                                                                             total_value,
                                                                                             name,))
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

    def get_salesman_by_name(self, user_tuple):
        name, position = user_tuple
        self.cur.execute('SELECT * FROM STAFF WHERE NAME = ? AND POSITION = ?', (name, position,))
        return self.cur.fetchall()

    def _user_exist(self, user_tuple):
        return bool(self.get_salesman_by_name(user_tuple))

    def add_user(self, user_tuple):
        if self._user_exist(user_tuple):
            print('Logging as a {} - {}'.format(user_tuple[0], user_tuple[1]))
        else:
            self.update_table_staff(user_tuple)
            self.update_table_sales(user_tuple)
            print 'User {} added as {}'.format(user_tuple[0], user_tuple[1])

    def menu(self):
        self.cur.execute('SELECT ROWID,* FROM COFFEE_PRICE')
        data = self.cur.fetchall()
        return [Beverage(rowid, name, price) for rowid, name, price in data]

    def view_menu(self, source=None, check_mode=False):
        if not source:
            source = self.menu()
        if check_mode:
            menu = [beverage.get_tuple_to_check() for beverage in source]
        else:
            menu = [beverage.get_tuple_to_menu() for beverage in source]
        columns = ['N#', 'Beverage', 'Price']
        return tabulate(menu, headers=columns, tablefmt="pipe", )

    def return_beverage_dict(self):
        return {str(beverage.rowid): beverage for beverage in self.menu()}

    def return_statistic(self):
        self.cur.execute('SELECT * FROM SALES')
        columns = ['Seller name', 'Number of sales', 'Total value($)']
        print tabulate(self.cur.fetchall(), headers=columns, tablefmt="pipe", ) + '\n'

    @staticmethod
    def get_overall_price(order):
        return sum(beverage.price for beverage in order)


configuration = Configuration()
coffee_for_me = DataBaseHandler()
coffee_for_me.init_tables(configuration)
