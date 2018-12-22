import argparse
from configured_logger import *
from input_menu import InputNameAndPosition


def create_parser():
    """Parse for optional argument:
    '-n' '--name' to get name
    '-p' '--position' to get position (variants are 'salesman', 'manager')
    if combination of name and position is not found in database, new user will be created
    """
    try:
        pars = argparse.ArgumentParser()
        pars.add_argument('-n', '--name',
                          help="space for the user's name")
        pars.add_argument('-p', '--position',
                          choices=['salesman', 'manager'],
                          help="space for the user's position")
        return pars
    except Exception as exc:
        logger.error("'{}' while executing the method 'create_parser'".format(exc))
        quit()


if __name__ == '__main__':
    parser = create_parser()
    name_space = parser.parse_args()
    user = InputNameAndPosition(name=name_space.name, position=name_space.position)
    user.entrance()
