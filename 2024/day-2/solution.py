import operator
from itertools import pairwise, starmap
from pathlib import Path
from typing import Any,  Sequence


type Report = tuple[int, ...]


def solve_part_1(reports: list[Report]) -> int:
    return len(list(filter(is_safe, reports)))


def solve_part_2(reports: list[Report]) -> int:
    return len(list(filter(is_mostly_safe, reports)))


def is_monotonic(sequence: Sequence[Any]) -> bool:
    if len(sequence) < 2:
        return True

    direction = operator.le if sequence[0] < sequence[1] else operator.ge
    return all(starmap(direction,  pairwise(sequence)))


def is_safe(report: Report) -> bool:
    if not is_monotonic(report):
        return False

    return all(1 <= abs(a - b) <= 3 for a, b in pairwise(report))


def is_mostly_safe(report: Report) -> bool:
    if is_safe(report):
        return True

    for i in range(len(report)):
        if is_safe(report[:i] + report[i + 1:]):
            return True

    else:
        return False


def parse_input(file_name: str) -> list[Report]:
    return [
        tuple(map(int, line.strip().split()))
        for line in Path(file_name).read_text().strip().splitlines()
    ]


assert solve_part_1(parse_input("example_input.txt")) == 2
print(solve_part_1(parse_input("puzzle_input.txt")))


assert solve_part_2(parse_input("example_input.txt")) == 4
print(solve_part_2(parse_input("puzzle_input.txt")))
