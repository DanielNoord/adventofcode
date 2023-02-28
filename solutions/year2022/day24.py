from __future__ import annotations

from collections.abc import Iterator
from functools import cache
from itertools import count

# pylint: disable=consider-using-namedtuple-or-dataclass,missing-class-docstring


DIRECTIONS: dict[str, tuple[int, int]] = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1),
}

Blizzards = set[tuple[tuple[int, int], tuple[int, int]]]
BlizzardPositions = set[tuple[int, int]]


class BlizzardFinder:
    def __init__(self, data: str) -> None:
        self.rounds_x_blizzards: dict[int, Blizzards] = {}

        # Set up the blizzards for the initial state
        round_zero_blizzards: Blizzards = set()
        split_data = data.splitlines()
        for y_index, y in enumerate(split_data):
            for x_index, x in enumerate(y):
                if x not in {"#", "."}:
                    round_zero_blizzards.add(((x_index, y_index), DIRECTIONS[x]))

        self.rounds_x_blizzards[0] = round_zero_blizzards
        self.base_height = len(split_data)
        self.base_width = len(split_data[0])
        self.height = self.base_height - 2
        self.width = self.base_width - 2

    def _move_blizzards(self, bliz: Blizzards) -> Blizzards:
        new_blizzards: Blizzards = set()
        for (x, y), (movex, movey) in bliz:
            if x + movex < 1:
                x += self.width
            if x + movex > self.width:
                x -= self.width
            if y + movey < 1:
                y += self.height
            if y + movey > self.height:
                y -= self.height
            new_blizzards.add(((x + movex, y + movey), (movex, movey)))
        return new_blizzards

    def get_blizzards_for_round(self, round_number: int) -> Blizzards:
        if round_number in self.rounds_x_blizzards:
            return self.rounds_x_blizzards[round_number]

        ret = self._move_blizzards(self.get_blizzards_for_round(round_number - 1))
        self.rounds_x_blizzards[round_number] = ret
        return ret

    @cache  # pylint: disable=method-cache-max-size-none
    def get_blizzard_positions_for_round(self, round_number: int) -> BlizzardPositions:
        return {bliz[0] for bliz in self.get_blizzards_for_round(round_number)}

    def round(
        self,
        round_number: int,
        position: tuple[int, int],
    ) -> Iterator[tuple[int, int]]:
        blizzards = self.get_blizzard_positions_for_round(round_number)

        # Don't allow going to the border
        return _get_moves(
            position, blizzards, self.base_height - 1, self.base_width - 1
        )

    def bfs_search(
        self,
        initial_round_number: int,
        initial_pos: tuple[int, int],
        destination: tuple[int, int],
    ) -> int:
        to_consider: set[tuple[int, int]] = {initial_pos}
        for round_number in count(initial_round_number):
            new_to_consider: set[tuple[int, int]] = set()
            for pos in to_consider:
                for move in self.round(round_number, pos):
                    # We have found a possible move
                    if move == destination:
                        return round_number + 1
                    new_to_consider.add(move)
            to_consider = new_to_consider
        raise AssertionError("No path found.")


def _get_moves(
    position: tuple[int, int], bliz: BlizzardPositions, height: int, width: int
) -> Iterator[tuple[int, int]]:
    for possible_direction in DIRECTIONS.values():
        if not 0 < position[0] + possible_direction[0] < width:
            continue
        if not 0 < position[1] + possible_direction[1] < height:
            continue
        if (
            position[0] + possible_direction[0],
            position[1] + possible_direction[1],
        ) in bliz:
            continue
        yield (position[0] + possible_direction[0], position[1] + possible_direction[1])
    if position not in bliz:
        yield position


def part1(data: str) -> str | int:
    bliz = BlizzardFinder(data)
    return bliz.bfs_search(0, (1, 0), (bliz.base_width - 2, bliz.base_height - 2))


def part2(data: str) -> str | int:
    bliz = BlizzardFinder(data)

    point_before_opening = (bliz.base_width - 2, bliz.base_height - 2)
    opening = (bliz.base_width - 2, bliz.base_height - 1)

    to_end = bliz.bfs_search(0, (1, 0), point_before_opening)
    to_begin = bliz.bfs_search(to_end, opening, (1, 1))
    return bliz.bfs_search(to_begin, (1, 0), point_before_opening)
