from typing import Generator
import io
import itertools
import pathlib


def process_input(input_file: io.TextIOWrapper):
    return [
        list(line.strip())
        for line in input_file
        if line.strip()
    ]


def get_neighbors(row: int, column: int, grid: list[list[str]]) -> list[str]:
    neighbors = []
    for row_move, column_move in itertools.product((-1, 0, 1), repeat=2):
        if row_move == 0 and column_move == 0:
            continue

        for distance in range(1, min(len(grid), len(grid[0]))):
            r = row + row_move * distance
            c = column + column_move * distance
            if (
                0 <= r < len(grid) and
                0 <= c < len(grid[0]) and
                grid[r][c] != "."
            ):
                neighbors.append(grid[r][c])
                break

    return neighbors


def iterate_grid(grid: list[list[str]]) -> Generator[None, list[list[str]], None]:
    previous_grid, current_grid = grid, recompute_grid(grid)
    yield current_grid
    while previous_grid != current_grid:
        previous_grid, current_grid = current_grid, recompute_grid(current_grid)
        yield current_grid


def recompute_grid(grid: list[list[str]]) -> list[list[str]]:
    new_grid = []
    for row_index, row in enumerate(grid):
        new_grid.append([])
        for column_index, space in enumerate(row):
            new_grid[row_index].append(
                iterate_space(
                    space,
                    get_neighbors(row_index, column_index, grid)
                )
            )

    return new_grid


def iterate_space(value: str, neighbors: list[str]) -> str:
    if value == "L" and all(neighbor != "#" for neighbor in neighbors):
        return "#"

    if value == "#" and sum(neighbor == "#" for neighbor in neighbors) >= 5:
        return "L"

    return value


def find_final_occupation(grid: list[list[str]]) -> int:
    return sum(space == "#" for space in itertools.chain(*list(iterate_grid(grid))[-1]))


if __name__ == "__main__":
    input_file_path = pathlib.Path(__file__).parent / "test_input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print("Test A")
    print(find_final_occupation(input_data), 26)

    input_file_path = pathlib.Path(__file__).parent / "input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print("\nFinal")
    print(find_final_occupation(input_data))
