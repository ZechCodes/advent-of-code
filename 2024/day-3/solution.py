import operator
import re
from enum import StrEnum
from itertools import starmap
from pathlib import Path
from typing import Generator


class StatusAction(StrEnum):
    DO = "do()"
    DONT = "don't()"


def solve_part_1(memory: str) -> int:
    return sum(
        starmap(
            operator.mul,
            get_multiplications(memory)
        )
    )


def solve_part_2(memory: str) -> int:
    return sum(
        starmap(
            operator.mul,
            get_enabled_multiplications(memory)
        )
    )


def get_multiplications(memory: str) -> Generator[tuple[int, int], None, None]:
    for a, b in re.findall(r"mul\((\d+),(\d+)\)", memory):
        yield int(a), int(b)


def get_enabled_multiplications(memory: str) -> Generator[tuple[int, int], None, None]:
    enabled = True
    for result in re.finditer(r"(do)\(\)|(don't)\(\)|mul\((\d+),(\d+)\)", memory):
        match result.group():
            case StatusAction.DO:
                enabled = True
            case StatusAction.DONT:
                enabled = False
            case _ if enabled:
                yield map(int, result.groups()[-2:])


def parse_input(file_name: str) -> str:
    with (Path(__file__).parent / file_name).open() as file:
        return file.read()


assert solve_part_1(parse_input("example_input_1.txt")) == 161
print(solve_part_1(parse_input("puzzle_input.txt")))


assert solve_part_2(parse_input("example_input_2.txt")) == 48
print(solve_part_2(parse_input("puzzle_input.txt")))
