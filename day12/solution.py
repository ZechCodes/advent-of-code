from typing import Generator
import io
import itertools
import pathlib


def process_input(input_file: io.TextIOWrapper) -> list[tuple[str, int]]:
    return [
        (line[0], int(line.strip()[1:]))
        for line in input_file
        if line.strip()
    ]


def compute_manhattan_distance(instructions: list[tuple[str, int]]):
    position_ns = 0
    position_ew = 0

    waypoint_facing = 0
    waypoint_ns = 1
    waypoint_ew = 10

    for instruction, amount in instructions:
        if instruction == "N":
            waypoint_ns += amount
        elif instruction == "S":
            waypoint_ns -= amount
        elif instruction == "E":
            waypoint_ew += amount
        elif instruction == "W":
            waypoint_ew -= amount
        elif instruction == "L":
            if amount == 180:
                waypoint_ns *= -1
                waypoint_ew *= -1
            elif amount == 90:
                waypoint_ew, waypoint_ns = waypoint_ns * -1, waypoint_ew
            elif amount == 270:
                waypoint_ew, waypoint_ns = waypoint_ns, waypoint_ew * -1
        elif instruction == "R":
            if amount == 180:
                waypoint_ns *= -1
                waypoint_ew *= -1
            elif amount == 90:
                waypoint_ew, waypoint_ns = waypoint_ns, waypoint_ew * -1
            elif amount == 270:
                waypoint_ew, waypoint_ns = waypoint_ns * -1, waypoint_ew
        elif instruction == "F":
            position_ns += amount * waypoint_ns
            position_ew += amount * waypoint_ew

        # print(f"{instruction} {amount:2}: {position_ew:3}-{position_ns:3} : {waypoint_ew:2}-{waypoint_ns:2} {waypoint_facing}")

    return abs(position_ew) + abs(position_ns)


if __name__ == "__main__":
    input_file_path = pathlib.Path(__file__).parent / "test_input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print("Test A")
    print(compute_manhattan_distance(input_data), 286)

    input_file_path = pathlib.Path(__file__).parent / "input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print("\nFinal")
    print(compute_manhattan_distance(input_data))
