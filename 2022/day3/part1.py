from input_parser import parse_by_compartment


def get_priority(item: str):
    if item.isupper():
        return ord(item) - 38

    return ord(item) - 96


def get_total_priority_of_all_duplicate_items() -> int:
    rucksacks = parse_by_compartment()
    totals = []
    for compartment_a, compartment_b in rucksacks:
        totals.extend(map(get_priority, compartment_a & compartment_b))

    return sum(totals)


if __name__ == "__main__":
    print(f"The total priority of all duplicate items is  {get_total_priority_of_all_duplicate_items():,}.")
