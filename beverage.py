# -*- coding: utf-8 -*-


class Beverage(object):

    def __init__(self, rowid, name, price):
        self.rowid = rowid
        self.name = name
        self.price = price
        self.number_in_sale_list = 0

    def get_tuple_to_check(self):
        return self.number_in_sale_list, self.name, self.price

    def get_tuple_to_menu(self):
        return self.rowid, self.name, self.price
