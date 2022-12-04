from pathlib import Path
from functools import partial


def parse() -> list[tuple[set[int], set[int]]]:
    with Path("assignments-data.txt").open("r") as data_file:
        return [
            (_parse_range(assignment_a), _parse_range(assignment_b))
            for assignment_a, assignment_b in map(
                partial(str.split, sep=","),
                data_file,
            )
        ]


def _parse_range(assignment: str) -> set[int]:
    return _make_range(*map(int, assignment.split("-")))


def _make_range(start: int, end: int) -> set[int]:
    return set(range(start, end + 1))
