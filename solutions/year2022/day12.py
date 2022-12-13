from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterator

Coords = tuple[int, int]


def create_grid(data: str) -> tuple[list[list[int]], Coords, Coords]:
    grid: list[list[int]] = []
    start, end = None, None
    for y_coord, row in enumerate(data.splitlines()):
        grid.append([])
        for x_coord, char in enumerate(row):
            if char == "S":
                start = y_coord, x_coord
                grid[y_coord].append(ord("a"))
            elif char == "E":
                end = y_coord, x_coord
                grid[y_coord].append(ord("z"))
            else:
                grid[y_coord].append(ord(char))
    assert start
    assert end
    return grid, start, end


# Implementation based on what I found online ... :)
def breadth_first_search(
    grid: list[list[int]],
    start: Coords,
    destination: Coords | int,
    get_neighbors: Callable[[list[list[int]], int, int, int, int], Iterator[Coords]],
) -> int:
    height, width = len(grid), len(grid[0])
    queue: deque[tuple[int, Coords]] = deque([(0, start)])
    visited: set[Coords] = set()

    while queue:
        distance, current_coord = queue.popleft()
        y_coord, x_coord = current_coord

        if destination in {current_coord, grid[y_coord][x_coord]}:
            return distance

        if current_coord not in visited:
            visited.add(current_coord)

            for neighbour in get_neighbors(grid, y_coord, x_coord, height, width):
                if neighbour in visited:
                    continue

                queue.append((distance + 1, neighbour))

    raise AssertionError()


def all_neighbours(
    y_coord: int, x_coord: int, height: int, width: int
) -> Iterator[Coords]:
    for new_y, new_x in (
        (y_coord + 1, x_coord),
        (y_coord - 1, x_coord),
        (y_coord, x_coord + 1),
        (y_coord, x_coord - 1),
    ):
        if 0 <= new_y < height and 0 <= new_x < width:
            yield new_y, new_x


def neighbors_forward(
    grid: list[list[int]], y_coord: int, x_coord: int, height: int, width: int
) -> Iterator[Coords]:
    max_el = grid[y_coord][x_coord] + 1
    for neigh in all_neighbours(y_coord, x_coord, height, width):
        if grid[neigh[0]][neigh[1]] <= max_el:
            yield neigh


def neighbors_backward(
    grid: list[list[int]], y_coord: int, x_coord: int, height: int, width: int
) -> Iterator[Coords]:
    min_el = grid[y_coord][x_coord] - 1
    for neigh in all_neighbours(y_coord, x_coord, height, width):
        if grid[neigh[0]][neigh[1]] >= min_el:
            yield neigh


def part1(data: str) -> str | int:
    grid, start, end = create_grid(data)
    return breadth_first_search(grid, start, end, neighbors_forward)


def part2(data: str) -> str | int:
    grid, _, end = create_grid(data)
    return breadth_first_search(grid, end, ord("a"), neighbors_backward)
