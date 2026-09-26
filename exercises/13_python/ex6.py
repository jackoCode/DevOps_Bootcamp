from random import randrange


def guessing_game() -> None:
    """Guessing game."""
    number_to_guess = randrange(1, 10, 1)

    while True:
        user_input = input('Guess the number (between 1 and 9): ')

        if number_to_guess == int(user_input):
            print('YOU WON!')
            break

        if number_to_guess < int(user_input):
            print('too high')
        if number_to_guess > int(user_input):
            print('to low')


def main():
    guessing_game()


if __name__ == '__main__':
    main()
