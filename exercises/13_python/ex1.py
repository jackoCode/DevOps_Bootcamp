def print_greater_equal_ten(integers: list[int]) -> None:
    """Print all integers of the list which are >= 10."""
    for integer in integers:
        if integer >= 10:
            print(integer)


def print_new_greater_equal_ten_list(integers: list[int]) -> None:
    """Create and print a new list with integers >= 10."""
    new_integers: list[int] = []

    for integer in integers:
        if integer >= 10:
            new_integers.append(integer)

    print(new_integers)


def print_higher_than_input(integers: list[int]) -> None:
    """Print all integers greater than the user input."""
    user_input = input('Choose a number: ')

    for integer in integers:
        if integer > int(user_input):
            print(integer)


def main():
    my_list = [1, 2, 2, 4, 4, 5, 6, 8, 10, 13, 22, 35, 52, 83]

    print('Print all elements greater or equal to 10')
    print_greater_equal_ten(my_list)

    print('Print new list of integers >= 10.')
    print_new_greater_equal_ten_list(my_list)

    print('Print integers greater than the user input.')
    print_higher_than_input(my_list)


if __name__ == '__main__':
    main()
