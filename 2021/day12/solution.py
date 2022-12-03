from __future__ import annotations
from collections import Counter, defaultdict
from typing import Callable, Iterator, Optional


Map = dict[str, set[str]]


def can_visit_again_single_small(visited: list[str], cave: str) -> bool:
    if cave.islower():
        return visited.count(cave) == 0

    return True


def can_visit_again_single_small_twice(visited: list[str], cave: str) -> bool:
    if cave.isupper():
        return True

    match (cave, visited.count(cave)):
        case (_, 0):
            return True

        case ("start" | "end", 1):
            return False

        case (_, 1):
            counts = Counter(filter(str.islower, visited))
            return not any(value > 1 for value in counts.values())

        case _:
            return False


def get_paths_from_cave_to_end(
    cave_map: Map,
    from_cave: str = "start",
    visited: Optional[list[str]] = None,
    can_visit: Callable[[list[str], str], bool] = can_visit_again_single_small,
) -> list[list[str]]:
    paths = []
    visited = visited.copy() if visited else []
    visited.append(from_cave)

    if from_cave == "end":
        return [visited]

    for next_cave in cave_map[from_cave]:
        if can_visit(visited, next_cave):
            branch_paths = get_paths_from_cave_to_end(
                cave_map, next_cave, visited, can_visit
            )
            for path in branch_paths:
                paths.append(path)

    return paths


def get_test_data() -> Map:
    return process_input_data(
        [
            "fs-end",
            "he-DX",
            "fs-he",
            "start-DX",
            "pj-DX",
            "end-zg",
            "zg-sl",
            "zg-pj",
            "pj-he",
            "RW-he",
            "fs-DX",
            "pj-RW",
            "zg-RW",
            "start-pj",
            "he-WI",
            "zg-he",
            "pj-fs",
            "start-RW",
        ]
    )


def get_input_data() -> Map:
    with open("input.txt", "r") as input_file:
        return process_input_data(line.strip() for line in input_file if line.strip())


def process_input_data(data: Iterator[str]) -> Map:
    cave_map = defaultdict(set)
    for connection in data:
        cave_a, cave_b = connection.split("-")
        cave_map[cave_a].add(cave_b)
        cave_map[cave_b].add(cave_a)

    return cave_map


def get_solution_1_result(cave_map: Map) -> int:
    return len(get_paths_from_cave_to_end(cave_map))


def test_1():
    data = get_test_data()
    result = get_solution_1_result(data)
    try:
        assert result == 226
    except AssertionError as e:
        print("FAILED RESULT", result)
        raise


def solution_1():
    data = get_input_data()
    result = get_solution_1_result(data)
    print(f"Solution 1 is {result}")


# ### Solution 2 ### #


def get_solution_2_result(cave_map: Map) -> int:
    return len(get_paths_from_cave_to_end(cave_map, can_visit=can_visit_again_single_small_twice))


def test_2():
    data = get_test_data()
    result = get_solution_2_result(data)
    try:
        assert result == 3509
    except AssertionError as e:
        print("FAILED RESULT", result)
        raise


def solution_2():
    data = get_input_data()
    result = get_solution_2_result(data)
    print(f"Solution 2 is {result}")


if __name__ == "__main__":
    test_1()
    solution_1()
    test_2()
    solution_2()
