from __future__ import annotations

import sys

from helpers.iterators import one_dimensional_neighbours

# pylint: disable=too-many-arguments


def _exceeds_max_bounds(
    coords: tuple[int, int, int], max_x: int, max_y: int, max_z: int
) -> bool:
    if coords[0] < -1 or max_x < coords[0]:
        return True
    if coords[1] < -1 or max_y < coords[1]:
        return True
    if coords[2] < -1 or max_z < coords[2]:
        return True
    return False


def _fill_neighbours(
    coords: tuple[int, int, int],
    max_x: int,
    max_y: int,
    max_z: int,
    seen: set[tuple[int, int, int]],
    droplets: set[tuple[int, int, int]],
) -> int:
    faces = 0
    for neighbour in one_dimensional_neighbours(*coords):
        if neighbour in droplets:
            faces += 1
        elif neighbour in seen:
            continue
        elif not _exceeds_max_bounds(neighbour, max_x, max_y, max_z):
            seen.add(neighbour)
            faces += _fill_neighbours(neighbour, max_x, max_y, max_z, seen, droplets)
    return faces


def part1(data: str) -> str | int:
    seen_droplets: set[tuple[int, int, int]] = set()
    for droplet in data.splitlines():
        seen_droplets.add(tuple(map(int, droplet.split(","))))  # type: ignore[arg-type]
    return sum(
        neigh not in seen_droplets
        for drop in seen_droplets
        for neigh in one_dimensional_neighbours(*drop)
    )


def part2(data: str) -> str | int:
    droplets: set[tuple[int, int, int]] = set()
    max_x, max_y, max_z = 0, 0, 0
    for droplet in data.splitlines():
        parsed_droplet = tuple(map(int, droplet.split(",")))
        if parsed_droplet[0] > max_x:
            max_x = parsed_droplet[0]
        if parsed_droplet[1] > max_y:
            max_y = parsed_droplet[1]
        if parsed_droplet[2] > max_z:
            max_z = parsed_droplet[2]
        droplets.add(parsed_droplet)  # type: ignore[arg-type]

    # I guess this is a sign of how optimized this all is...
    sys.setrecursionlimit(10000)
    return _fill_neighbours(
        (-1, -1, -1), max_x + 1, max_y + 1, max_z + 1, set(), droplets
    )
