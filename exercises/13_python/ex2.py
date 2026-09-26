def update_dict(employee: dict) -> None:
    """Update the given dictionary."""
    employee['job'] = 'Software Engineer'
    employee.pop('age')

    for key, value in employee.items():
        print(f'{key}: {value}')


def merge_dicts(dict_1: dict, dict_2: dict) -> dict:
    """Merge two dictionaries into one."""
    merged_dict: dict = {}

    merged_dict = dict_1 | dict_2
    print(merged_dict)

    return merged_dict


def sum_dict_values(sum_dict: dict) -> None:
    """Sum all values of the dictionary."""
    dict_values_sum: int = 0

    for _, values in sum_dict.items():
        dict_values_sum += values
    print(dict_values_sum)


def print_min_max(merged: dict) -> None:
    """Print the min and max value of the dictionary."""
    print(f'The min value is: {min(merged.values())}')
    print(f'The max value is: {max(merged.values())}')


def main():
    employee = {
        "name": "Tim",
        "age": 30,
        "birthday": "1990-03-10",
        "job": "DevOps Engineer"
    }

    print('Update and print key/value pairs of the dictionary.')
    update_dict(employee)

    dict_one = {'a': 100, 'b': 400}
    dict_two = {'x': 300, 'y': 200}

    print('Merge dictionaries.')
    merged_dict = merge_dicts(dict_one, dict_two)

    print('Sum values.')
    sum_dict_values(merged_dict)

    print('Print min and max value.')
    print_min_max(merged_dict)


if __name__ == '__main__':
    main()
