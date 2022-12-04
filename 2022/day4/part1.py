from input_parser import parse


def get_number_of_fully_contained_assignments() -> int:
    return sum(
        assignment_b.issubset(assignment_a) or assignment_a.issubset(assignment_b)
        for assignment_a, assignment_b in parse()
    )


if __name__ == "__main__":
    print(
        f"There are {get_number_of_fully_contained_assignments():,} assignments that are fully contained within the "
        f"other assignment."
    )
