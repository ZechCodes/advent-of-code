from pathlib import Path
from typing import TypeAlias


Compartment: TypeAlias = set[str]
Rucksack: TypeAlias = tuple[Compartment, Compartment]


def parse() -> list[str]:
    with Path("rucksacks-data.txt").open("r") as data_file:
        return [*map(str.strip, data_file)]


def parse_by_compartment() -> list[Rucksack]:
    return [
        (
            set(rucksack[:(l := len(rucksack) // 2)]),
            set(rucksack[l:])
        )
        for rucksack in parse()
    ]
