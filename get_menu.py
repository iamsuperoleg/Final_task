class GetProductList(object):

    def __init__(self, rowid, name, price):
        self.rowid = rowid
        self.name = name
        self.price = price

    def get_tuple_to_product(self):
        return self.rowid, self.name, self.price
