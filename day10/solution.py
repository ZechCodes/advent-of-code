import io
import pathlib
import time


def process_input(input_file: io.TextIOWrapper):
    adapters = sorted(int(line.strip()) for line in input_file if line.strip())
    return [0] + adapters + [max(adapters) + 3]


def get_jolt_differences(adapters: list[int]) -> int:
    differences = [higher - lower for higher, lower in zip(adapters[1:], adapters)]
    num_3s = sum(1 for difference in differences if difference == 3)
    num_1s = sum(1 for difference in differences if difference == 1)
    return num_1s * num_3s


def count_combinations(adapters: list[int]) -> int:
    paths = [1] * (len(adapters))

    for index in range(1, len(adapters)):
        paths[index] = sum(paths[previous] for previous in get_previous_adapter_indexes(index, adapters))

    return max(paths)


def get_previous_adapter_indexes(adapter_index: int, adapters: list[int]) -> list[int]:
    indexes = []
    adapter = adapters[adapter_index]
    for index, current in enumerate(adapters[:adapter_index]):
        if adapter - 3 <= current < adapter:
            indexes.append(index)

    return indexes


if __name__ == "__main__":
    input_file_path = pathlib.Path(__file__).parent / "test_input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print("Test A")
    print(get_jolt_differences(input_data), 35)
    print(count_combinations(input_data), 8)

    # ---------- #
    input_file_path = pathlib.Path(__file__).parent / "test_input_b.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print("\nTest B")
    print(get_jolt_differences(input_data), 220)
    print(count_combinations(input_data), 19208)

    # ---------- #
    input_file_path = pathlib.Path(__file__).parent / "input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print("\nFinal")
    start = time.time()
    print("Start", start)
    print(get_jolt_differences(input_data))
    print(count_combinations(input_data), "\nEnd", (end := time.time()))
    print(1 / (end - start), "seconds")
