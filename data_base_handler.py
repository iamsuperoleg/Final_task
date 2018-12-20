import sqlite3
import logging
import sys
from configuration import InfoForTables
from get_menu import GetProductList

logger = logging.getLogger(__name__)
logfile = "final_task_log.log"

formatter = logging.Formatter('%(asctime)s - %(name)s:  %(levelname)s - %(message)s')
screen_handler = logging.StreamHandler(sys.stdout)
screen_handler.setLevel(logging.ERROR)
screen_handler.setFormatter(formatter)

file_handler = logging.FileHandler(logfile)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(screen_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

try:
    from tabulate import tabulate
except ImportError:
    logger.error("Must be installed module {}"
                 "\n Try 'python -m pip install tabulate'".format(__name__))
    quit()


class DataBaseHandler(object):

    def __init__(self, db_name="coffee_for_me.db"):
        try:
            self.db_name = db_name
            self.database = sqlite3.connect(db_name)
            self.cur = self.database.cursor()
        except Exception as exc:
            logger.error("During connecting to database:{}"
                         "\n ERROR:{}".format(self.db_name, exc))
            quit()

    def create_tables(self):
        try:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS STAFF (NAME TEXT, POSITION TEXT)""")
            self.cur.execute("""CREATE TABLE IF NOT EXISTS COFFEE_PRICE (COFFEE TEXT, PRICE INTEGER FLOAT)""")
            self.cur.execute("""CREATE TABLE IF NOT EXISTS ADDITIVE_PRICE (ADDITIVE TEXT, PRICE INTEGER FLOAT)""")
            self.cur.execute('''CREATE TABLE  IF NOT EXISTS SALES (NAME TEXT, 
                                                                   \"NUMBER OF SALES\" INTEGER FLOAT, 
                                                                   \"TOTAL VALUE\" REAL)''')
        except Exception as exc:
            logger.error("ERROR: {} while executing the method 'create_tables'".format(exc))
            quit()

    def update_table_staff(self, user_tuple):
        try:
            if not self._user_exist(user_tuple):
                self.cur.execute("INSERT INTO STAFF VALUES (?,?)", user_tuple)
                self.database.commit()
        except Exception as exc:
            logger.error("ERROR: {} while executing the method 'update_table_staff'".format(exc))
            quit()

    def update_table_coffee_price(self, coffee_price):
        try:
            if not self._coffee_exist(coffee_price):
                self.cur.execute("INSERT INTO COFFEE_PRICE VALUES (?,?)", coffee_price)
                self.database.commit()
        except Exception as exc:
            logger.error("ERROR: {} while executing the method 'update_table_coffee_price'".format(exc))
            quit()

    def update_table_additive_price(self, additive_price):
        try:
            if not self._additive_exist(additive_price):
                self.cur.execute("INSERT INTO ADDITIVE_PRICE VALUES (?,?)", additive_price)
                self.database.commit()
        except Exception as exc:
            logger.error("ERROR: {} while executing the method 'update_table_additive_price'".format(exc))
            quit()

    def update_table_sales(self, user_tuple):
        try:
            name, position = user_tuple
            if not self._sales_exist(user_tuple) and position == 'SALESMAN':
                self.cur.execute("INSERT INTO SALES VALUES (?,?,?)", (name, 0, 0,))
                self.database.commit()
        except Exception as exc:
            logger.error("ERROR: {} while executing the method 'update_table_sales'".format(exc))
            quit()

    def rewrite_table_sales(self, name, sale_list):
        try:
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
        except Exception as exc:
            logger.error("ERROR: {} while executing the method 'rewrite_table_sales'".format(exc))
            quit()

    def init_tables(self, info_for_tables):

        self.create_tables()

        for user_tuple in info_for_tables.staff_tuple():
            self.update_table_staff(user_tuple)
            self.update_table_sales(user_tuple)

        for coffee_price_tuple in info_for_tables.coffee_price_tuple():
            self.update_table_coffee_price(coffee_price_tuple)

        for additive_price_tuple in info_for_tables.additive_price_tuple():
            self.update_table_additive_price(additive_price_tuple)

    def check_table_staff(self, user_tuple):
        name, position = user_tuple
        self.cur.execute('SELECT * FROM STAFF WHERE NAME = ? AND POSITION = ?', (name, position,))
        return self.cur.fetchall()

    def check_table_coffee(self, coffee_price):
        coffee, price = coffee_price
        self.cur.execute('SELECT * FROM COFFEE_PRICE WHERE COFFEE = ? AND PRICE = ?', (coffee, price,))
        return self.cur.fetchall()

    def check_table_additive(self, additive_price):
        additive, price = additive_price
        self.cur.execute('SELECT * FROM ADDITIVE_PRICE WHERE ADDITIVE = ? AND PRICE = ?', (additive, price,))
        return self.cur.fetchall()

    def check_table_sales(self, user_tuple):
        name, position = user_tuple
        self.cur.execute('SELECT * FROM SALES WHERE NAME = ?', (name,))
        return self.cur.fetchall()

    def _user_exist(self, user_tuple):
        return bool(self.check_table_staff(user_tuple))

    def _coffee_exist(self, coffee_price):
        return bool(self.check_table_coffee(coffee_price))

    def _additive_exist(self, additive_price):
        return bool(self.check_table_additive(additive_price))

    def _sales_exist(self, user_tuple):
        return bool(self.check_table_sales(user_tuple))

    def add_user(self, user_tuple):
        if self._user_exist(user_tuple):
            print('Logging as a {} - {}'.format(user_tuple[0], user_tuple[1]))
        else:
            self.update_table_staff(user_tuple)
            self.update_table_sales(user_tuple)
            print 'User {} added as {}'.format(user_tuple[0], user_tuple[1])

    def coffee_list(self):
        self.cur.execute('SELECT ROWID,* FROM COFFEE_PRICE')
        coffee_data = self.cur.fetchall()
        return [GetProductList(rowid, name, price) for rowid, name, price in coffee_data]

    def additive_list(self):
        self.cur.execute('SELECT ROWID,* FROM ADDITIVE_PRICE')
        additive_data = self.cur.fetchall()
        return [GetProductList(rowid, name, price) for rowid, name, price in additive_data]

    def view_coffee_list(self):
        coffee_source = self.coffee_list()
        coffee_menu = [beverage.get_tuple_to_product() for beverage in coffee_source]
        columns = ['POS', 'COFFEE', 'PRICE']
        return tabulate(coffee_menu, headers=columns, tablefmt="pipe", )

    def view_additive_list(self):
        additive_source = self.additive_list()
        additive_menu = [beverage.get_tuple_to_product() for beverage in additive_source]
        columns = ['POS', 'ADDITIVE', 'PRICE']
        return tabulate(additive_menu, headers=columns, tablefmt="pipe", )

    def return_coffee_dict(self):
        return {str(beverage.rowid): beverage for beverage in self.coffee_list()}

    def return_additive_dict(self):
        return {str(beverage.rowid): beverage for beverage in self.additive_list()}

    def return_statistic(self):
        self.cur.execute('SELECT * FROM SALES')
        columns = ['Seller name', 'Number of sales', 'Total value($)']
        print tabulate(self.cur.fetchall(), headers=columns, tablefmt="pipe", ) + '\n'

    @staticmethod
    def get_overall_price(order):
        return sum(beverage.price for beverage in order)


info_for_tables = InfoForTables()
data_base_handler = DataBaseHandler()
data_base_handler.init_tables(info_for_tables)
