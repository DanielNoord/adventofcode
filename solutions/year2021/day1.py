from __future__ import annotations


def part1(data: str) -> str | int:
    lines = list(map(int, data.splitlines()))
    increases = 0
    for index, line in enumerate(lines[:-1]):
        if lines[index + 1] > line:
            increases += 1
    return increases


def part2(data: str) -> str | int:
    lines = list(map(int, data.splitlines()))
    increases = 0
    for index, line in enumerate(lines[:-3]):
        if (
            line + lines[index + 1] + lines[index + 2]
            < lines[index + 1] + lines[index + 2] + lines[index + 3]
        ):
            increases += 1
    return increases
