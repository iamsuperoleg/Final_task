import unittest
from data_base_handler import DataBaseHandler
from get_product_list import GetProductList

COFFEE_PRICE = [(1, 'CAPPUCCINO', 5), (2, 'LATTE', 6), (3, 'ESPRESSO', 4)]
ADDITIVE_PRICE = [(1, 'CINNAMON', 1.1), (2, 'SUGAR', 0.11), (3, 'MILK', 0.99)]


class TestHandler(unittest.TestCase):
    def setUp(self):
        self.data_base_handler = DataBaseHandler()

    def test_get_overall_price(self):
        sale_list1 = []
        sale_list2 = []
        coffee_list = [GetProductList(rowid, name, price) for rowid, name, price in COFFEE_PRICE]
        coffee_dict = {str(additive.rowid): additive for additive in coffee_list}
        for coffee in coffee_dict.values():
            sale_list1.append(coffee)
        total_price1 = self.data_base_handler.get_overall_price(sale_list1)
        for value in COFFEE_PRICE:
            sale_list2.append(value[2])
        total_price2 = sum(sale_list2)
        self.assertEqual(total_price1, total_price2)


if __name__ == '__main__':
    unittest.main()
