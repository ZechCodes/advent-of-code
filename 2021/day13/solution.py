from __future__ import annotations
from typing import Callable, Iterator, Optional


Paper = set[tuple[int, int]]
Fold = tuple[str, int]


def do_fold(paper: Paper, fold: Fold) -> Paper:
    axis, coord = fold
    folded_paper = set()
    for x, y in paper:
        if axis == "x" and x > coord:
            x = coord - (x - coord)
        elif axis == "y" and y > coord:
            y = coord - (y - coord)

        folded_paper.add((x, y))

    return folded_paper


def get_final_paper(paper: Paper, folds: list[Fold]) -> Paper:
    for fold in folds:
        paper = do_fold(paper, fold)

    return paper


def get_max_coord(paper: Paper) -> tuple[int, int]:
    return max(x for x, _ in paper), max(y for _, y in paper)


def print_paper(paper: Paper):
    max_x, max_y = get_max_coord(paper)
    for y in range(max_y + 1):
        print("".join("#" if (x, y) in paper else "." for x in range(max_x + 1)))


def get_test_data() -> tuple[Paper, list[Fold]]:
    return process_input_data(
        [
            "6,10",
            "0,14",
            "9,10",
            "0,3",
            "10,4",
            "4,11",
            "6,0",
            "6,12",
            "4,1",
            "0,13",
            "10,12",
            "3,4",
            "3,0",
            "8,4",
            "1,10",
            "2,14",
            "8,10",
            "9,0",
            "",
            "fold along y=7",
            "fold along x=5",
        ]
    )


def get_input_data() -> tuple[Paper, list[Fold]]:
    with open("input.txt", "r") as input_file:
        return process_input_data(line.strip() for line in input_file if line.strip())


def process_input_data(data: Iterator[str]) -> tuple[Paper, list[Fold]]:
    paper = set()
    folds = []
    for line in data:
        if line.startswith("fold"):
            axis, coord = line.split()[-1].split("=")
            folds.append((axis, int(coord)))
        elif line:
            x, y = map(int, line.split(","))
            paper.add((x, y))

    return paper, folds


# ### Solution 1 ### #


def get_solution_1_result(paper: Paper, folds: list[Fold]) -> int:
    return len(do_fold(paper, folds[0]))


def test_1():
    paper, folds = get_test_data()
    result = get_solution_1_result(paper, folds)
    try:
        assert result == 17
    except AssertionError as e:
        print("FAILED RESULT", result)
        raise


def solution_1():
    paper, folds = get_input_data()
    result = get_solution_1_result(paper, folds)
    print(f"Solution 1 is {result}")


# ### Solution 2 ### #


def test_2():
    print(f"Test 2 is:")
    paper, folds = get_test_data()
    folded_paper = get_final_paper(paper, folds[:2])
    print_paper(folded_paper)


def solution_2():
    print(f"Solution 2 is:")
    paper, folds = get_input_data()
    folded_paper = get_final_paper(paper, folds)
    print_paper(folded_paper)


if __name__ == "__main__":
    test_1()
    solution_1()
    test_2()
    solution_2()
