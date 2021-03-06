from configured_logger import *
from data_base_handler import data_base_handler

try:
    new_input = raw_input
except NameError:
    new_input = input


class InputNameAndPosition(object):

    def __init__(self, name=None, position=None):
        self.name = name
        self.position = position

    def entrance(self):
        while True:
            if not self.name:
                self.get_name()
            if not self.position:
                self.get_position()
            self.create_new_user()
            self.choose_behavior()

    def get_name(self):
        self.name = new_input("Hello! "
                              "\nEnter your name: ").upper()
        return self.get_position()

    def get_position(self):
        position = new_input(("Hello, {}! "
                              "\n1 - MANAGER "
                              "\n2 - SALESMAN "
                              "\nEnter your position: ").format(self.name)).upper()

        if position == 'MANAGER' or position == '1':
            self.position = 'MANAGER'
            return self.create_new_user()
        if position == 'SALESMAN' or position == '2':
            self.position = 'SALESMAN'
            return self.create_new_user()
        else:
            print ('Wrong choice!')
            return self.get_name()

    def create_new_user(self):
        user_tuple = (self.name.upper(), self.position.upper())
        data_base_handler.add_user(user_tuple)
        return self.choose_behavior()

    def choose_behavior(self):
        if self.position == 'MANAGER':
            return InputMenuForManager(name=self.name, position=self.position)
        else:
            return InputMenuForSalesman(name=self.name, position=self.position)


class InputMenuForSalesman(InputNameAndPosition):
    def __init__(self, name, position):
        super(InputMenuForSalesman, self).__init__(name, position)
        self.menu_for_salesman()

    def menu_for_salesman(self):
        salesman_choose = new_input(('Ok, {}!'
                                     '\n1 - GET ORDER'
                                     '\n2 - LOGOUT'
                                     '\nChose action: ').format(self.name)).upper()
        if salesman_choose in ('1', 'GET ORDER'):
            return SalesMenu(self.name, self.position)
        if salesman_choose in ('2', 'LOGOUT'):
            self.name = None
            self.position = None
            print ('Logging off...')
            return self.entrance()
        else:
            print ('Wrong choice!')
            return self.menu_for_salesman()


class SalesMenu(InputNameAndPosition):
    def __init__(self, name, position):
        super(SalesMenu, self).__init__(name, position)
        self.sale_list = []
        self.coffee_dict = data_base_handler.return_coffee_dict()
        self.addictive_dict = data_base_handler.return_additive_dict()
        self.order_request()

    def order_request(self):
        print data_base_handler.view_coffee_list()
        while True:
            try:
                choose = new_input('\nSelect coffee position (or zero(0) to continue): ').upper()
                if choose in self.coffee_dict.keys():
                    coffee = self.coffee_dict[choose]
                    self.sale_list.append(coffee)
                    print 'Adding {} by price - {}'.format(coffee.name, coffee.price)
                if choose == "0":
                    print (data_base_handler.view_additive_list())
                    while True:
                        choose = new_input('\nSelect additive position (or zero(0) to continue): ').upper()
                        if choose in self.addictive_dict.keys():
                            additive = self.addictive_dict[choose]
                            self.sale_list.append(additive)
                            print ('Adding {} by price - {}'.format(additive.name, additive.price))
                        if choose == "0":
                            self.submit_order()
            except Exception as exc:
                logger.error("'{}' while executing the method 'order_request'".format(exc))
                quit()

    def submit_order(self):
        print ('Submitting order...')
        data_base_handler.rewrite_table_sales(self.name, self.sale_list)
        return self.total_price_request(self.sale_list)

    def total_price_request(self, sale_list):
        while True:
            choose = new_input('Printing total price?(Y/n): ')
            if choose.upper() == 'Y' or choose.upper() == '':
                print ("Total price is $ {}".format(data_base_handler.get_overall_price(sale_list)))
                return InputMenuForSalesman(self.name, self.position)
            if choose.upper() == 'N':
                return InputMenuForSalesman(self.name, self.position)


class InputMenuForManager(InputNameAndPosition):
    def __init__(self, name, position):
        super(InputMenuForManager, self).__init__(name, position)
        self.menu_for_manager()

    def menu_for_manager(self):
        manager_choose = new_input(('Ok, {}!'
                                    '\n1 - GET OVERALL STATISTIC'
                                    '\n2 - LOGOUT'
                                    '\nChose action: ').format(self.name)).upper()
        if manager_choose in ('1', 'GET OVERALL STATISTIC'):
            data_base_handler.return_statistic()
            return self.menu_for_manager()
        if manager_choose in ('2', 'LOGOUT'):
            self.name = None
            self.position = None
            print ('Logging off...')
            return self.entrance()
        else:
            print ('Wrong choice!')
            return self.menu_for_manager()
