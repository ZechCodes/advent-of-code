from itertools import product


def fix_expense_report(report: list[int]) -> int:
    for value_a, value_b in product(report, repeat=2):
        if value_a + value_b == 2020:
            return value_a * value_b

    return -1


if __name__ == "__main__":
    import pathlib

    with (pathlib.Path(__file__).parent / "input.txt").open() as expense_report:
        expenses = [int(line.strip()) for line in expense_report if line.strip()]
        print(fix_expense_report(expenses))
