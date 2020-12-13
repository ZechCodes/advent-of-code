import io
import math
import pathlib


def process_input(input_file: io.TextIOWrapper) -> tuple[int, dict[int, int]]:
    return (
        int(input_file.readline()),
        {
            index: int(bus_id)
            for index, bus_id in enumerate(input_file.readline().split(","))
            if bus_id != "x"
        }
    )


def get_next_departure(bus_id: int, desired_time: int) -> int:
    return math.ceil(desired_time / bus_id) * bus_id - desired_time


def find_earliest_departure(time: int, buses: list[int]) -> int:
    departure, bus_id = min(
        ((get_next_departure(bus_id, time), bus_id) for bus_id in buses.values()),
        key=lambda bus: bus[0]
    )
    return departure * bus_id


def find_time_of_most_departures(buses: dict[int, int]) -> int:
    indexes = [bus - index for index, bus in buses.items()]
    product = math.prod(buses.values())
    time = 0
    for index, interval in zip(indexes, buses.values()):
        partial_produdct = product // interval
        mod_inverse = get_mod_inverse(partial_produdct, interval)
        time += index * mod_inverse * partial_produdct

    return time % product


def get_mod_inverse(partial_product: int, interval: int) -> int:
    for i in range(interval):
        if partial_product * i % interval == 1:
            return i


if __name__ == "__main__":
    input_file_path = pathlib.Path(__file__).parent / "test_input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)


    print("Test A")
    print(find_earliest_departure(*input_data), 295)

    print(">>", find_time_of_most_departures(input_data[1]), 1_068_781)
    print("Test B")
    print(">>", find_time_of_most_departures({0: 17, 2: 13, 3: 19}), 3417)

    input_file_path = pathlib.Path(__file__).parent / "input.txt"
    with input_file_path.open() as input_file:
        input_data = process_input(input_file)

    print("\nFinal")
    print(find_earliest_departure(*input_data))
    print(f">> {find_time_of_most_departures(input_data[1]):,}")
