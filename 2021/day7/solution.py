from __future__ import annotations
from statistics import median_low


def calculate_least_fuel(crabs: list[int]) -> int:
    alignment_point = median_low(crabs)
    return sum(abs(alignment_point - position) for position in crabs)


def calculate_fuel_cost_part_2(distance: int) -> int:
    return int(distance / 2 * (distance + 1))


def calculate_least_fuel_part_2(crabs: list[int]) -> int:
    def generate_possibilities():
        for point in range(min(crabs), max(crabs) + 1):
            yield sum(
                calculate_fuel_cost_part_2(abs(point - position)) for position in crabs
            )

    return min(generate_possibilities())


def get_test_data() -> list[int]:
    return [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]


def get_input_data() -> list[int]:
    with open("input.txt", "r") as input_file:
        return [int(crab) for crab in input_file.readline().split(",")]


def test_1():
    crabs = get_test_data()
    fuel = calculate_least_fuel(crabs)
    assert fuel == 37


def test_2():
    crabs = get_test_data()
    fuel = calculate_least_fuel_part_2(crabs)
    assert fuel == 168


def solution_1():
    crabs = get_input_data()
    fuel = calculate_least_fuel(crabs)
    print(f"Solution 1 is {fuel}")


def solution_2():
    crabs = get_input_data()
    fuel = calculate_least_fuel_part_2(crabs)
    print(f"Solution 2 is {fuel}")


if __name__ == "__main__":
    test_1()
    solution_1()
    test_2()
    solution_2()
