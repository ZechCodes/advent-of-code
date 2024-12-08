from collections.abc import Callable
from functools import wraps
from pathlib import Path


def output[**P](func: Callable[P, int]) -> Callable[P, int]:
    @wraps
    def call_and_print(*args: P.args, **kwargs: P.kwargs) -> int:
        result = func(*args, **kwargs)
        print(f"{func.__name__} => {result}")
        return result

    return call_and_print


@output
def solve_part_1() -> int:
    return 0


@output
def solve_part_2() -> int:
    return 0


def parse_input(file_name: str):
    with (Path(__file__).parent / file_name).open() as file:
        return


assert solve_part_1(parse_input("example_input.txt")) == 0
solve_part_1(parse_input("puzzle_input.txt"))

assert solve_part_2(parse_input("example_input.txt")) == 0
solve_part_2(parse_input("puzzle_input.txt"))
