from __future__ import annotations

from collections.abc import Callable


def part1(data: str) -> str | int:
    positions = sorted(int(i) for i in data.split(","))

    last_fuel = float("inf")
    for position in range(positions[-1]):
        if (fuel := sum(abs(i - position) for i in positions)) > last_fuel:
            break
        last_fuel = fuel

    return int(last_fuel)


def part2(data: str) -> str | int:
    positions = sorted(int(i) for i in data.split(","))

    last_fuel = float("inf")
    sum_of_integers: Callable[[int], float] = lambda x: (x * (x + 1)) / 2
    for position in range(positions[-1]):
        if (
            fuel := sum(sum_of_integers(abs(i - position)) for i in positions)
        ) > last_fuel:
            break
        last_fuel = fuel
    return int(last_fuel)
