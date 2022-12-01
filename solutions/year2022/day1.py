from __future__ import annotations

from collections.abc import Iterator


def _get_calories_per_elf(data: str) -> Iterator[int]:
    for elf in data.split("\n\n"):
        yield sum(map(int, elf.split("\n")))


def part1(data: str) -> str | int:
    return max(_get_calories_per_elf(data))


def part2(data: str) -> str | int:
    return sum(sorted(_get_calories_per_elf(data), reverse=True)[:3])
