from __future__ import annotations
from typing import Optional
import io
import itertools
import pathlib


class Universe:
    def __init__(self, dimensions):
        self.cells = {}
        self.dimensions = dimensions

    def __getitem__(self, coords: tuple[int, int, int, int]) -> Optional[Cell]:
        return self.cells.get(coords, Cell(False, coords, self))

    def __setitem__(self, coords: tuple[int, int, int, int], active: bool):
        if coords in self:
            self[coords].active = active
        else:
            self.cells[coords] = Cell(active, coords, self)

    def __contains__(self, coords: tuple[int, int, int, int]) -> bool:
        return coords in self.cells


class Cell:
    def __init__(self, active: bool,  coords: tuple[int, int, int, int], universe: Universe):
        self.active = active
        self.coords = coords
        self.universe = universe

    def create_neighbors(self):
        if not self.active:
            return

        for delta in itertools.product((-1, 0, 1), repeat=self.universe.dimensions):
            coords = tuple(v1 + v2 for v1, v2 in zip(self.coords, delta))
            if coords != self.coords and coords not in self.universe:
                self.universe[coords] = False

    def get_neighbors(self) -> list[Cell]:
        return [
            self.universe[tuple(v1 + v2 for v1, v2 in zip(self.coords, delta))]
            for delta in itertools.product((-1, 0, 1), repeat=self.universe.dimensions)
            if any(delta)
        ]


def process_input(input_file: io.TextIOWrapper, dimensions) -> Universe:
    universe = Universe(dimensions)
    for y, line in enumerate(l.strip() for l in input_file):
        for x, state in enumerate(line):
            universe[tuple([x, y] + [0 for _ in range(dimensions - 2)])] = state == "#"

    return universe


def get_active_cells(universe: Universe) -> int:
    return sum(cell.active for cell in universe.cells.values())


def iterate_universe(universe: Universe, iterations: int, dimensions: int) -> Universe:
    next_gen_universe = Universe(dimensions)
    for cell in list(universe.cells.values()):
        cell.create_neighbors()

    for cell in universe.cells.values():
        active_neighbors = sum(neighbor.active for neighbor in cell.get_neighbors())
        if cell.active and 2 <= active_neighbors <= 3:
            next_gen_universe[cell.coords] = True
        elif not cell.active and active_neighbors == 3:
            next_gen_universe[cell.coords] = True
        elif active_neighbors:
            next_gen_universe[cell.coords] = False

    return next_gen_universe if iterations == 1 else iterate_universe(next_gen_universe, iterations - 1, dimensions)


if __name__ == "__main__":
    input_file_path = pathlib.Path(__file__).parent / "test_input.txt"
    with input_file_path.open() as input_file:
        universe = process_input(input_file, 4)

    assert get_active_cells(universe) == 5, "Not enough active cells"
    gen_6_universe = iterate_universe(universe, 6, 4)
    print(get_active_cells(gen_6_universe), 848)

    print("\n----\nFinal")
    input_file_path = pathlib.Path(__file__).parent / "input.txt"
    with input_file_path.open() as input_file:
        universe = process_input(input_file, 4)

    gen_6_universe = iterate_universe(universe, 6, 4)
    print(get_active_cells(gen_6_universe))
