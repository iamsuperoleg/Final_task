# -*- coding: utf-8 -*-


class GetMenu(object):

    def __init__(self, rowid, name, price):
        self.rowid = rowid
        self.name = name
        self.price = price

    def get_tuple_to_menu(self):
        return self.rowid, self.name, self.price
