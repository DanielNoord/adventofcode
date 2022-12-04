from __future__ import annotations

from collections import Counter


def _fish_day(fish: dict[int, int]) -> dict[int, int]:
    """Compute a day of fish growth."""
    new_fish: dict[int, int] = {}
    for fish_type, amount in fish.items():
        if not fish_type:
            new_fish[8] = amount
            if 6 in new_fish:
                new_fish[6] += amount
            else:
                new_fish[6] = amount
        elif fish_type == 7:
            if 6 in new_fish:
                new_fish[6] += amount
            else:
                new_fish[6] = amount
        else:
            new_fish[fish_type - 1] = amount
    return new_fish


def part1(data: str) -> str | int:
    fish: dict[int, int] = Counter(int(i) for i in data.split(","))

    for _ in range(80):
        fish = _fish_day(fish)
    return sum(fish.values())


def part2(data: str) -> str | int:
    fish: dict[int, int] = Counter(int(i) for i in data.split(","))

    for _ in range(256):
        fish = _fish_day(fish)
    return sum(fish.values())
