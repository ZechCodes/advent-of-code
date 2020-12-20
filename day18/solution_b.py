from __future__ import annotations
from typing import TextIO, Union
import abc
import pathlib
import re


Stack = "list[Union[Value, Operator]]"


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
    def __init__(self, token: Union[str, int]):
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

        stack = self.do_addition(self.tokens[::-1])  # Reverse it so that we don't need to do pop(0)
        return self.do_multiplication(stack)

    def do_multiplication(self, stack: Stack) -> int:
        value = stack.pop().value
        while stack:
            operator = stack.pop()
            next_value = stack.pop().value
            value = operator.evaluate(value, next_value)

        return value

    def do_addition(self, stack: Stack) -> Stack:
        new_stack = [stack.pop()]
        while stack:
            operator = stack.pop()
            next_value = stack.pop()
            if isinstance(operator, AdditionOperator):
                value = new_stack.pop().value
                new_stack.append(
                    Number(operator.evaluate(value, next_value.value))
                )
            else:
                new_stack.append(operator)
                new_stack.append(next_value)

        return new_stack[::-1]

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
    input_file_path = pathlib.Path(__file__).parent / "test_input_b.txt"
    with input_file_path.open() as input_file:
        parsers = process_input(input_file)

    print("Test Data")
    print(
        "\n".join(
            f"{parser.evaluate()} should be {value}"
            for parser, value in zip(parsers, (51, 46, 1445, 669060, 23340))
        )
    )

    print("Final")
    input_file_path = pathlib.Path(__file__).parent / "input.txt"
    with input_file_path.open() as input_file:
        parsers = process_input(input_file)

    print(sum(parser.evaluate() for parser in parsers))
