from datetime import datetime


def time_to_birthday(birthday: datetime) -> None:
    """Calculate days, hours, minutes are remaining till birthday."""
    birthday = birthday.replace(year=datetime.today().year + 1)
    today = datetime.today()

    time_to_next_birthday = birthday - today

    print(
        f'There are '
        f'{time_to_next_birthday.days} days, '
        f'{time_to_next_birthday.seconds // 3600} hours and '
        f'{(time_to_next_birthday.seconds % 3600) // 60} minutes to your next birthday.'
    )


def main():
    time_to_birthday(datetime(1982, 8, 20))


if __name__ == '__main__':
    main()
