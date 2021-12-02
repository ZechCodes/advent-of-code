from operator import mul


def get_commands() -> list[(str, int)]:
    with open(f"input.txt", "r") as data_file:
        return [((l := line.split())[0], int(l[1])) for line in data_file]


def get_position(commands: list[(str, int)]) -> (int, int):
    depth = horizontal = 0
    for command, amount in commands:
        match command:
            case "forward":
                horizontal += amount
            case "down":
                depth += amount
            case "up":
                depth -= amount
            
    return depth, horizontal


def get_position_using_aim(commands: list[(str, int)]) -> (int, int):
    aim = depth = horizontal = 0
    for command, amount in commands:
        match command:
            case "forward":
                horizontal += amount
                depth += aim * amount
            case "down":
                aim += amount
            case "up":
                aim -= amount

    return depth, horizontal


def get_part_1_solution() -> int:
    commands = get_commands()
    return mul(*get_position(commands))


def get_part_2_solution():
    commands = get_commands()
    return mul(*get_position_using_aim(commands))


def test_1():
    commands = [("forward", 5),
                ("down", 5),
                ("forward", 8),
                ("up", 3),
                ("down", 8),
                ("forward", 2)]
    assert mul(*get_position(commands)) == 150


def test_2():
    commands = [("forward", 5),
                ("down", 5),
                ("forward", 8),
                ("up", 3),
                ("down", 8),
                ("forward", 2)]
    assert mul(*get_position_using_aim(commands)) == 900


if __name__ == "__main__":
    test_1()
    print(f"Part 1 solution is {get_part_1_solution()}")

    test_2()
    print(f"Part 2 solution is {get_part_2_solution()}")
