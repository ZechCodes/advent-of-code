from pathlib import Path


def parse() -> list[tuple[str, str]]:
    with Path("plays-data.txt").open("r") as data_file:
        return [(opponent, me) for opponent, me in map(str.split, data_file)]

