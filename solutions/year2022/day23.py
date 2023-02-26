from __future__ import annotations

from collections import Counter
from enum import StrEnum, auto
from itertools import count


class Direction(StrEnum):
    """Possible movement directions."""

    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


def _can_go_north(elf: tuple[int, int], map_: set[tuple[int, int]]) -> bool:
    return all(
        coord not in map_
        for coord in (
            (elf[0] - 1, elf[1] - 1),
            (elf[0], elf[1] - 1),
            (elf[0] + 1, elf[1] - 1),
        )
    )


def _can_go_south(elf: tuple[int, int], map_: set[tuple[int, int]]) -> bool:
    return all(
        coord not in map_
        for coord in (
            (elf[0] - 1, elf[1] + 1),
            (elf[0], elf[1] + 1),
            (elf[0] + 1, elf[1] + 1),
        )
    )


def _can_go_east(elf: tuple[int, int], map_: set[tuple[int, int]]) -> bool:
    return all(
        coord not in map_
        for coord in (
            (elf[0] + 1, elf[1] - 1),
            (elf[0] + 1, elf[1]),
            (elf[0] + 1, elf[1] + 1),
        )
    )


def _can_go_west(elf: tuple[int, int], map_: set[tuple[int, int]]) -> bool:
    return all(
        coord not in map_
        for coord in (
            (elf[0] - 1, elf[1] - 1),
            (elf[0] - 1, elf[1]),
            (elf[0] - 1, elf[1] + 1),
        )
    )


# pylint: disable=too-many-branches, too-many-return-statements
def _find_direction(
    north: bool, south: bool, east: bool, west: bool, round_number: int
) -> Direction | None:
    if round_number % 4 == 0:  # pylint: disable=compare-to-zero
        if north:
            return Direction.NORTH
        if south:
            return Direction.SOUTH
        if west:
            return Direction.WEST
        if east:
            return Direction.EAST
        return None
    if round_number % 4 == 1:
        if south:
            return Direction.SOUTH
        if west:
            return Direction.WEST
        if east:
            return Direction.EAST
        if north:
            return Direction.NORTH
        return None
    if round_number % 4 == 2:
        if west:
            return Direction.WEST
        if east:
            return Direction.EAST
        if north:
            return Direction.NORTH
        if south:
            return Direction.SOUTH
        return None
    assert round_number % 4 == 3
    if east:
        return Direction.EAST
    if north:
        return Direction.NORTH
    if south:
        return Direction.SOUTH
    if west:
        return Direction.WEST
    return None


def _do_round(
    initial_map: set[tuple[int, int]], round_number: int
) -> tuple[set[tuple[int, int]], dict[tuple[int, int], tuple[int, int]]]:
    map_with_proposals: dict[tuple[int, int], tuple[int, int]] = {}
    proposals: Counter[tuple[int, int]] = Counter()
    new_map: set[tuple[int, int]] = set()

    for elf in initial_map:
        may_go_north = _can_go_north(elf, initial_map)
        may_go_south = _can_go_south(elf, initial_map)
        may_go_east = _can_go_east(elf, initial_map)
        may_go_west = _can_go_west(elf, initial_map)

        if may_go_north and may_go_south and may_go_east and may_go_west:
            new_map.add(elf)
        else:
            direction = _find_direction(
                may_go_north, may_go_south, may_go_east, may_go_west, round_number
            )
            if direction is None:
                new_map.add(elf)
            elif direction is Direction.NORTH:
                map_with_proposals[elf] = (elf[0], elf[1] - 1)
                proposals[(elf[0], elf[1] - 1)] += 1
            elif direction is Direction.SOUTH:
                map_with_proposals[elf] = (elf[0], elf[1] + 1)
                proposals[(elf[0], elf[1] + 1)] += 1
            elif direction is Direction.WEST:
                map_with_proposals[elf] = (elf[0] - 1, elf[1])
                proposals[(elf[0] - 1, elf[1])] += 1
            elif direction is Direction.EAST:
                map_with_proposals[elf] = (elf[0] + 1, elf[1])
                proposals[(elf[0] + 1, elf[1])] += 1
            else:
                new_map.add(elf)

    return (
        new_map
        | {v if proposals[v] == 1 else k for k, v in map_with_proposals.items()},
        map_with_proposals,
    )


def _get_initial_map(data: str) -> set[tuple[int, int]]:
    map_: set[tuple[int, int]] = set()
    for y_index, y_row in enumerate(data.splitlines()):
        for x_index, x_row in enumerate(y_row):
            if x_row == "#":
                map_.add((x_index, y_index))
    return map_


def part1(data: str) -> str | int:
    map_ = _get_initial_map(data)

    for i in range(10):
        map_, _proposals = _do_round(map_, i)

    min_y = min(i[1] for i in map_)
    max_y = max(i[1] for i in map_)
    min_x = min(i[0] for i in map_)
    max_x = max(i[0] for i in map_)

    return (max_y - min_y + 1) * (max_x - min_x + 1) - len(map_)


def part2(data: str) -> str | int:
    map_ = _get_initial_map(data)

    for i in count():
        map_, proposals = _do_round(map_, i)
        if not proposals:
            return i + 1

    min_y = min(i[1] for i in map_)
    max_y = max(i[1] for i in map_)
    min_x = min(i[0] for i in map_)
    max_x = max(i[0] for i in map_)

    return (max_y - min_y + 1) * (max_x - min_x + 1) - len(map_)
