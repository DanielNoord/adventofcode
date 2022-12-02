from __future__ import annotations

# pylint: disable=consider-using-namedtuple-or-dataclass

OUTCOMES = {
    "A": {"X": 4, "Y": 8, "Z": 3},
    "B": {"X": 1, "Y": 5, "Z": 9},
    "C": {"X": 7, "Y": 2, "Z": 6},
}
NEEDED_TO_GET = {
    "A": {"X": 3, "Y": 4, "Z": 8},
    "B": {"X": 1, "Y": 5, "Z": 9},
    "C": {"X": 2, "Y": 6, "Z": 7},
}


def part1(data: str) -> str | int:
    total = 0
    for game in data.split("\n"):
        opp, you = game.split(" ")
        total += OUTCOMES[opp][you]
    return total


def part2(data: str) -> str | int:
    total = 0
    for game in data.split("\n"):
        opp, you = game.split(" ")
        total += NEEDED_TO_GET[opp][you]
    return total
