from typing import Any
import io
import pathlib
import re


def count_valid_passports(passports: list[dict[str, Any]]) -> int:
    required_keys = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    return len([passport for passport in passports if required_keys.issubset(passport)])


def count_validated_passports(passports: list[dict[str, Any]]) -> int:
    return len([passport for passport in passports if fields_are_valid(passport)])


def fields_are_valid(passport: dict[str, Any]) -> bool:
    predicates = {
        "byr": lambda value: value.isdigit() and 1920 <= int(value) <= 2002,
        "iyr": lambda value: value.isdigit() and 2010 <= int(value) <= 2020,
        "eyr": lambda value: value.isdigit() and 2020 <= int(value) <= 2030,
        "hgt": lambda value: (
            value[:-2].isdigit() and (
                (value[-2:] == "in" and 59 <= int(value[:-2]) <= 76) or
                (value[-2:] == "cm" and 150 <= int(value[:-2]) <= 193)
            )
        ),
        "hcl": lambda value: re.match(r"#[0-9abcdef]{6}", value),
        "ecl": lambda value: value in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
        "pid": lambda value: len(value) == 9 and value.isdigit(),
    }
    for key, predicate in predicates.items():
        if key not in passport:
            return False

        if not predicate(passport[key]):
            return False

    return True


def process_passport_file(passport_file: io.TextIOWrapper) -> list[dict[str, Any]]:
    passports = []
    current = {}
    for line in (l.strip() for l in passport_file):
        if line:
            current.update(process_passport_line(line))

        else:
            passports.append(current)
            current = {}

    passports.append(current)
    return passports


def process_passport_line(line: str) -> dict[str, Any]:
    data = {}
    for token in line.split():
        key, value = token.split(":")
        data[key] = value

    return data


if __name__ == "__main__":
    passport_file_path = pathlib.Path(__file__).parent / "passports.txt"
    with passport_file_path.open() as passports_file:
        passports = process_passport_file(passports_file)

    print(count_valid_passports(passports))
    print(count_validated_passports(passports))
