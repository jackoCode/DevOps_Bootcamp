import pandas as pd


def spreadsheets() -> None:
    """Working with spreadsheets."""
    data = pd.read_excel('employees.xlsx')

    sorted_data = data[
        [
            'Name',
            'Years of Experience',
        ]
    ].sort_values(
        by='Years of Experience',
        ascending=False,
    )

    sorted_data.to_excel('employees_sorted.xlsx', index=False)


def main():
    spreadsheets()


if __name__ == '__main__':
    main()
