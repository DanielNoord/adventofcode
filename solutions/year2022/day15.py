from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator
from itertools import chain

# pylint: disable=compare-to-zero, invalid-name


def _parse_line(line: str) -> tuple[tuple[int, int], tuple[int, int]]:
    sens_x, sens_y_beac_x, beac_y = line.split(", ")
    _, sens_y, beac_x = sens_y_beac_x.split("=")
    return (int(sens_x.split("=")[1]), int(sens_y.split(":")[0])), (
        int(beac_x),
        int(beac_y[2:]),
    )


def _find_covered_x_coords_for_y(
    sensor: tuple[int, int], beacon: tuple[int, int], target: int
) -> Iterator[int]:
    manhattan_distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    y_to_cover = abs(sensor[1] - target)

    if (x_difference := manhattan_distance - y_to_cover) > -1:
        yield from range(sensor[0] - x_difference, sensor[0] + x_difference)


def _find_diamond(
    sensor: tuple[int, int], beacon: tuple[int, int]
) -> Iterator[tuple[int, tuple[int, int]]]:
    manhattan_distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    for y in range(sensor[1] - manhattan_distance, sensor[1] + manhattan_distance + 1):
        x_difference = manhattan_distance - abs(sensor[1] - y)
        yield y, (
            sensor[0] - x_difference,
            sensor[0] + x_difference,
        )


def _join_ranges(data: list[tuple[int, int]]) -> Iterator[tuple[int, int]]:
    data = sorted(
        chain.from_iterable(((start, 1), (stop + 2, -1)) for start, stop in data)
    )
    c = 0
    for value, label in data:
        if c == 0:
            x = value
        c += label
        if c == 0:
            yield x, value - 2


def part1(data: str) -> str | int:
    covered_coords: set[int] = set()
    for line in data.splitlines():
        sensor, beacon = _parse_line(line)
        covered_coords.update(_find_covered_x_coords_for_y(sensor, beacon, 2000000))

    return len(covered_coords)


def part2(data: str) -> str | int:
    y_coords: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)

    for line in data.splitlines():
        for y, new_range in _find_diamond(*_parse_line(line)):
            y_coords[y].append(new_range)

    for y in range(0, 4000001):
        if len(list(_join_ranges(y_coords[y]))) > 1:
            last_y = y
            break

    return last_y + (4000000 * (y_coords[last_y][0][1] + 1))
