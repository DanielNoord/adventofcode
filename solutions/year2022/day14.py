from __future__ import annotations

import itertools
from collections import defaultdict

# pylint: disable=unsubscriptable-object


def _make_rock_grid(data: str) -> tuple[list[list[str]], int]:
    rocks: defaultdict[int, set[int]] = defaultdict(set)
    max_y = 0
    for rock in data.splitlines():
        previous: tuple[int, int] | None = None
        for point in rock.split(" -> "):
            x, y = map(int, point.split(","))
            rocks[x].add(y)
            if previous is not None:
                if previous[0] == x:
                    for i in range(min(previous[1], y), max(previous[1], y) + 1):
                        rocks[x].add(i)
                elif previous[1] == y:
                    for i in range(min(previous[0], x), max(previous[0], x) + 1):
                        rocks[i].add(y)
            previous = (x, y)
            max_y = max(max_y, y)

    min_rocks = min(rocks)
    grid: list[list[str]] = [
        ["." for _ in range(min(rocks), max(rocks) + 1)] for _ in range(max_y + 1)
    ]
    for y, row in enumerate(grid):
        for x, _coord in enumerate(row):
            if y in rocks[x + min_rocks]:
                row[x] = "#"
    return grid, 500 - min_rocks


def _add_sand(grid: list[list[str]], sand_x: int) -> tuple[list[list[str]], int]:
    start_x, sand_y = sand_x, 0
    while True:
        if sand_x - 1 < 0:
            grid = [["."] + y for y in grid]
            grid[-1][0] = "#"
            sand_x += 1
            start_x += 1
        elif sand_x + 1 >= len(grid[0]) - 1:
            grid = [y + ["."] for y in grid]
            grid[-1][-1] = "#"
        if grid[sand_y][sand_x] == ".":
            sand_y += 1
        elif grid[sand_y][sand_x] in {"#", "o"}:
            if grid[sand_y][sand_x - 1] == ".":
                sand_x -= 1
            elif grid[sand_y][sand_x + 1] == ".":
                sand_x += 1
            else:
                grid[sand_y - 1][sand_x] = "o"
                return grid, start_x


def part1(data: str) -> str | int:
    grid, sand_x = _make_rock_grid(data)

    sand_unit = 0
    for sand_unit in itertools.count():
        try:
            grid, _start_x = _add_sand(grid, sand_x)
        except IndexError:
            break
    return sand_unit


def part2(data: str) -> str | int:
    grid, start_x = _make_rock_grid(data)

    max_x = len(grid[0])
    grid.append(["." for _ in range(max_x)])
    grid.append(["#" for _ in range(max_x)])

    sand_unit = 0
    for sand_unit in itertools.count():
        if grid[0][start_x] == "o":
            break
        grid, start_x = _add_sand(grid, start_x)
    return sand_unit
