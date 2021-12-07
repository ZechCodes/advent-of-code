from __future__ import annotations
from collections import deque


def get_number_of_fish(fish: list[int], generations: int) -> int:
    fish_counts = consolidate_fish_to_days(fish)
    return run_generations(fish_counts, generations)


def consolidate_fish_to_days(fish: list[int]) -> list[int]:
    days = [0] * 7
    for day in fish:
        days[day] += 1

    return days


def run_generations(days: list[int], generations: int):
    babies = deque([0] * 2)
    fish = deque(days)
    for _ in range(generations):
        baby_fish = babies.popleft()
        parent_fish = fish.popleft()
        babies.append(parent_fish)
        fish.append(parent_fish + baby_fish)

    return sum(fish) + sum(babies)


def get_test_data() -> list[int]:
    return [3, 4, 3, 1, 2]


def get_input_data() -> list[int]:
    with open("input.txt", "r") as input_file:
        return [int(fish) for fish in input_file.readline().split(",")]


def test_1():
    fish = get_test_data()
    total = get_number_of_fish(fish, 80)
    print(total)
    assert total == 5934


def test_2():
    fish = get_test_data()
    total = get_number_of_fish(fish, 256)
    assert total == 26984457539


def solution_1():
    fish = get_input_data()
    total = get_number_of_fish(fish, 80)
    print(f"Solution 1 is {total}")


def solution_2():
    fish = get_input_data()
    total = get_number_of_fish(fish, 256)
    print(f"Solution 2 is {total}")


if __name__ == "__main__":
    test_1()
    solution_1()
    test_2()
    solution_2()
