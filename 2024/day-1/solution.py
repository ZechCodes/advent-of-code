from pathlib import Path
from typing import Generator


def solve_part_1(left: list[int], right: list[int]) -> int:
    distances = get_distances(left, right)
    return sum(distances)


def solve_part_2(left: list[int], right: list[int]) -> int:
    similarity = get_similarity(left, right)
    return sum(similarity)


def get_distances(left: list[int], right: list[int]) -> Generator[int, None, None]:
    for a, b in zip(*map(sorted, (left, right))):
        yield abs(a - b)


def get_similarity(left: list[int], right: list[int]) -> Generator[int, None, None]:
    for n in left:
        yield n * right.count(n)


def parse_input(file_name: str) -> tuple[list[int], list[int]]:
    left, right = [], []
    with (Path(__file__).parent / file_name).open() as f:
        for line in f:
            left_number, right_number = map(str.strip, line.split(maxsplit=1))
            left.append(int(left_number))
            right.append(int(right_number))

    return left, right


example = [3, 4, 2, 1, 3, 3], [4, 3, 5, 3, 9, 3]
assert solve_part_1(*example) == 11
print(solve_part_1(*parse_input("puzzle_input.txt")))


assert solve_part_2(*example) == 31
print(solve_part_2(*parse_input("puzzle_input.txt")))
