from input_parser import parse


def get_number_of_overlapping_assignments() -> int:
    return sum(
        len(assignment_a & assignment_b) > 0 for assignment_a, assignment_b in parse()
    )


if __name__ == "__main__":
    print(
        f"There are {get_number_of_overlapping_assignments():,} assignments that are overlapping."
    )
