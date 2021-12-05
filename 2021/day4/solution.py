from __future__ import annotations
from io import StringIO
from itertools import filterfalse


class Board:
    def __init__(self):
        self._called_numbers: set[int] = set()

        self._groups: list[CellGroup] = []

    def call_number(self, number: int):
        self._called_numbers.add(number)

    def create_cell_group(self, row_group: bool) -> CellGroup:
        group = CellGroup(row_group)
        self._groups.append(group)
        return group

    def get_score(self) -> int:
        return sum(
            group.get_score(self._called_numbers)
            for group in self._groups
            if group.is_row
        )

    def has_won(self) -> bool:
        return any(group.is_filled(self._called_numbers) for group in self._groups)

    @classmethod
    def build(cls, boards: list[list[int]]) -> Board:
        board = cls()
        columns = [board.create_cell_group(False) for _ in range(5)]
        for row in boards:
            row_group = board.create_cell_group(True)
            for i, cell in enumerate(row):
                row_group.add_cell(cell)
                columns[i].add_cell(cell)

        return board


class BoardGroup:
    def __init__(self, boards: list[Board]):
        self._boards: list[Board] = boards

    def play(self, numbers: list[int]) -> int:
        for number in numbers:
            for board in self._boards:
                board.call_number(number)
                if board.has_won():
                    return number * board.get_score()

        return 0

    def play_for_last_place(self, numbers: list[int]) -> int:
        won = 0
        for number in numbers:
            for board in filterfalse(Board.has_won, self._boards):
                board.call_number(number)
                if board.has_won():
                    won += 1

                    if won == len(self._boards):
                        return number * board.get_score()

        return 0

    @classmethod
    def build(cls, boards: list[list[list[int]]]):
        boards = [Board.build(board) for board in boards]
        return BoardGroup(boards)


class CellGroup:
    def __init__(self, row_group):
        self._cells: set[int] = set()
        self._row_group = row_group

    @property
    def is_row(self) -> bool:
        return self._row_group

    def add_cell(self, number: int):
        self._cells.add(number)

    def get_score(self, called_numbers: set[int]) -> int:
        return sum(self._cells.difference(called_numbers))

    def is_filled(self, called_numbers: set[int]) -> bool:
        return len(self._cells.difference(called_numbers)) == 0


def get_input_data() -> tuple[BoardGroup, list[int]]:
    with open("input.txt", "r") as input_file:
        numbers = [int(n) for n in input_file.readline().split(",")]
        input_file.readline()
        board_group = BoardGroup.build(parse_boards(input_file))
        return board_group, numbers


def parse_boards(raw_input: StringIO) -> list[list[list[int]]]:
    boards = [[]]
    for line in raw_input:
        if not line.strip():
            boards.append([])
            continue

        boards[-1].append([int(n) for n in line.split() if n.strip()])

    return boards


def get_test_data() -> tuple[BoardGroup, list[int]]:
    numbers = [
        7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1  # fmt: skip
    ]
    boards = parse_boards(
        StringIO(
            "22 13 17 11  0\n"
            " 8  2 23  4 24\n"
            "21  9 14 16  7\n"
            " 6 10  3 18  5\n"
            " 1 12 20 15 19\n"
            "\n"
            " 3 15  0  2 22\n"
            " 9 18 13 17  5\n"
            "19  8  7 25 23\n"
            "20 11 10 24  4\n"
            "14 21 16 12  6\n"
            "\n"
            "14 21 17 24  4\n"
            "10 16 15  9 19\n"
            "18  8 23 26 20\n"
            "22 11 13  6  5\n"
            " 2  0 12  3  7\n"
        )
    )
    board_group = BoardGroup.build(boards)
    return board_group, numbers


def test_1():
    board_group, numbers = get_test_data()
    winning_score = board_group.play(numbers)
    assert winning_score == 4512


def test_2():
    board_group, numbers = get_test_data()
    winning_score = board_group.play_for_last_place(numbers)
    assert winning_score == 1924


def solution_1():
    board_group, numbers = get_input_data()
    winning_score = board_group.play(numbers)
    print(f"Solution 1 is {winning_score}")


def solution_2():
    board_group, numbers = get_input_data()
    winning_score = board_group.play_for_last_place(numbers)
    print(f"Solution 2 is {winning_score}")


if __name__ == "__main__":
    test_1()
    solution_1()
    test_2()
    solution_2()
