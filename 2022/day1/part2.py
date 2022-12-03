from input_parser import parse


def get_calories_carried_by_top_3_elves() -> int:
    elves = parse()
    return sum(sorted(sum(elf) for elf in elves)[-3:])


if __name__ == "__main__":
    print(f"The 3 elves carrying the most calories are carrying a total of {get_calories_carried_by_top_3_elves():,} calories.")
