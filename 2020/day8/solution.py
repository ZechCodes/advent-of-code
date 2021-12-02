import io
import pathlib
import parse


Instructions = list[tuple[str, int]]


def process_input(input_file: io.TextIOWrapper) -> Instructions:
    pattern = parse.compile("{} {:d}")
    return [pattern.parse(line).fixed for line in input_file if line.strip()]


def find_last_value_before_reloop(instructions: Instructions) -> int:
    accumulator = 0
    next_instruction = 0
    already_run = set()

    while next_instruction not in already_run:
        current_instruction, next_instruction = next_instruction, next_instruction + 1
        operation, argument = instructions[current_instruction]

        if operation == "acc":
            accumulator += argument

        elif operation == "jmp":
            next_instruction = argument + current_instruction

        already_run.add(current_instruction)

    return accumulator


def find_last_value_after_correction(instructions: Instructions) -> int:
    accumulator = 0
    next_instruction = 0
    already_run = set()

    while next_instruction < len(instructions):
        current_instruction, next_instruction = next_instruction, next_instruction + 1
        operation, argument = instructions[current_instruction]

        if operation == "acc":
            accumulator += argument

        elif operation == "jmp":
            if (
                not is_infinite(current_instruction, instructions) or
                is_infinite(current_instruction + 1, instructions)
            ):
                next_instruction = current_instruction + argument

        elif operation == "nop":
            if (
                is_infinite(current_instruction, instructions) and
                not is_infinite(current_instruction + argument, instructions)
            ):
                next_instruction = current_instruction + argument

        already_run.add(current_instruction)

    return accumulator


def is_infinite(start_at: int, instructions: Instructions) -> bool:
    next_instruction = start_at
    already_run = set()

    while next_instruction < len(instructions):
        already_run.add(next_instruction)
        operation, argument = instructions[next_instruction]

        if operation == "jmp":
            next_instruction += argument
        else:
            next_instruction += 1

        if next_instruction in already_run:
            return True

    return False


if __name__ == "__main__":
    input_file_path = pathlib.Path(__file__).parent / "input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print(find_last_value_before_reloop(input_data), 5)
    print(find_last_value_after_correction(input_data), 8)

