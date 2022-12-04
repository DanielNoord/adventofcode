from __future__ import annotations

from collections.abc import Callable

# pylint: disable=consider-using-namedtuple-or-dataclass

ACTIONS = {"forward": (1, 0), "up": (0, -1), "down": (0, 1)}
ACTIONS_WITH_AIM: dict[str, tuple[int, Callable[[tuple[int, int, int]], int], int]] = {
    "forward": (1, lambda x: x[2], 0),
    "up": (0, lambda x: 0, -1),
    "down": (0, lambda x: 0, 1),
}


def part1(data: str) -> str | int:
    lines = [i.split(" ") for i in data.splitlines()]
    coords = (0, 0)
    for move in lines:
        action = ACTIONS[move[0]]
        coords = (
            coords[0] + action[0] * int(move[1]),
            coords[1] + action[1] * int(move[1]),
        )
    return coords[0] * coords[1]


def part2(data: str) -> str | int:
    lines = [i.split(" ") for i in data.splitlines()]
    coords = (0, 0, 0)
    for move in lines:
        action = ACTIONS_WITH_AIM[move[0]]
        coords = (
            coords[0] + action[0] * int(move[1]),
            coords[1] + action[1](coords) * int(move[1]),
            coords[2] + action[2] * int(move[1]),
        )
    return coords[0] * coords[1]
