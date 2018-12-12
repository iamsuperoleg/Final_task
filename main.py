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
            position = raw_input(
                ("Hello, {}! "
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
        user_tuple = self.name, self.position
        coffee_for_me.add_user(user_tuple)


if __name__ == '__main__':
    User()
