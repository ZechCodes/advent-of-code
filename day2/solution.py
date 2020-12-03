from io import TextIOBase
import parse
import pathlib


RuleAndPassword = tuple[int, int, str, str]


def count_invalid_passwords(passwords: list[RuleAndPassword]) -> int:
    return sum(
        1
        for minimum, maximum, letter, password in passwords
        if minimum <= password.count(letter) <= maximum
    )


def count_invalid_passwords_update(passwords: list[RuleAndPassword]) -> int:
    valid_count = 0
    for first_position, second_position, letter, password in passwords:
        positions = {password[first_position - 1], password[second_position - 1]}
        if letter in positions and len(positions) > 1:
            valid_count += 1
    return valid_count


def process_passwords_file(password_file: TextIOBase) -> list[RuleAndPassword]:
    pattern = parse.compile("{:d}-{:d} {}: {}")
    return [
        pattern.parse(line.strip()).fixed
        for line in password_file
        if line.strip()
    ]


if __name__ == "__main__":
    with (pathlib.Path(__file__).parent / "passwords.txt").open() as password_file:
        passwords = process_passwords_file(password_file)
        print(count_invalid_passwords(passwords))
        print(count_invalid_passwords_update(passwords))
