from itertools import pairwise


def get_data() -> list[int]:
    with open(f"input.txt", "r") as data_file:
        return [int(line) for line in data_file]


def get_number_increasing(data: list[int]) -> int:
    increasing = 0
    for a, b in pairwise(data):
        if a < b:
            increasing += 1
    return increasing


def denoise(data: list[int]) -> list[int]:
    return [sum(values) for values in zip(data, data[1:], data[2:])]


def get_part_1_solution():
    data = get_data()
    return get_number_increasing(data)


def get_part_2_solution():
    data = get_data()
    data = denoise(data)
    return get_number_increasing(data)


def test_1():
    data = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    assert get_number_increasing(data) == 7


def test_2():
    data = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    data = denoise(data)
    assert get_number_increasing(data) == 5


if __name__ == "__main__":
    test_1()
    print(f"Part 1 solution is {get_part_1_solution()}")

    test_2()
    print(f"Part 2 solution is {get_part_2_solution()}")
