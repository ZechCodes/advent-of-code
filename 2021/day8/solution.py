from __future__ import annotations
from itertools import chain
from typing import Iterator
import re


Digits = list[list[str]]


def find_mapping(digits: list[str]) -> dict[str, int]:
    possibilities = get_possible_digits(digits)
    return create_mapping(possibilities)


def get_possible_digits(digits: list[str]) -> list[set[str]]:
    lengths = {6: (0, 6, 9), 2: (1,), 5: (2, 3, 5), 4: (4,), 3: (7,), 7: (8,)}
    possibilities = [set() for _ in range(10)]
    for digit in set(digits):
        for number in lengths[len(digit)]:
            possibilities[number].add(digit)

    return possibilities


def create_mapping(possibilities: list[set[str]]) -> dict[str, int]:
    mapping = {n: possibilities[n].pop() for n in {1, 4, 7, 8}}

    mapping[6] = doesnt_match(possibilities[6], mapping[7])
    possibilities[0].remove(mapping[6])
    possibilities[9].remove(mapping[6])

    mapping[9] = get_nearest_match(possibilities[9], mapping[4])
    possibilities[0].remove(mapping[9])

    mapping[0] = possibilities[0].pop()

    mapping[2] = get_furthest_match(possibilities[2], mapping[9])
    possibilities[3].remove(mapping[2])
    possibilities[5].remove(mapping[2])

    mapping[3] = get_nearest_match(possibilities[3], mapping[7])
    possibilities[5].remove(mapping[3])

    mapping[5] = possibilities[5].pop()

    return dict(zip(mapping.values(), mapping))


def decode_display(digits: list[str], mapping: dict[str, int]) -> int:
    number = 0
    for digit in digits:
        number = number * 10 + mapping[digit]

    return number


def get_decoded_outputs(inputs: Digits, outputs: Digits) -> list[int]:
    return [decode_display(o, find_mapping(i)) for i, o in zip(inputs, outputs)]


def get_nearest_match(possibilities: set[str], search: str) -> str:
    sorted_by_num_differences = sorted(
        possibilities, key=lambda x: len(set(search) - set(x))
    )
    return sorted_by_num_differences[0]


def get_furthest_match(possibilities: set[str], search: str) -> str:
    sorted_by_num_differences = sorted(
        possibilities, key=lambda x: len(set(search) - set(x))
    )
    return sorted_by_num_differences[-1]


def doesnt_match(possibilities: set[str], search: str) -> str:
    for possible_match in possibilities:
        if not set(search).issubset(possible_match):
            return possible_match


def get_unique_digits(outputs: Digits) -> list[str]:
    return [digit for digit in chain(*outputs) if len(digit) in {2, 3, 4, 7}]


def parse_line(line: str) -> list[str]:
    return ["".join(sorted(section)) for section in re.findall(r"[^\s]+", line)]


def get_test_data() -> tuple[Digits, Digits]:
    data = map(
        parse_line,
        [
            "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
            "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
            "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
            "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
            "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
            "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
            "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
            "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
            "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
            "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce",
        ],
    )

    return separate_inputs_and_outputs(data)


def separate_inputs_and_outputs(data: Iterator[list[str]]) -> tuple[Digits, Digits]:
    inputs: list[list[str]] = []
    outputs: list[list[str]] = []

    for line in data:
        inputs.append(current := [])

        for digit in line:
            if digit == "|":
                outputs.append((current := []))

            else:
                current.append(digit)

    return inputs, outputs


def get_input_data() -> tuple[Digits, Digits]:
    with open("input.txt", "r") as input_file:
        data = map(parse_line, (line.strip() for line in input_file))
        return separate_inputs_and_outputs(data)


def test_1():
    inputs, outputs = get_test_data()
    unique = get_unique_digits(outputs)
    assert len(unique) == 26


def test_2():
    inputs, outputs = get_test_data()
    decoded_outputs = get_decoded_outputs(inputs, outputs)
    print(sum(decoded_outputs))
    assert sum(decoded_outputs) == 61229


def solution_1():
    inputs, outputs = get_input_data()
    unique = len(get_unique_digits(outputs))
    print(f"Solution 1 is {unique}")


def solution_2():
    inputs, outputs = get_input_data()
    decoded_outputs = get_decoded_outputs(inputs, outputs)
    print(f"Solution 2 is {sum(decoded_outputs)}")


if __name__ == "__main__":
    test_1()
    solution_1()
    test_2()
    solution_2()
