from __future__ import annotations
from typing import Iterator


CAVE_MAP = list[list[int]]


def cache(func):
    _cache = {}

    def wrapper(cm, x=0, y=0, v=None):
        if (x, y) not in _cache:
            _cache[(x, y)] = func(cm, x, y, v)

        return _cache[(x, y)]

    return wrapper


@cache
def find_best_path(
    cave_map: CAVE_MAP,
    x: int = -1,
    y: int = -1,
    visited: list[tuple[int, int]] | None = None,
):
    x, y = x if x >= 0 else len(cave_map[0]), y if y >= 0 else len(cave_map)
    visited = visited or []
    visited.append((x, y))
    if x == len(cave_map[0]) - 1 and y == len(cave_map) - 1:
        print(visited)
        return 0

    best = -1
    for delta_x, delta_y in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        next_x, next_y = delta_x + x, delta_y + y
        if (
            0 <= next_x < len(cave_map[0])
            and 0 <= next_y < len(cave_map)
            and (next_x, next_y) not in visited
        ):
            path_score = cave_map[next_y][next_x] + find_best_path(
                cave_map, next_x, next_y, visited.copy()
            )
            if path_score >= 0 and (best == -1 or path_score < best):
                best = path_score

    return best


def get_test_data() -> CAVE_MAP:
    return process_input_data(
        [
            "1163751742",
            "1381373672",
            "2136511328",
            "3694931569",
            "7463417111",
            "1319128137",
            "1359912421",
            "3125421639",
            "1293138521",
            "2311944581",
        ]
    )


def get_input_data() -> CAVE_MAP:
    with open("input.txt", "r") as input_file:
        return process_input_data(line.strip() for line in input_file if line.strip())


def process_input_data(data: Iterator[str]) -> CAVE_MAP:
    return [[int(c) for c in row] for row in data]


# ### Solution 1 ### #


def get_solution_1_result(cave_map: CAVE_MAP) -> int:
    best_path = find_best_path(cave_map)
    return best_path


def test_1():
    data = get_test_data()
    result = get_solution_1_result(data)
    try:
        assert result == 40
    except AssertionError as e:
        print("FAILED RESULT", result)
        raise


def solution_1():
    data = get_input_data()
    result = get_solution_1_result(*data)
    print(f"Solution 1 is {result}")


# ### Solution 2 ### #


def get_solution_2_result(cave_map: CAVE_MAP) -> int:
    frequencies = get_polymer_element_frequencies(template, rules, 40)
    counts = get_element_counts(frequencies, template)
    return max(counts.values()) - min(counts.values())


def test_2():
    data = get_test_data()
    result = get_solution_2_result(*data)
    try:
        assert result == 2188189693529
    except AssertionError as e:
        print("FAILED RESULT", result, 2188189693529, 2188189693529 - result)
        raise


def solution_2():
    data = get_input_data()
    result = get_solution_2_result(*data)
    print(f"Solution 2 is {result}")


if __name__ == "__main__":
    test_1()
    solution_1()
    # test_2()
    # solution_2()
