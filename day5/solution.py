import io
import pathlib


def decode_number(encoded: str, mapping: tuple[str, str]) -> int:
    translation = encoded.translate(dict(zip(map(ord, mapping), ("0", "1"))))
    return int(translation, base=2)


def parse_boarding_pass(boarding_pass: str) -> int:
    row = decode_number(boarding_pass[:-3], ("F", "B"))
    col = decode_number(boarding_pass[-3:], ("L", "R"))
    return row * 8 + col


def process_boarding_passes(boarding_pass_file: io.TextIOWrapper) -> list[int]:
    return [
        parse_boarding_pass(boarding_pass)
        for boarding_pass in
        (line.strip() for line in boarding_pass_file if line.strip())
    ]


def find_highest_seat_id(boarding_passes: list[int]) -> int:
    return max(boarding_passes)


def find_empty_seat(boarding_passes: list[tuple[int, int, int]]) -> int:
    passes = sorted(boarding_passes)
    for pre, cur, nex in zip(passes, passes[1:-1], passes[2:]):
        if pre + 1 != cur:
            return pre + 1
        elif nex - 1 != cur:
            return nex - 1

    return -1


if __name__ == "__main__":
    boarding_pass_path = pathlib.Path(__file__).parent / "boarding_passes.txt"
    with boarding_pass_path.open() as boarding_pass_file:
        boarding_passes = process_boarding_passes(boarding_pass_file)
        print(find_highest_seat_id(boarding_passes))
        print(find_empty_seat(boarding_passes))
