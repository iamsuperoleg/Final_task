import argparse
from input_menu import InputNameAndPosition


def create_parser():
    """Parse for optional argument:
    '-n' '--name' to get name
    '-p' '--position' to get position (variants are 'salesman', 'manager')
    if combination of name and position is not found in database, new user will be created
    """
    pars = argparse.ArgumentParser()
    pars.add_argument('-n', '--name', type=str, help="space for user's name")
    pars.add_argument('-p', '--position', choices=['salesman', 'manager'], type=str,
                        help="space for user's position")

    return parser


if __name__ == '__main__':
    parser = create_parser()
    name_space = parser.parse_args()
    user = InputNameAndPosition(name=name_space.name, position=name_space.position)
    user.entrance()
