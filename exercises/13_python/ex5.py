def calculator() -> None:
    """Calculator"""
    calculation_count = 0

    while True:
        print('Type "exit" to quit.')

        first_input = input('Enter the first number: ')

        if first_input.lower() == 'exit':
            break

        try:
            first_number = float(first_input)
        except ValueError:
            print('Invalid input. Only numbers are allowed.')
            continue

        operation = input('Enter operation (+, -, *, /): ')

        if operation.lower() == 'exit':
            break

        if operation not in ['+', '-', '*', '/']:
            print('Invalid operation. Please use +, -, *, or /.')
            continue

        second_input = input('Enter the second number: ')

        if second_input.lower() == 'exit':
            break

        try:
            second_number = float(second_input)
        except ValueError:
            print('Invalid input. Only numbers are allowed.')
            continue

        result = None

        if operation == '+':
            result = first_number + second_number
        elif operation == '-':
            result = first_number - second_number
        elif operation == '*':
            result = first_number * second_number
        elif operation == '/':
            if second_number == 0:
                print('Cannot divide by zero.')
                continue
            result = first_number / second_number

        print(f'Result: {result}')

        calculation_count += 1

    print(f'Performed calculations: {calculation_count}')


def main():
    calculator()


if __name__ == '__main__':
    main()
