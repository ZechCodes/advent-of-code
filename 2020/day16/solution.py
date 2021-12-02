from typing import Union
import collections
import io
import math
import pathlib


Ticket = list[int]
Rule = tuple[str, range, range]
Sections = dict[str, Union[list[Ticket], list[Rule], Ticket]]


def process_input(input_file: io.TextIOWrapper) -> Sections:
    section = "rules"
    sections: Sections = {
        "rules": [],
        "your ticket": None,
        "nearby tickets": [],
    }
    for line in (l.strip() for l in input_file if l.strip()):
        if line.endswith(":"):
            section = line[:-1]
        elif ":" in line:
            name = line[:line.find(":")]
            start_a = int(line[line.find(":") + 2:line.find("-")])
            end_a = int(line[line.find("-") + 1:line.find(" or")])
            end_b = int(line[line.rfind("-") + 1:])
            start_b = int(line[line.rfind(" ") + 1:line.rfind("-")])
            sections[section].append(
                (
                    name,
                    range(start_a, end_a + 1),
                    range(start_b, end_b + 1),
                )
            )
        elif section == "your ticket":
            sections[section] = [int(num) for num in line.split(",")]
        else:
            sections[section].append(
                [int(num) for num in line.split(",")]
            )

    return sections


def get_invalid_ticket_fields(rules: list[Rule], tickets: list[Ticket]) -> list[int]:
    return [
        field
        for ticket in tickets
        for field in ticket
        if not is_valid_field(rules, field)
    ]


def get_valid_tickets(rules: list[Rule], tickets: list[Ticket]) -> list[Ticket]:
    valid_tickets = []
    for ticket in tickets:
        for field in ticket:
            if not is_valid_field(rules, field):
                break
        else:
            valid_tickets.append(ticket)

    return valid_tickets


def is_valid_field(rules: list[Rule], field: int) -> bool:
    return any(
        field_matches(lower, upper, field)
        for _, lower, upper in rules
    )


def field_matches(lower: range, upper: range, field: int) -> bool:
    return field in lower or field in upper


def determine_ticket_fields(rules: list[Rule], tickets: list[Ticket], your_ticket: Ticket) -> dict[str, int]:
    valid_tickets = get_valid_tickets(rules, tickets)

    possible_fields = collections.defaultdict(lambda: set(range(len(rules))))

    for ticket in valid_tickets:
        field_rules = collections.defaultdict(set)
        for name, upper, lower in rules:
            for field, value in enumerate(ticket):
                if field_matches(lower, upper, value):
                    field_rules[name].add(field)

        for rule_name, fields_matched in field_rules.items():
            possible_fields[rule_name] = possible_fields[rule_name].intersection(fields_matched)

    ticket_fields = {}
    for field_name, fields in sorted(possible_fields.items(), key=lambda items: len(items[1])):
        for field in fields:
            if field not in ticket_fields.values():
                ticket_fields[field_name] = field
                break

    return {
        field_name: your_ticket[field]
        for field_name, field in ticket_fields.items()
    }


if __name__ == "__main__":
    input_file_path = pathlib.Path(__file__).parent / "test_input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print("Test")
    print("Sum:", sum(get_invalid_ticket_fields(input_data["rules"], input_data["nearby tickets"])), 71)

    print()
    input_file_path = pathlib.Path(__file__).parent / "test_input_b.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print(determine_ticket_fields(input_data["rules"], input_data["nearby tickets"], input_data["your ticket"]))

    print()
    input_file_path = pathlib.Path(__file__).parent / "input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print("Final")
    print("Sum:", sum(get_invalid_ticket_fields(input_data["rules"], input_data["nearby tickets"])))
    ticket = determine_ticket_fields(input_data["rules"], input_data["nearby tickets"], input_data["your ticket"])
    departures = [
        value
        for name, value in ticket.items()
        if name.startswith("departure")
    ]
    print(ticket)
    print(departures, len(departures))
    assert len(departures) == 6
    print(math.prod(departures))
