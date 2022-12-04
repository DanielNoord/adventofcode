from __future__ import annotations

from typing import Literal


def _fold_dots(
    dots: set[tuple[int, int]], axis: Literal["x", "y"], coord: int
) -> set[tuple[int, int]]:
    new_dots: set[tuple[int, int]] = set()
    if axis == "x":
        for x, y in dots:
            if x < coord:
                new_dots.add((x, y))
            else:
                new_dots.add((coord + coord - x, y))
    else:
        for x, y in dots:
            if y < coord:
                new_dots.add((x, y))
            else:
                new_dots.add((x, coord + coord - y))

    return new_dots


def part1(data: str) -> str | int:
    state, instructions = data.split("\n\n")
    dots = {tuple(map(int, pair.split(","))) for pair in state.splitlines()}

    for instruction in instructions.splitlines():
        axis, coord = instruction[11:].split("=")
        dots = _fold_dots(dots, axis, int(coord))  # type: ignore[arg-type, assignment]
        # We only do the first instruction in part one
        break

    return len(dots)


def part2(data: str) -> str | int:
    state, instructions = data.split("\n\n")
    dots = {tuple(map(int, pair.split(","))) for pair in state.splitlines()}
    max_x = 0
    max_y = 0

    for instruction in instructions.splitlines():
        axis, coord = instruction[11:].split("=")
        dots = _fold_dots(dots, axis, int(coord))  # type: ignore[arg-type, assignment]
        if axis == "x":
            max_x = int(coord)
        else:
            max_y = int(coord)
    final_dots = sorted(dots)
    output_string = ""
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) in final_dots:
                output_string += "#"
            else:
                output_string += "."
        output_string += "\n"

    return output_string[:-1]  # To remove last new line
