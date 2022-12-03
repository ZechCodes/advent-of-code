from input_parser import parse


def get_game_score_following_the_guide_correctly() -> int:
    points = {
        "X": {
            "A": 3,
            "B": 1,
            "C": 2,
        },
        "Y": {
            "A": 1 + 3,
            "B": 2 + 3,
            "C": 3 + 3,
        },
        "Z": {
            "A": 2 + 6,
            "B": 3 + 6,
            "C": 1 + 6,
        },
    }
    return sum(points[result][opponent] for opponent, result in parse())


if __name__ == "__main__":
    print(f"If you correctly follow the guide you were given you will score {get_game_score_following_the_guide_correctly():,} points.")
