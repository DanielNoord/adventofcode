from __future__ import annotations


def part1(data: str) -> str | int:
    grid = [list(map(int, y)) for y in data.splitlines()]
    score = 0
    length_of_x = len(grid[0]) - 1
    length_of_y = len(grid) - 1

    for y_coord, y_values in enumerate(grid):
        for x_coord, x_value in enumerate(y_values):
            if not x_coord or x_value >= max(y_values[:x_coord]) + 1:
                score += 1
            elif length_of_x == x_coord or x_value >= max(y_values[x_coord + 1 :]) + 1:
                score += 1
            elif not y_coord or x_value >= max(y[x_coord] for y in grid[:y_coord]) + 1:
                score += 1
            elif (
                length_of_y == y_coord
                or x_value >= max(y[x_coord] for y in grid[y_coord + 1 :]) + 1
            ):
                score += 1
    return score


def _find_furhest_neighbour(value: int, neighbours: list[int]) -> int:
    score = 0
    for neighbour in neighbours:
        score += 1
        if neighbour >= value:
            return score
    return score


def part2(data: str) -> str | int:
    grid = [list(map(int, y)) for y in data.splitlines()]
    best_score = 0

    for y_coord, y_values in enumerate(grid):
        for x_coord, x_value in enumerate(y_values):
            if not x_coord or not y_coord:
                continue
            score = _find_furhest_neighbour(x_value, y_values[x_coord - 1 :: -1])
            score *= _find_furhest_neighbour(x_value, y_values[x_coord + 1 :])
            score *= _find_furhest_neighbour(
                x_value, [y[x_coord] for y in grid[y_coord - 1 :: -1]]
            )
            score *= _find_furhest_neighbour(
                x_value, [y[x_coord] for y in grid[y_coord + 1 :]]
            )
            if score > best_score:
                best_score = score
    return best_score
