from input_parser import parse


def get_game_score_following_the_guide() -> int:
    beats = {
        "A": "Z",
        "B": "X",
        "C": "Y",
        "X": "C",
        "Y": "A",
        "Z": "B",
    }
    points = {
        "X": 1,
        "Y": 2,
        "Z": 3,
    }
    plays = parse()
    score = 0
    for opponent, me in plays:
        score += points[me]
        if beats[me] == opponent:
            score += 6

        elif beats.get(opponent) != me:
            score += 3

    return score


if __name__ == "__main__":
    print(f"If you follow the guide you were given you will score {get_game_score_following_the_guide():,} points.")
