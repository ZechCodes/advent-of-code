from __future__ import annotations
from dataclasses import dataclass
from math import prod
from typing import Iterator


class Map:
    def __init__(self):
        self._points: dict[tuple[int, int], Point] = {}

    def add_point(self, x: int, y: int, height: int):
        self._points[(x, y)] = Point(x, y, height, self)

    def get_basins(self) -> list[set[Point]]:
        basins = []
        checked = set()
        for point in self._points.values():
            if point in checked:
                continue

            if point.height == 9:
                continue

            basin = self._get_points_in_basin(point)
            checked.update(basin)
            basins.append(basin)

        return sorted(basins, key=len, reverse=True)

    def get_low_points(self) -> list[Point]:
        return [point for point in self._points.values() if point.is_low_point()]

    def get_point(self, x: int, y: int) -> Point | None:
        return self._points.get((x, y), NullPoint())

    def _get_points_in_basin(self, start: Point) -> set[Point]:
        points = set()
        need_to_check = {start}
        while need_to_check:
            point = need_to_check.pop()
            if point.height == 9:
                continue

            points.add(point)
            need_to_check.update(point.neighbors - points)

        return points

    @classmethod
    def build(cls, data: Iterator[Iterator[int]]) -> Map:
        new_map = Map()
        for y, row in enumerate(data):
            for x, height in enumerate(row):
                new_map.add_point(x, y, height)

        return new_map


@dataclass
class Point:
    x: int
    y: int
    height: int
    map: Map

    @property
    def neighbors(self) -> set[Point]:
        neighbors = set()
        for delta_x, delta_y in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            point = self.map.get_point(self.x + delta_x, self.y + delta_y)
            if not isinstance(point, NullPoint):
                neighbors.add(point)

        return neighbors

    @property
    def risk_level(self) -> int:
        return self.height + 1

    def is_low_point(self) -> bool:
        return all(neighbor > self for neighbor in self.neighbors)

    def __lt__(self, other: Point):
        return self.height < other.height

    def __gt__(self, other: Point):
        return self.height > other.height

    def __eq__(self, other: Point):
        return self.height == other.height

    def __hash__(self):
        return hash((self.x, self.y))


class NullPoint(Point):
    _null_instance = None

    def __new__(cls, *args, **kwargs):
        if cls._null_instance is None:
            cls._null_instance = super().__new__(cls, *args, **kwargs)

        return cls._null_instance

    def __init__(self, *_, **__):
        self.height = -1
        self.x = -1
        self.y = -1

    def is_low_point(self) -> bool:
        return False

    def __lt__(self, _: Point):
        return False

    def __gt__(self, _: Point):
        return True

    def __eq__(self, _: Point):
        return False


def get_test_data() -> Map:
    data = [
        "2199943210",
        "3987894921",
        "9856789892",
        "8767896789",
        "9899965678",
    ]

    return Map.build(map(int, row) for row in data)


def get_input_data() -> Map:
    with open("input.txt", "r") as input_file:
        return Map.build(map(int, row.strip()) for row in input_file)


def get_solution_1_result(height_map: Map) -> int:
    return sum(point.risk_level for point in height_map.get_low_points())


def test_1():
    height_map = get_test_data()
    result = get_solution_1_result(height_map)
    assert result == 15


def solution_1():
    height_map = get_input_data()
    result = get_solution_1_result(height_map)
    print(f"Solution 1 is {result}")


# ### Solution 2 ### #


def get_solution_2_result(height_map: Map) -> int:
    return prod(len(basin) for basin in height_map.get_basins()[:3])


def test_2():
    height_map = get_test_data()
    result = get_solution_2_result(height_map)
    assert result == 1134


def solution_2():
    height_map = get_input_data()
    result = get_solution_2_result(height_map)
    print(f"Solution 2 is {result}")


if __name__ == "__main__":
    test_1()
    solution_1()
    test_2()
    solution_2()
