from typing import Generator, Iterator


def parse(data: Iterator[str]) -> Generator[list[int], None, None]:
    for line in data:
        yield [int(c) for c in line if c.isdigit()]


def parse_with_spelled_out(data: Iterator[str]) -> Generator[list[int], None, None]:
    for line in data:
        yield list(parse_line_with_spelled_out(line))


def parse_line_with_spelled_out(line: str) -> Generator[int, None, None]:
    numbers = dict(
        zip(
            ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"],
            range(1, 10),
        )
    )

    for i, c in enumerate(line):
        if c.isdigit():
            yield int(c)

        for number, value in numbers.items():
            if line[i:].startswith(number):
                yield value
                break
