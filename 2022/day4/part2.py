from input_parser import parse


def get_number_of_overlapping_assignments() -> int:
    return sum(
        bool(assignment_a & assignment_b) for assignment_a, assignment_b in parse()
    )


if __name__ == "__main__":
    print(
        f"There are {get_number_of_overlapping_assignments():,} assignments that are overlapping."
    )
