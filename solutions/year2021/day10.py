from __future__ import annotations

OPENERS = {"(": ")", "{": "}", "[": "]", "<": ">"}
COR_ILLEGALS = {")": 3, "]": 57, "}": 1197, ">": 25137}
INC_ILLEGALS = {")": 1, "]": 2, "}": 3, ">": 4}


def _check_line(line: str) -> tuple[int, list[str]]:
    """Checks a line for corruption and incompleteness."""
    delimiters: list[str] = []
    for char in line:
        if char in OPENERS:
            delimiters.append(char)
        else:
            if char != OPENERS[delimiters[-1]]:
                return COR_ILLEGALS[char], delimiters
            delimiters.pop()
    return 0, delimiters


def part1(data: str) -> str | int:
    corruption_score = 0

    for line in data.split("\n"):
        correction_illegal, _ = _check_line(line)
        corruption_score += correction_illegal

    return corruption_score


def part2(data: str) -> str | int:
    incomplete_score: list[int] = []

    for line in data.split("\n"):
        corruption_score, delimiters = _check_line(line)
        if not corruption_score:
            score = 0
            for unclosed in delimiters[::-1]:
                score *= 5
                score += INC_ILLEGALS[OPENERS[unclosed]]
            incomplete_score.append(score)
    return sorted(incomplete_score)[len(incomplete_score) // 2]
