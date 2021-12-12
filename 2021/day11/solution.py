from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from typing import Iterator


class Map:
    def __init__(self):
        self._octopi = {}

    @property
    def num_octopi(self) -> int:
        return len(self._octopi)

    def add_octopus(self, x: int, y: int, power: int):
        self._octopi[(x, y)] = Octopus(x, y, power, self)

    def get(self, x: int, y: int) -> Octopus:
        return self._octopi.get((x, y), NullOctopus())

    def get_num_flashes_this_cycle(self) -> int:
        for octopus in self._octopi.values():
            octopus.give_energy()

        return sum(octopus.update() for octopus in self._octopi.values())

    def get_num_flashes_after_cycling(self, cycles: int) -> int:
        total = 0
        for _ in range(cycles):
            total += self.get_num_flashes_this_cycle()

        return total

    def get_cycle_of_synchronization(self) -> int:
        cycle = 1
        while self.num_octopi != self.get_num_flashes_this_cycle():
            cycle += 1

        return cycle

    @classmethod
    def create_map(cls, data: list[list[int]]) -> Map:
        octopus_map = cls()
        for y, row in enumerate(data):
            for x, power in enumerate(row):
                octopus_map.add_octopus(x, y, power)

        return octopus_map


@dataclass
class Octopus:
    x: int
    y: int
    power: int
    map: Map

    @property
    def flashed(self) -> bool:
        return self.power >= 9

    @property
    def neighbors(self) -> list[Octopus]:
        neighbors = []
        for delta_x, delta_y in filter(any, product((0, 1, -1), repeat=2)):
            neighbor = self.map.get(self.x + delta_x, self.y + delta_y)
            if not isinstance(neighbor, NullOctopus):
                neighbors.append(neighbor)

        return neighbors

    def flash(self):
        for neighbor in self.neighbors:
            neighbor.give_energy()

    def give_energy(self):
        self.power += 1

        if self.power == 10:
            self.flash()

    def update(self) -> bool:
        if self.power > 9:
            self.power = 0
            return True

        return False


class NullOctopus(Octopus):
    def __init__(self, *_, **__):
        ...


def get_test_data() -> list[list[int]]:
    return process_input_data(
        [
            "5483143223",
            "2745854711",
            "5264556173",
            "6141336146",
            "6357385478",
            "4167524645",
            "2176841721",
            "6882881134",
            "4846848554",
            "5283751526",
        ]
    )


def get_input_data() -> list[list[int]]:
    with open("input.txt", "r") as input_file:
        return process_input_data(input_file)


def process_input_data(data: Iterator[str]) -> list[list[int]]:
    return [[int(char) for char in line.strip()] for line in data]


def get_solution_1_result(octopi_power_levels: list[list[int]]) -> int:
    return Map.create_map(octopi_power_levels).get_num_flashes_after_cycling(100)


def test_1():
    data = get_test_data()
    result = get_solution_1_result(data)
    try:
        assert result == 1656
    except AssertionError:
        print("FAILED RESULT", result)
        raise


def solution_1():
    data = get_input_data()
    result = get_solution_1_result(data)
    print(f"Solution 1 is {result}")


# ### Solution 2 ### #


def get_solution_2_result(octopi_power_levels: list[list[int]]) -> int:
    return Map.create_map(octopi_power_levels).get_cycle_of_synchronization()


def test_2():
    data = get_test_data()
    result = get_solution_2_result(data)
    assert result == 195


def solution_2():
    data = get_input_data()
    result = get_solution_2_result(data)
    print(f"Solution 2 is {result}")


if __name__ == "__main__":
    test_1()
    solution_1()
    test_2()
    solution_2()
