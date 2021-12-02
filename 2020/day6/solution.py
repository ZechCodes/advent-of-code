import io
import itertools
import pathlib


def process_answers_file(input_file: io.TextIOWrapper) -> list[set[str]]:
    groups = []
    current = set()
    for line in (l.strip() for l in input_file):
        if line:
            current.update(set(line))
        else:
            groups.append(current)
            current = set()
    else:
        groups.append(current)

    return groups


def process_answers_file_all_yes(input_file: io.TextIOWrapper) -> list[set[str]]:
    groups = []
    current = None
    for line in (l.strip() for l in input_file):
        if line:
            answers = set(line)
            current = answers if current is None else current.intersection(answers)
        else:
            groups.append(current)
            current = None
    else:
        groups.append(current)

    return groups


if __name__ == "__main__":
    input_file_path = pathlib.Path(__file__).parent / "input.txt"

    with input_file_path.open() as input_file:
        answers = process_answers_file(input_file)
    print(len(list(itertools.chain(*answers))))

    with input_file_path.open() as input_file:
        answers = process_answers_file_all_yes(input_file)
    print(len(list(itertools.chain(*answers))))
