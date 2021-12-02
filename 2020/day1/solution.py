from itertools import product
from math import prod


def fix_expense_report(report: list[int]) -> int:
    for value_a, value_b in product(report, repeat=2):
        if value_a + value_b == 2020:
            return value_a * value_b

    return -1


def product_three_sum_2020(report: list[int]) -> int:
    for values in product(report, repeat=3):
        if sum(values) == 2020:
            return prod(values)

    return -1


if __name__ == "__main__":
    import pathlib

    with (pathlib.Path(__file__).parent / "input.txt").open() as expense_report:
        expenses = [int(line.strip()) for line in expense_report if line.strip()]
        print(fix_expense_report(expenses))
        print(product_three_sum_2020(expenses))
