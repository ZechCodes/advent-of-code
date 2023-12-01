from parser import parse
from pathlib import Path


def solution(data):
    return sum(10 * l[0] + l[~0] for l in data)


if __name__ == "__main__":
    with (Path(__file__).parent / "input1.txt").open() as f:
        data = parse(f)
        print(f"The solution for day 1 part 2 is {solution(data)}")
