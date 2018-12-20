from data_base_handler import data_base_handler

try:
    new_input = raw_input
except NameError:
    new_input = input


class InputNameAndPosition(object):

    def __init__(self, name=None, position=None):
        self.name = name
        self.position = position
        if not self.name:
            self.get_name()

    def get_name(self):
        if not self.name:
            self.name = new_input("Hello! "
                                  "\nEnter your name: ").upper()
            return self.get_position()

    def get_position(self):
        if not self.position:
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
                print 'Wrong choice!'
                return self.get_name()

    def create_new_user(self):
        user_tuple = (self.name, self.position)
        data_base_handler.add_user(user_tuple)
        return self.chose_behavior()

    def chose_behavior(self):
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
                                     '\nchose action: ').format(self.name)).upper()
        if salesman_choose in ('1', 'GET ORDER'):
            return SalesMenu(self.name, self.position)
        if salesman_choose in ('2', 'LOGOUT'):
            print 'Logging off...'
            return InputNameAndPosition()
        else:
            print 'Wrong choice!'
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
            choose = new_input('\nSelect coffee position (or zero(0) to continue): ').upper()
            if choose in self.coffee_dict.keys():
                coffee = self.coffee_dict[choose]
                self.sale_list.append(coffee)
                print 'Adding {} by price - {}'.format(coffee.name, coffee.price)
            if choose == "0":
                print data_base_handler.view_additive_list()
                while True:
                    choose = new_input('\nSelect coffee position (or zero(0) to continue): ').upper()
                    if choose in self.addictive_dict.keys():
                        addictive = self.addictive_dict[choose]
                        self.sale_list.append(addictive)
                        print 'Adding {} by price - {}'.format(addictive.name, addictive.price)
                    else:
                        self.submit_order()

    def submit_order(self):
        print 'Submitting order...'
        data_base_handler.rewrite_table_sales(self.name, self.sale_list)
        return self.total_price_request(self.sale_list)

    def total_price_request(self, sale_list):
        choose = new_input('Printing total price?(Y/n): ')
        if choose.upper() == 'Y':
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
                                    '\nchose action: ').format(self.name)).upper()
        if manager_choose in ('1', 'GET OVERALL STATISTIC'):
            data_base_handler.return_statistic()
            return self.menu_for_manager()
        if manager_choose in ('2', 'LOGOUT'):
            print 'Logging off...'
            return InputNameAndPosition()
        else:
            print 'Wrong choice!'
            return self.menu_for_manager()
