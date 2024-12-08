import operator
from functools import wraps
from itertools import product
from pathlib import Path
from typing import Generator, Callable


def output[**P](func: Callable[P, int]) -> Callable[P, int]:
    @wraps(func)
    def call_and_print(*args: P.args, **kwargs: P.kwargs) -> int:
        result = func(*args, **kwargs)
        print(f"{func.__name__} => {result}")
        return result

    return call_and_print


@output
def solve_part_1(tests: list[tuple[int, list[int]]]) -> int:
    valid_tests_results = find_valid_test_results(tests, [operator.mul, operator.add])
    return sum(valid_tests_results)


@output
def solve_part_2(tests: list[tuple[int, list[int]]]) -> int:
    valid_tests_results = find_valid_test_results(tests, [operator.mul, operator.add, concatenate_operator])
    return sum(valid_tests_results)


def find_valid_test_results(
    tests: list[tuple[int, list[int]]],
    operators: list[Callable[[int, int], int]]
) -> Generator[int, None, None]:
    for result, numbers in tests:
        for ops in product(operators, repeat=len(numbers) - 1):
            test_result = evaluate_with_operators(numbers, ops)
            if test_result == result:
                yield result
                break


def evaluate_with_operators(numbers: list[int], operators: tuple[Callable[[int, int], int], ...]) -> int:
    result = numbers[0]
    for number, op in zip(numbers[1:], operators):
        result = op(result, number)

    return result


def concatenate_operator(a: int, b: int) -> int:
    return int(f"{a}{b}")


def parse_input(file_name: str) -> list[tuple[int, list[int]]]:
    with (Path(__file__).parent / file_name).open() as file:
        return [
            (int(result), [int(n) for n in numbers.strip().split(" ")])
            for result, numbers in (line.split(":") for line in file)
        ]


assert solve_part_1(parse_input("example_input.txt")) == 3749
solve_part_1(parse_input("puzzle_input.txt"))

assert solve_part_2(parse_input("example_input.txt")) == 11387
solve_part_2(parse_input("puzzle_input.txt"))
