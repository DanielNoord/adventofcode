from __future__ import annotations


def _find_score(letter: str) -> int:
    if (score := ord(letter) - 96) < 1:
        score += 58
    return score


def part1(data: str) -> str | int:
    score = 0
    for rucksack in data.split("\n"):
        half = len(rucksack) // 2
        for letter in rucksack[:half]:
            if letter in rucksack[half:]:
                score += _find_score(letter)
                break
    return score


def part2(data: str) -> str | int:
    rucksacks = data.split("\n")
    score = 0
    for i in range(0, len(rucksacks), 3):
        for letter in rucksacks[i]:
            if letter in rucksacks[i + 1] and letter in rucksacks[i + 2]:
                score += _find_score(letter)
                break
    return score
