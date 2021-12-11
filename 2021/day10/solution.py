from __future__ import annotations


def compute_line_auto_completions_scores(
    auto_completions: list[list[str]],
) -> list[int]:
    return [
        compute_line_auto_completion_score(auto_completion)
        for auto_completion in auto_completions
    ]


def compute_line_auto_completion_score(line_auto_completion: list[str]) -> int:
    points = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    score = 0
    for token in line_auto_completion:
        score *= 5
        score += points[token]

    return score


def find_first_syntax_error_on_line(line: str) -> str | None:
    token_pairs = {"[": "]", "(": ")", "{": "}", "<": ">"}
    stack = []
    for token in line:
        if token in token_pairs:
            stack.append(token_pairs[token])

        elif token != stack.pop():
            return token

    return None


def generate_line_auto_completion(line: str) -> list[str] | None:
    token_pairs = {"[": "]", "(": ")", "{": "}", "<": ">"}
    stack = []
    for token in line:
        if token in token_pairs:
            stack.append(token_pairs[token])

        elif token != stack.pop():
            return None

    return stack[::-1]


def get_line_auto_completions(code: list[str]) -> list[list[str]]:
    auto_completions = []
    for line in code:
        auto_completion = generate_line_auto_completion(line)
        if auto_completion:
            auto_completions.append(auto_completion)

    return auto_completions


def get_incorrect_characters(code: list[str]) -> list[str]:
    incorrect = []
    for line in code:
        result = find_first_syntax_error_on_line(line)
        if result:
            incorrect.append(result)

    return incorrect


def get_test_data() -> list[str]:
    return [
        "[({(<(())[]>[[{[]{<()<>>",
        "[(()[<>])]({[<{<<[]>>(",
        "{([(<{}[<>[]}>{[]{[(<()>",
        "(((({<>}<{<{<>}{[]{[]{}",
        "[[<[([]))<([[{}[[()]]]",
        "[{[{({}]{}}([{[{{{}}([]",
        "{<[[]]>}<{[{[{[]{()[[[]",
        "[<(<(<(<{}))><([]([]()",
        "<{([([[(<>()){}]>(<<{{",
        "<{([{{}}[<[[[<>{}]]]>[]]",
    ]


def get_input_data() -> list[str]:
    with open("input.txt", "r") as input_file:
        return [line.strip() for line in input_file]


def get_solution_1_result(code: list[str]) -> int:
    values = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    incorrect = get_incorrect_characters(code)
    return sum(values[character] for character in incorrect)


def test_1():
    data = get_test_data()
    result = get_solution_1_result(data)
    assert result == 26397


def solution_1():
    data = get_input_data()
    result = get_solution_1_result(data)
    print(f"Solution 1 is {result}")


# ### Solution 2 ### #


def get_solution_2_result(code: list[str]) -> int:
    completions = get_line_auto_completions(code)
    result = sorted(compute_line_auto_completions_scores(completions))
    return result[len(result) // 2]


def test_2():
    data = get_test_data()
    result = get_solution_2_result(data)
    assert result == 288957


def solution_2():
    data = get_input_data()
    result = get_solution_2_result(data)
    print(f"Solution 2 is {result}")


if __name__ == "__main__":
    test_1()
    solution_1()
    test_2()
    solution_2()
