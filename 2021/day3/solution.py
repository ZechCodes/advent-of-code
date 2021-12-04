from operator import mul


def get_diagnostics() -> list[str]:
    with open(f"input.txt", "r") as data_file:
        return [line.strip() for line in data_file.readlines() if line.strip()]


def get_gamma_rate(diagnostics: list[str]) -> int:
    gamma_rate = 0
    for values in zip(*diagnostics):
        gamma_rate <<= 1
        gamma_rate |= values.count("1") >= len(values) // 2
    return gamma_rate


def get_epsilon_rate(gamma_rate: int, width: int) -> int:
    return int("1" * width, base=2) ^ gamma_rate


def get_oxygen_rating(diagnostics: list[str]) -> int:
    values = diagnostics
    for bit in range(len(diagnostics[0])):
        count = sum(v[bit] == "1" for v in values)
        keep = str(int(count >= len(values) / 2))
        values = [v for v in values if v[bit] == keep]
        if len(values) == 1:
            break

    return int(values[0], base=2)


def get_co2_rating(diagnostics: list[str]) -> int:
    values = diagnostics
    for bit in range(len(diagnostics[0])):
        count = sum(v[bit] == "1" for v in values)
        keep = str(int(count < len(values) / 2))
        values = [v for v in values if v[bit] == keep]
        if len(values) == 1:
            break

    return int(values[0], base=2)


def get_part_1_solution() -> int:
    diagnostics = get_diagnostics()
    gamma_rate = get_gamma_rate(diagnostics)
    epsilon_rate = get_epsilon_rate(gamma_rate, len(diagnostics[0]))
    return gamma_rate * epsilon_rate


def get_part_2_solution():
    diagnostics = get_diagnostics()
    gamma_rate = get_gamma_rate(diagnostics)
    epsilon_rate = get_epsilon_rate(gamma_rate, len(diagnostics[0]))
    oxygen_rating = get_oxygen_rating(diagnostics)
    co2_rating = get_co2_rating(diagnostics)
    return oxygen_rating * co2_rating


def test_1():
    diagnostics = [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]
    gamma_rate = get_gamma_rate(diagnostics)
    epsilon_rate = get_epsilon_rate(gamma_rate, len(diagnostics[0]))
    assert gamma_rate * epsilon_rate == 198


def test_2():
    diagnostics = [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]
    oxygen_rating = get_oxygen_rating(diagnostics)
    co2_rating = get_co2_rating(diagnostics)
    assert oxygen_rating * co2_rating == 230


if __name__ == "__main__":
    test_1()
    print(f"Part 1 solution is {get_part_1_solution()}")

    test_2()
    print(f"Part 2 solution is {get_part_2_solution()}")
