from __future__ import annotations
from typing import Generator, TextIO
import abc
import pathlib
import re


class Rule(abc.ABC):
    rule_table: dict[int, Rule] = {}

    @abc.abstractmethod
    def matches(self, string: str) -> bool:
        ...

    @abc.abstractmethod
    def get_match(self, string: str) -> str:
        ...

    @classmethod
    def create(cls, index: int, tokens: tuple[str]) -> Rule:
        if "\"" in tokens[0]:
            rule = RuleString(index, tokens[0][1:-1])
        else:
            rule = RuleGroup(index)
            group = []
            for token in tokens:
                if token == "|":
                    rule.add_rule(group)
                    group = []
                    continue

                group.append(int(token))
            else:
                rule.add_rule(group)

        cls.rule_table[index] = rule
        return rule


class RuleGroup(Rule):
    def __init__(self, index: int):
        self.index = index
        self._rules = []

    @property
    def rules(self) -> list[list[Rule]]:
        return [
            [
                self.rule_table[rule_index]
                for rule_index in rules
            ] for rules in self._rules
        ]

    def add_rule(self, rule: list[int]):
        self._rules.append(rule)

    def matches(self, string: str, custom_rules: bool = False) -> bool:
        return self.get_match(string, custom_rules) == string

    def get_match(self, string: str, custom_rules: bool = False) -> str:
        # print(f"{self.index:<6}  {self!s:12}  {string}")
        if self.index == 0 and custom_rules:
            r = self.do_rule_0(string)
            # print(string == r)
            return r

        for group in self.rules:
            index = 0
            for rule in group:
                match = rule.get_match(string[index:])
                if not match:
                    break

                index += len(match)
            else:
                return string[:index]

        return ""

    def do_rule_0(self, string: str) -> str:
        rule_42 = 0
        index = 0
        match = None
        while match != "":
            rule_31 = 0
            match2 = None
            index2 = index
            while match2 != "" and rule_42 - rule_31 >= 2:
                match2 = self.rule_table[31].get_match(string[index2:])
                index2 += len(match2)
                if match2:
                    rule_31 += 1

                if index2 == len(string) and rule_42 - rule_31 >= 2:
                    return string

            match = self.rule_table[42].get_match(string[index:])
            index += len(match)
            rule_42 += 1

        return ""

    def __repr__(self):
        return f"<{type(self).__name__} {self.index}: {self.rules!r}>"

    def __str__(self):
        return " | ".join(
            " ".join(
                str(rule.index)
                for rule in group
            ) for group in self.rules
        )


class RuleString(Rule):
    def __init__(self, index: int, string: str):
        self.index = index
        self.string = string

    def matches(self, string: str) -> bool:
        return self.string == string

    def get_match(self, string: str) -> str:
        # print(f"{self.index:<6}  {self.string!r:12}  {string}")
        return self.string if string.startswith(self.string) else ""

    def __repr__(self):
        return f"<{type(self).__name__} {self.index}: {self.string!r}>"

    def __str__(self):
        return self.string


def process_input(input_file: TextIO) -> tuple[dict[int, Rule], list[str]]:
    input_data = (line.strip() for line in input_file)
    rules = process_rules(input_data)
    data = process_data(input_data)
    return rules, data


def process_rules(input_data: Generator[str]) -> dict[int, Rule]:
    for line in input_data:
        if not line:
            break

        index, *tokens = re.findall(r"(\".+?\"|\d+|\|)", line)
        Rule.create(int(index), tokens)

    return Rule.rule_table


def process_data(input_data: Generator[str]) -> list[str]:
    return list(input_data)


if __name__ == "__main__":
    def main():
        input_file_path = pathlib.Path(__file__).parent / "test_input.txt"
        with input_file_path.open() as input_file:
            rules, data = process_input(input_file)

        print(
            "\n".join(
                f"{d!r} correct {rules[0].matches(d) == solution}"
                for d, solution in zip(data, (True, False, True, False, False, False))
            )
        )

        input_file_path = pathlib.Path(__file__).parent / "test_input_b.txt"
        with input_file_path.open() as input_file:
            rules, data = process_input(input_file)

        Rule.create(8, "42 | 42 8".split())
        Rule.create(11, "42 31 | 42 11 31".split())

        print(
            "\n".join(
                f"{d!r:50} {rules[0].matches(d, custom_rules=True) == solution!s:5} {solution}"
                for d, solution in zip(
                    data,
                    (False, True, True, True, True, True, True, True, True, True, True, False, True, False, True)
                )
            )
        )

        print()
        print("---- Final")

        input_file_path = pathlib.Path(__file__).parent / "input.txt"
        with input_file_path.open() as input_file:
            rules, data = process_input(input_file)

        print(
            sum(
                rules[0].matches(string)
                for string in data
            )
        )

        Rule.create(8, "42 | 42 8".split())
        Rule.create(11, "42 31 | 42 11 31".split())

        print(
            sum(
                rules[0].matches(string, custom_rules=True)
                for string in data
            )
        )

    main()
