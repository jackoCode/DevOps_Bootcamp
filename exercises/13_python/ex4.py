def find_youngest_employee(employees: list[dict]) -> None:
    """Find the youngest employee in the list."""
    name_age: dict = {}

    for employee in employees:
        name_age[employee['name']] = employee['age']

    print(min(name_age.items(), key=lambda item: item[1]))


def count_upper_lower(word: str) -> None:
    """Count number of upper and lower case letters."""
    upper: int = 0
    lower: int = 0

    for i in word:
        if i.isupper():
            upper += 1
        if i.islower():
            lower += 1

    print(f'{upper} upper case and {lower} lower case letters in {word}.')


def is_even(numbers: list[int]) -> None:
    """Print all even numbers form the list."""
    for number in numbers:
        if number % 2 == 0:
            print(number)


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

    print('Youngest employee.')
    find_youngest_employee(employees)

    print('Calculate lower and upper case.')
    count_upper_lower('Hello, World!')

    print('Print even numbers.')
    is_even([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


if __name__ == '__main__':
    main()
