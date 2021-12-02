def find(rounds: int, *start: int):
    said = dict(zip(start, range(len(start))))
    inserting = 0 if start[-1] not in start[:-1] else start[-2::-1].index(start[-1]) + 1
    last = 0
    for i in range(len(start), rounds):
        next_number = 0
        if inserting in said:
            next_number = i - said[inserting]

        said[inserting] = i
        last, inserting = inserting, next_number

    return last


if __name__ == "__main__":
    print("Tests")
    tests = {
        1: (1, 3, 2),
        10: (2, 1, 3),
        27: (1, 2, 3),
        78: (2, 3, 1),
        436: (0, 3, 6),
        438: (3, 2, 1),
        1836: (3, 1, 2),
    }
    for solution, start in tests.items():
        print(f"\n{start}: {find(2020, *start)} = {solution}")

    print()
    print("Final")
    print(find(2020, 12, 20, 0, 6, 1, 17, 7))
    print(find(30_000_000, 12, 20, 0, 6, 1, 17, 7))
