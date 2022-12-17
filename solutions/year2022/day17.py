from __future__ import annotations

import itertools
from collections import defaultdict
from collections.abc import Iterator

# pylint: disable=too-many-locals

ROCKS: list[list[tuple[int, int]]] = [
    [(3, 0), (4, 0), (5, 0), (6, 0)],
    [(4, 2), (3, 1), (4, 1), (5, 1), (4, 0)],
    [(5, 2), (5, 1), (3, 0), (4, 0), (5, 0)],
    [(3, 3), (3, 2), (3, 1), (3, 0)],
    [(3, 1), (4, 1), (3, 0), (4, 0)],
]

JETS: dict[str, int] = {">": 1, "<": -1}

ROCK_MOVES: dict[tuple[int, ...], list[int]] = {}


def move_x(rock_xs: list[int], jet: int) -> list[int]:
    if (*rock_xs, jet) in ROCK_MOVES:
        return ROCK_MOVES[*rock_xs, jet]

    new_list: list[int] = []
    for x in rock_xs:
        if not 0 < x + jet < 8:
            return rock_xs
        new_list.append(x + jet)

    ROCK_MOVES[*rock_xs, jet] = new_list
    return new_list


def _move_rock(
    rock: list[tuple[int, int]],
    jets_order: list[int],
    jet_indices: Iterator[int],
    max_height: int,
    heights: defaultdict[int, set[int]],
) -> tuple[int, defaultdict[int, set[int]], int]:
    # Move rock until it hits something below
    while True:
        jet_index = next(jet_indices)
        jet = jets_order[jet_index]

        # Find x-axis move
        cur_xs = [x for x, _ in rock]
        new_xs = move_x(cur_xs, jet)
        if not new_xs == cur_xs:
            pot_rock = [(new_xs[i], y) for i, (x, y) in enumerate(rock)]
            if not any(coord[0] in heights[coord[1]] for coord in pot_rock):
                rock = pot_rock

        # Find y-axis move
        for coord in rock:
            # Break if we collide
            if coord[0] in heights[coord[1] - 1]:
                max_height = max(max_height, max(coord[1] for coord in rock))
                for coord_two in rock:
                    heights[coord_two[1]].add(coord_two[0])
                break
        else:
            # Move rock down
            rock = [(x, y - 1) for x, y in rock]
            continue
        return max_height, heights, jet_index


def part1(data: str) -> str | int:
    # Create infinite iterator for jets, use index as that is useful in part 2
    jets_order = [JETS[j] for j in data]
    jet_indices = itertools.cycle(range(len(jets_order)))

    heights: defaultdict[int, set[int]] = defaultdict(set)
    heights[0] = {1, 2, 3, 4, 5, 6, 7}
    max_height = 0

    for rock_index in range(2022):
        rock = ROCKS[rock_index % 5]
        rock = [(x, y + max_height + 4) for x, y in rock]

        max_height, heights, _jets_index = _move_rock(
            rock, jets_order, jet_indices, max_height, heights
        )

    return max_height


def part2(data: str) -> str | int:
    # Create infinite iterator for jets
    jets_order = [JETS[j] for j in data]
    jet_indices = itertools.cycle(range(len(jets_order)))
    jet_index = -100

    heights: defaultdict[int, set[int]] = defaultdict(set)
    heights[0] = {1, 2, 3, 4, 5, 6, 7}
    max_height = 0

    seen_starts: dict[tuple[int, int, tuple[int, ...]], tuple[int, int]] = {}

    for rock_index in range(1000000000000):
        rock = ROCKS[rock_index % 5]
        rock = [(x, y + max_height + 4) for x, y in rock]

        # Determine characteristics of starting position
        heighest_x: list[int] = [0, 0, 0, 0, 0, 0, 0, 0]
        for key, x_values in heights.items():
            for x in x_values:
                if key > heighest_x[x]:
                    heighest_x[x] = key
        best: tuple[int, ...] = tuple(max_height + 4 - i for i in heighest_x[1:])

        # Check if this is a recurring starting position
        if (start := (jet_index + 1, rock_index % 5, best)) in seen_starts:
            rock_index_increase = rock_index - seen_starts[start][0]
            max_height_increase = max_height - seen_starts[start][1]
            count = (1000000000000 - rock_index) // rock_index_increase
            rock_index += count * rock_index_increase
            break

        seen_starts[start] = (rock_index, max_height)

        max_height, heights, jet_index = _move_rock(
            rock, jets_order, jet_indices, max_height, heights
        )

    for rock_index in range(rock_index, 1000000000000):
        rock = ROCKS[rock_index % 5]
        rock = [(x, y + max_height + 4) for x, y in rock]

        max_height, heights, _jets_index = _move_rock(
            rock, jets_order, jet_indices, max_height, heights
        )

    return max_height + count * max_height_increase
