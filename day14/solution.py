from typing import Optional, Sequence
import io
import itertools
import pathlib
import re


def process_input(input_file: io.TextIOWrapper) -> list[Sequence[str]]:
    return [
        re.search(r"(mask|mem)\s*(?:\[(\d+)])?\s+=\s+([0-9X]+)", line).groups()
        for line in input_file
    ]


class BitMaskedMemory:
    def __init__(self):
        self.mask = "X" * 36
        self.memory = {}

    def __getitem__(self, item):
        return self.memory[item]

    def __setitem__(self, key, value):
        self.memory[key] = self.mask_value(value)

    def __iter__(self):
        return iter(self.memory.items())

    def mask_value(self, value: str) -> str:
        binary_value = bin(int(value))[2:]
        masked = "".join(
            v1 if v2 == "X" else v2
            for v1, v2 in zip(binary_value.zfill(36), self.mask)
        )
        return masked


class BitMaskedMemoryAddresses(BitMaskedMemory):
    def __setitem__(self, key, value):
        masked_addresses = self.mask_address(key)
        for masked_address in masked_addresses:
            self.memory[masked_address] = value

    def mask_address(self, address: str) -> list[str]:
        binary_address = bin(int(address))[2:].zfill(36)
        floating_masked = []
        total_floating_bits = 0
        for bit, mask in zip(binary_address, self.mask):
            if mask == "0":
                floating_masked.append(bit)
            elif mask == "1":
                floating_masked.append(mask)
            elif mask == "X":
                total_floating_bits += 1
                floating_masked.append("{}")

        masked = "".join(floating_masked)
        permutations = [
            masked.format(*permutation)
            for permutation in itertools.product((0, 1), repeat=total_floating_bits)
        ]
        return permutations


def get_sum_of_masked_memory(instructions: list[Sequence[str]]) -> int:
    memory = BitMaskedMemory()
    for instruction, address, value in instructions:
        if instruction == "mask":
            memory.mask = value
        elif instruction == "mem":
            memory[address] = value

    return sum(int(value, 2) for address, value in memory)


def get_sum_of_masked_memory_addresses(instructions: list[Sequence[str]]) -> int:
    memory = BitMaskedMemoryAddresses()
    for instruction, address, value in instructions:
        if instruction == "mask":
            memory.mask = value
        elif instruction == "mem":
            memory[address] = value

    return sum(int(value) for address, value in memory)


if __name__ == "__main__":
    input_file_path = pathlib.Path(__file__).parent / "test_input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print("Test Returns")
    print("Sum:", get_sum_of_masked_memory(input_data), "==", 165)

    input_file_path = pathlib.Path(__file__).parent / "test_b.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print("Test B Returns")
    print("Sum:", get_sum_of_masked_memory_addresses(input_data), "==", 208)

    input_file_path = pathlib.Path(__file__).parent / "input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)
    print()
    print("Final Results")
    print("Sum:", get_sum_of_masked_memory(input_data))
    print("Sum:", get_sum_of_masked_memory_addresses(input_data))