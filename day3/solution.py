import io
import math
import pathlib

TreeMap = list[list[bool]]


def count_trees_crossing_map(x_move: int, y_move: int, tree_map: TreeMap):
    x = y = tree_count = 0
    while y < len(tree_map):
        if tree_map[y][x]:
            tree_count += 1

        x = (x + x_move) % len(tree_map[0])
        y += y_move

    return tree_count


def create_map(map_grid_file: io.TextIOWrapper) -> TreeMap:
    return [
        [space == "#" for space in row.strip()]
        for row in map_grid_file
        if row.strip()
    ]


if __name__ == "__main__":
    map_path = pathlib.Path(__file__).parent / "map.txt"
    with map_path.open() as map_grid_file:
        tree_map = create_map(map_grid_file)
        print(count_trees_crossing_map(3, 1, tree_map))
        print(
            math.prod(
                count_trees_crossing_map(x, y, tree_map)
                for x, y in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
            )
        )
