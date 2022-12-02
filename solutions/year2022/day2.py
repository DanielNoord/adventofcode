from __future__ import annotations

# pylint: disable=consider-using-namedtuple-or-dataclass

OUTCOMES = {
    "A X": 4,
    "A Y": 8,
    "A Z": 3,
    "B X": 1,
    "B Y": 5,
    "B Z": 9,
    "C X": 7,
    "C Y": 2,
    "C Z": 6,
}
NEEDED_TO_GET = {
    "A X": 3,
    "A Y": 4,
    "A Z": 8,
    "B X": 1,
    "B Y": 5,
    "B Z": 9,
    "C X": 2,
    "C Y": 6,
    "C Z": 7,
}


def part1(data: str) -> str | int:
    return sum(OUTCOMES[game] for game in data.splitlines())


def part2(data: str) -> str | int:
    return sum(NEEDED_TO_GET[game] for game in data.splitlines())
