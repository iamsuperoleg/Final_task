#!/usr/bin/env python
# -*- coding: utf-8 -*-


from data_base_handler import coffee_for_me


class User(object):

    def __init__(self, name=None, position=None):
        self.name = name
        self.position = position
        if not self.name:
            self.get_name()

    def get_name(self):
        if not self.name:
            self.name = raw_input("Hello! "
                                  "\nEnter your name: ").upper()
            return self.get_position()

    def get_position(self):
        if not self.position:
            position = raw_input(("Hello, {}! "
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
        coffee_for_me.add_user(user_tuple)
        return self.chose_behavior()

    def chose_behavior(self):
        if self.position == 'MANAGER':
            return Manager(name=self.name, position=self.position)
        else:
            return Salesman(name=self.name, position=self.position)


class Salesman(User):
    def __init__(self, name, position):
        super(Salesman, self).__init__(name, position)
        self.salesman_main()

    def salesman_main(self):
        salesman_choose = raw_input(('Ok, {}!'
                                     '\n1 - GET ORDER'
                                     '\n2 - LOGOUT'
                                     '\nchose action: ').format(self.name)).upper()
        if salesman_choose in ('1', 'GET ORDER'):
            return Sale(self.name, self.position)
        if salesman_choose in ('2', 'LOGOUT'):
            print 'Logging off...'
            return User()
        else:
            print 'Wrong choice!'
            return self.salesman_main()


class Sale(User):
    def __init__(self, name, position):
        super(Sale, self).__init__(name, position)
        self.sale_list = []
        self.beverage_options = coffee_for_me.return_beverage_dict()
        self.collect_order()

    def collect_order(self):
        func_option = {'SUBMIT': self.submit_order}
        print coffee_for_me.view_menu()
        while True:
            choose = raw_input('\nTo submit print "SUBMIT": ').upper()
            for choose in choose.split():
                if choose in func_option.keys():
                    if self.sale_list_empty_check():
                        continue
                    return func_option[choose]()
                if choose in self.beverage_options.keys():
                    beverage = self.beverage_options[choose]
                    self.sale_list.append(beverage)
                    print 'Adding {} by price - {}'.format(beverage.name, beverage.price)
                else:
                    print "Please, choose from provided option!"

    def sale_list_empty_check(self):
        if not self.sale_list:
            print "Order list is empty!"
            return True

    def submit_order(self):
        print 'Submitting order...'
        coffee_for_me.rewrite_table_sales(self.name, self.sale_list)
        return self.ask_for_check(self.sale_list)

    def ask_for_check(self, sale_list):
        choose = raw_input('Printing check?(Y/n): ')
        if choose.upper() == 'Y':
            print coffee_for_me.get_overall_price(sale_list)
            return Salesman(self.name, self.position)


class Manager(User):
    def __init__(self, name, position):
        super(Manager, self).__init__(name, position)
        self.manager_main()

    def manager_main(self):
        manager_choose = raw_input(('Ok, {}!'
                                    '\n1 - GET OVERALL STATISTIC'
                                    '\n2 - LOGOUT'
                                    '\nchose action: ').format(self.name)).upper()
        if manager_choose in ('1', 'GET OVERALL STATISTIC'):
            coffee_for_me.return_statistic()
            return self.manager_main()
        if manager_choose in ('2', 'LOGOUT'):
            print 'Logging off...'
            return User()
        else:
            print 'Wrong choice!'
            return self.manager_main()


if __name__ == '__main__':
    User()
