from __future__ import annotations
from collections import Counter
import parse
from dataclasses import dataclass


POINT = tuple[int, int]


@dataclass
class Line:
    x1: int
    x2: int
    y1: int
    y2: int

    @property
    def horizontal(self) -> bool:
        return self.y1 == self.y2

    @property
    def vertical(self) -> bool:
        return self.x1 == self.x2

    @property
    def diagonal(self) -> bool:
        return not self.horizontal and not self.vertical

    def get_points(self, diagonals: bool = False) -> list[POINT]:
        if self.horizontal:
            return self.get_horizontal_points()

        if self.vertical:
            return self.get_vertical_points()

        if diagonals:
            return self.get_diagonal_points()

        return []

    def get_diagonal_points(self):
        delta_x = -1 if self.x1 > self.x2 else 1
        delta_y = -1 if self.y1 > self.y2 else 1
        return [
            (self.x1 + delta_x * i, self.y1 + delta_y * i)
            for i in range(abs(self.x1 - self.x2) + 1)
        ]

    def get_horizontal_points(self):
        return [
            (x, self.y1)
            for x in range(min(self.x1, self.x2), max(self.x1, self.x2) + 1)
        ]

    def get_vertical_points(self):
        return [
            (self.x1, y)
            for y in range(min(self.y1, self.y2), max(self.y1, self.y2) + 1)
        ]


def parse_line(line) -> Line:
    return Line(**parse.parse("{x1:d},{y1:d} -> {x2:d},{y2:d}", line.strip()).named)


def count_overlaps(lines: list[Line], diagonals: bool = False):
    points = []
    for line in lines:
        points.extend(line.get_points(diagonals))

    counts = Counter(points)
    return sum(count > 1 for count in counts.values())


def get_test_data() -> list[Line]:
    return [
        parse_line(line)
        for line in [
            "0, 9 -> 5, 9",
            "8, 0 -> 0, 8",
            "9, 4 -> 3, 4",
            "2, 2 -> 2, 1",
            "7, 0 -> 7, 4",
            "6, 4 -> 2, 0",
            "0, 9 -> 2, 9",
            "3, 4 -> 1, 4",
            "0, 0 -> 8, 8",
            "5, 5 -> 8, 2",
        ]
    ]


def get_input_data() -> list[Line]:
    with open("input.txt", "r") as input_file:
        return [parse_line(line) for line in input_file if line.strip()]


def test_1():
    lines = get_test_data()
    overlaps = count_overlaps(lines)
    assert overlaps == 5


def test_2():
    lines = get_test_data()
    overlaps = count_overlaps(lines, diagonals=True)
    assert overlaps == 12


def solution_1():
    lines = get_input_data()
    overlaps = count_overlaps(lines)
    print(f"Solution 1 is {overlaps}")


def solution_2():
    lines = get_input_data()
    overlaps = count_overlaps(lines, diagonals=True)
    print(f"Solution 2 is {overlaps}")


if __name__ == "__main__":
    test_1()
    solution_1()
    test_2()
    solution_2()
