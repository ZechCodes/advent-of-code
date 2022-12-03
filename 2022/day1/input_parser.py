from pathlib import Path


def parse() -> list[list[int]]:
    elves = [[]]
    with Path("calories-data.txt").open("r") as data_file:
        for line in map(str.strip, data_file):
            if line:
                elves[-1].append(int(line))
            else:
                elves.append([])

    return elves
