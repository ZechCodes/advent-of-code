from __future__ import annotations
from collections import Counter, defaultdict
from itertools import pairwise
from typing import Iterator


Rules = dict[tuple[str, str], str]


def get_polymer_element_frequencies(
    polymer: str, rules: Rules, generations: int
) -> dict[tuple[str, str], int]:
    counts = Counter(pairwise(polymer))
    for _ in range(1, generations + 1):
        new_count = defaultdict(lambda: 0)
        for (a, b), count in counts.items():
            insert = rules[a, b]
            new_count[a, insert] += count
            new_count[insert, b] += count

        counts = new_count

    return counts


def get_element_counts(
    frequencies: dict[tuple[str, str], int], template: str
) -> dict[str, int]:
    counts = defaultdict(lambda: 0)
    for (_, element), count in frequencies.items():
        counts[element] += count

    counts[template[0]] += 1
    return counts


def get_test_data() -> tuple[str, Rules]:
    return process_input_data(
        [
            "NNCB",
            "",
            "CH -> B",
            "HH -> N",
            "CB -> H",
            "NH -> C",
            "HB -> C",
            "HC -> B",
            "HN -> C",
            "NN -> C",
            "BH -> H",
            "NC -> B",
            "NB -> B",
            "BN -> B",
            "BB -> N",
            "BC -> B",
            "CC -> N",
            "CN -> C",
        ]
    )


def get_input_data() -> tuple[str, Rules]:
    with open("input.txt", "r") as input_file:
        return process_input_data(line.strip() for line in input_file if line.strip())


def process_input_data(data: Iterator[str]) -> tuple[str, Rules]:
    rules: Rules = {}
    template = ""
    for line in data:
        if "-" in line:
            rules[(line[0], line[1])] = line[-1]
        elif line:
            template = line

    return template, rules


# ### Solution 1 ### #


def get_solution_1_result(template: str, rules: Rules) -> int:
    frequencies = get_polymer_element_frequencies(template, rules, 10)
    counts = get_element_counts(frequencies, template)
    return max(counts.values()) - min(counts.values())


def test_1():
    data = get_test_data()
    result = get_solution_1_result(*data)
    try:
        assert result == 1588
    except AssertionError as e:
        print("FAILED RESULT", result)
        raise


def solution_1():
    data = get_input_data()
    result = get_solution_1_result(*data)
    print(f"Solution 1 is {result}")


# ### Solution 2 ### #


def get_solution_2_result(template: str, rules: Rules) -> int:
    frequencies = get_polymer_element_frequencies(template, rules, 40)
    counts = get_element_counts(frequencies, template)
    return max(counts.values()) - min(counts.values())


def test_2():
    data = get_test_data()
    result = get_solution_2_result(*data)
    try:
        assert result == 2188189693529
    except AssertionError as e:
        print("FAILED RESULT", result, 2188189693529, 2188189693529 - result)
        raise


def solution_2():
    data = get_input_data()
    result = get_solution_2_result(*data)
    print(f"Solution 2 is {result}")


if __name__ == "__main__":
    test_1()
    solution_1()
    test_2()
    solution_2()
