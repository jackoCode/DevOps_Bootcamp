from ex4 import find_youngest_employee, count_upper_lower, is_even


def main():
    find_youngest_employee([{
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
        }])

    count_upper_lower('Hello')

    is_even([12, 13, 14, 15, 16, 17, 18, 19, 20])


if __name__ == '__main__':
    main()
