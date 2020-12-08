import functools
import io
import pathlib
import re


Graph = dict[str, dict[str, int]]


def process_input(input_file: io.TextIOWrapper) -> dict[str, dict[str, int]]:
    data: dict[str, dict[str, int]] = {}
    for line in input_file:
        tokens = re.findall(r"(\d*\s?[\w\s]+?(?=\sbag))", line)
        bag_type = tokens[0]
        data[bag_type] = {}

        if "contain no other" in line:
            continue

        for token in tokens[1:]:
            quantity, sub_bag_type = re.match(r".+?(\d+).+?([\w\s]+)", token).groups()
            data[bag_type][sub_bag_type] = int(quantity)

    return data


def check_if_contains(search_for: str, parent: str, bag_graph: Graph) -> bool:
    if search_for in bag_graph[parent]:
        return True

    for child in bag_graph[parent]:
        if check_if_contains(search_for, child, bag_graph):
            return True

    return False


def count_bags_that_can_contain(search_for: str, bag_graph: Graph) -> int:
    total = 0
    for bag in bag_graph:
        total += check_if_contains(search_for, bag, bag_graph)

    return total


def get_total_bags_contained(parent: str, bag_graph: Graph) -> int:
    total = 0
    for bag, count in bag_graph[parent].items():
        total += count * (get_total_bags_contained(bag, bag_graph) + 1)

    return total


if __name__ == "__main__":
    input_file_path = pathlib.Path(__file__).parent / "input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print(count_bags_that_can_contain("shiny gold", input_data))
    print(get_total_bags_contained("shiny gold", input_data))

