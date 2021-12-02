from itertools import combinations
from typing import Sequence
import io
import pathlib


def process_input(input_file: io.TextIOWrapper):
    return [int(line.strip()) for line in input_file if line.strip()]


def find_invalid_value(xmas_input: Sequence[int], scan_size: int) -> int:
    for index, number in enumerate(xmas_input[scan_size:], start=scan_size):
        valid_values = (sum(combination) for combination in combinations(xmas_input[index - scan_size:index], 2))
        if number not in valid_values:
            return number

    return -1


def find_encryption_weakness(xmas_input: Sequence[int], target: int) -> int:
    for start, number in enumerate(xmas_input):
        values = [number, xmas_input[start + 1]]
        next_value = start + 2
        while sum(values) < target and next_value < len(xmas_input):
            values.append(xmas_input[next_value])
            next_value += 1

        if sum(values) == target:
            return max(values) + min(values)

    return -1


if __name__ == "__main__":
    input_file_path = pathlib.Path(__file__).parent / "test_input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    invalid_value = find_invalid_value(input_data, 5)
    print(invalid_value, 127)
    print(find_encryption_weakness(input_data, invalid_value), 62)

    # ---------- #
    input_file_path = pathlib.Path(__file__).parent / "input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    invalid_value = find_invalid_value(input_data, 25)
    print(invalid_value)
    print(find_encryption_weakness(input_data, invalid_value))

