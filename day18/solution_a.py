from __future__ import annotations
from typing import TextIO, Union
import abc
import pathlib
import re


def process_input(file: TextIO) -> list[Parser]:
    return [
        Parser(line).parse()
        for line in file
        if not line.isspace()
    ]


class Parser:
    token_pattern = re.compile(r"\d+|[()+*]")

    def __init__(self, line: str):
        self.tokens = self.tokenize(line)
        self.root = Parenthetical()

    def evaluate(self) -> int:
        return self.root.value

    def parse(self) -> Parser:
        parentheticals = [self.root]
        for token in self.tokens:
            if token == "(":
                parenthetical = Parenthetical()
                parentheticals[-1].push(parenthetical)
                parentheticals.append(parenthetical)
            elif token == ")":
                parentheticals.pop()
            elif token.isdigit():
                parentheticals[-1].push(Number(token))
            else:
                parentheticals[-1].push(Operator.create(token))

        return self

    def tokenize(self, line: str) -> list[str]:
        return self.token_pattern.findall(line)


class Value(abc.ABC):
    @property
    @abc.abstractmethod
    def value(self) -> int:
        ...


class Number(Value):
    def __init__(self, token: str):
        self._value = int(token)

    @property
    def value(self) -> int:
        return self._value

    def __repr__(self):
        return f"<{type(self).__name__}: {self.value}>"


class Parenthetical(Value):
    def __init__(self):
        self.tokens = []

    @property
    def value(self) -> int:
        if not self.tokens:
            return 0

        tokens = self.tokens[::-1]  # Reverse it so that we don't need to do pop(0)
        value = tokens.pop().value
        while tokens:
            operator = tokens.pop()
            next_value = tokens.pop().value
            value = operator.evaluate(value, next_value)

        return value

    def push(self, token: Union[Value, Operator]):
        self.tokens.append(token)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.tokens}>"


class Operator(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, left: int, right: int) -> int:
        ...

    @classmethod
    def create(cls, token: str) -> Operator:
        if token == "+":
            return AdditionOperator()
        elif token == "*":
            return MultiplicationOperator()

    def __repr__(self):
        return f"<{type(self).__name__}>"


class AdditionOperator(Operator):
    def evaluate(self, augend: int, addend: int) -> int:
        return augend + addend


class MultiplicationOperator(Operator):
    def evaluate(self, multiplicand: int, multiplier: int) -> int:
        return multiplicand * multiplier


if __name__ == "__main__":
    input_file_path = pathlib.Path(__file__).parent / "test_input_a.txt"
    with input_file_path.open() as input_file:
        parsers = process_input(input_file)

    print("Test Data")
    print(
        "\n".join(
            f"{parser.evaluate()} should be {value}"
            for parser, value in zip(parsers, (26, 437, 12240, 13632))
        )
    )

    print("Final")
    input_file_path = pathlib.Path(__file__).parent / "input.txt"
    with input_file_path.open() as input_file:
        parsers = process_input(input_file)

    print(sum(parser.evaluate() for parser in parsers))
