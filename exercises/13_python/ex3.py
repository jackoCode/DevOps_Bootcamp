def print_employee_data(employees: list[dict]) -> None:
    """Print name, job and city of each employee."""
    for employee in employees:
        print(f'Name: {employee["name"]}, Job: {employee["job"]}, City: {employee["address"]["city"]}')


def print_country_of_second(employees: list[dict]) -> None:
    """Print the country of the second employee."""
    print(employees[1]['address']['country'])


def main():
    employees = [{
        "name": "Tina",
        "age": 30,
        "birthday": "1990-03-10",
        "job": "DevOps Engineer",
        "address": {
            "city": "New York",
            "country": "USA"
        }
    },
        {
            "name": "Tim",
            "age": 35,
            "birthday": "1985-02-21",
            "job": "Developer",
            "address": {
                "city": "Sydney",
                "country": "Australia"
            }
        }]

    print('Print name, job and city of each employee.')
    print_employee_data(employees)

    print('Print country of the second employee.')
    print_country_of_second(employees)


if __name__ == '__main__':
    main()
