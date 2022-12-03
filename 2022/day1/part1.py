from input_parser import parse


def get_most_calories_carried_by_elf() -> int:
    elves = parse()
    return max(sum(elf) for elf in elves)


if __name__ == "__main__":
    print(f"The elf carrying the most calories is carrying {get_most_calories_carried_by_elf():,} calories.")
