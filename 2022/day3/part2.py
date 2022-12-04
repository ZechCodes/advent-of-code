from input_parser import parse


def get_priority(item: str):
    if item.isupper():
        return ord(item) - 38

    return ord(item) - 96


def get_total_priority_of_all_badges() -> int:
    rucksacks = list(map(set, parse()))
    badge_priorities = 0
    for elf_a, elf_b, elf_c in zip(rucksacks[::3], rucksacks[1::3], rucksacks[2::3]):
        badge_priorities += sum(map(get_priority, elf_a & elf_b & elf_c))

    return badge_priorities


if __name__ == "__main__":
    print(f"The total priority of all badges is  {get_total_priority_of_all_badges():,}.")
