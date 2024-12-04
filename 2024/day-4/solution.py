from pathlib import Path

type LetterGridRow = list[str]
type LetterGrid = list[LetterGridRow]


def solve_part_1(grid: LetterGrid) -> int:
    return count_word_occurrences("XMAS", grid)


def solve_part_2(grid: LetterGrid) -> int:
    count = 0
    for y, row in enumerate(grid[1:-1], start=1):
        for x, value in enumerate(row[1:-1], start=1):
            if value != "A":
                continue

            top_right = {grid[y - 1][x - 1], grid[y + 1][x + 1]}
            top_left = {grid[y - 1][x + 1], grid[y + 1][x - 1]}
            if top_right == {"M", "S"} == top_left:
                count += 1

    return count



def count_word_occurrences(word: str, grid: LetterGrid) -> int:
    return (
        count_word_occurrences_across(word, grid) +
        count_word_occurrences_down(word, grid) +
        count_word_occurrences_diagonal(word, grid)
    )

def count_word_occurrences_across(word: str, grid: LetterGrid) -> int:
    return count_word_occurrence_in_rows(word, grid)


def count_word_occurrences_down(word: str, grid: LetterGrid) -> int:
    return count_word_occurrence_in_rows(word, rotate_90(grid))


def count_word_occurrences_diagonal(word: str, grid: LetterGrid) -> int:
    return (
        count_word_occurrence_in_rows(word, rotate_45(grid)) +
        count_word_occurrence_in_rows(word, rotate_45(rotate_90(grid)))
    )


def count_word_occurrence_in_rows(word: str, grid: LetterGrid) -> int:
    return sum(
        (
            count_word_occurrences_in_string(word, "".join(row)) +
            count_word_occurrences_in_string(word, "".join(row[::-1]))
        ) for row in grid
    )


def count_word_occurrences_in_string(word: str, string: str) -> int:
    return string.count(word)


def rotate_45[T](matrix: list[list[T]]) -> list[list[T]]:
    rotated = []
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if i + j >= len(rotated):
                rotated.append([])

            rotated[i + j].append(value)

    return rotated


def rotate_90[T](matrix: list[list[T]]) -> list[list[T]]:
    return [
        list(row)
        for row in zip(*matrix[::-1])
    ]


def flip[T](matrix: list[list[T]]) -> list[list[T]]:
    return [
        row[::-1]
        for row in matrix
    ]


def parse_input(file_name: str) -> LetterGrid:
    with (Path(__file__).parent / file_name).open() as file:
        return [
            list(line.strip())
            for line in file.readlines()
        ]


assert solve_part_1(parse_input("example_input.txt")) == 18
print(solve_part_1(parse_input("puzzle_input.txt")))

assert solve_part_2(parse_input("example_input.txt")) == 9
print(solve_part_2(parse_input("puzzle_input.txt")))
