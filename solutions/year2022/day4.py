from __future__ import annotations

# pylint: disable=confusing-consecutive-elif


def part1(data: str) -> str | int:
    overlapping_pairs = 0
    for pair in data.splitlines():
        first, second = (p.split("-") for p in pair.split(","))
        if int(first[0]) > int(second[0]):
            if int(first[-1]) <= int(second[-1]):
                overlapping_pairs += 1
        elif int(second[0]) > int(first[0]):
            if int(second[-1]) <= int(first[-1]):
                overlapping_pairs += 1
        else:
            overlapping_pairs += 1
    return overlapping_pairs


def part2(data: str) -> str | int:
    overlapping_pairs = 0
    for pair in data.splitlines():
        first, second = (p.split("-") for p in pair.split(","))
        if int(first[0]) <= int(second[-1]):
            if int(first[-1]) >= int(second[0]):
                overlapping_pairs += 1
        elif int(second[0]) <= int(first[-1]):
            if int(second[-1]) >= int(first[0]):
                overlapping_pairs += 1
    return overlapping_pairs
