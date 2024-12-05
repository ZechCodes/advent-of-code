from collections import defaultdict
from functools import partial
from itertools import takewhile
from pathlib import Path
from typing import Iterator, Generator

type Page = int
type Update = list[Page]
type Updates = list[Update]
type PriorPages = list[Page]
type Orderings = dict[Page, PriorPages]


def solve_part_1(updates: Updates, orderings: Orderings) -> int:
    valid_updates = find_valid_updates(updates, orderings)
    return sum(find_middle_pages(valid_updates))


def solve_part_2(updates: Updates, orderings: Orderings) -> int:
    invalid_updates = find_invalid_updates(updates, orderings)
    corrected_updates = correct_ordering_of_updates(invalid_updates, orderings)
    return sum(find_middle_pages(corrected_updates))


def find_valid_updates(updates: Updates, orderings: Orderings) -> Generator[Update, None, None]:
    for update in updates:
        if is_update_valid(update, orderings):
            yield update


def find_invalid_updates(updates: Updates, orderings: Orderings) -> Generator[Update, None, None]:
    for update in updates:
        if not is_update_valid(update, orderings):
            yield update


def is_update_valid(update: Update, orderings: Orderings) -> bool:
    for i, page in enumerate(update):
        if any(before in update[i+1:] for before in orderings.get(page, [])):
            return False

    return True


def find_middle_pages(updates: Iterator[Update]) -> Generator[Page, None, None]:
    for update in updates:
        yield update[len(update) // 2]


def correct_ordering_of_updates(updates: Iterator[Update], orderings: Orderings) -> Generator[Update, None, None]:
    for update in updates:
        yield correct_update_ordering(update, orderings)


def correct_update_ordering(update: Update, orderings: Orderings) -> Update:
    def order(a, b) -> int:
        if a == b:
            return 0

        if b in orderings.get(a, []):
            return -1

        return 1

    corrected = list(update)
    page_stack = iter(update)
    while not is_update_valid(corrected, orderings):
        page = next(page_stack)
        corrected = sorted(corrected, key=partial(order, page))

    return corrected


def parse_input(file_name: str) -> tuple[Updates, Orderings]:
    with (Path(__file__).parent / file_name).open() as file:
        lines = map(str.strip, file)
        orderings = parse_orderings(lines)
        updates = parse_updates(lines)
        return updates, orderings


def parse_orderings(lines: Iterator[str]) -> Orderings:
    orderings = defaultdict(list)
    for line in takewhile(bool, lines):
        before, after = map(int, line.strip().split("|"))
        orderings[after].append(before)

    return orderings


def parse_updates(lines: Iterator[str]) -> Updates:
    return [
        [int(page) for page in line.split(",")]
        for line in lines
    ]


assert solve_part_1(*parse_input("example_input.txt")) == 143
print(solve_part_1(*parse_input("puzzle_input.txt")))

assert solve_part_2(*parse_input("example_input.txt")) == 123
print(solve_part_2(*parse_input("puzzle_input.txt")))
