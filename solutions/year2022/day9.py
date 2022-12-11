from __future__ import annotations

# pylint: disable=consider-using-namedtuple-or-dataclass

MOVES: dict[str, tuple[int, int]] = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def _do_step(head_x: int, head_y: int, tail_x: int, tail_y: int) -> tuple[int, int]:
    diff_x = head_x - tail_x
    diff_y = head_y - tail_y

    if diff_x > 1 or diff_x < -1:
        if diff_y == 2:
            diff_y = 1
        if diff_y == -2:
            diff_y = -1
        return tail_x + (diff_x // 2), tail_y + diff_y
    if diff_y > 1 or diff_y < -1:
        if diff_x == 2:
            diff_x = 1
        if diff_x == -2:
            diff_x = -1
        return tail_x + diff_x, tail_y + (diff_y // 2)
    return tail_x, tail_y


def part1(data: str) -> str | int:
    head, tail = (0, 0), (0, 0)
    visited: set[tuple[int, int]] = set()
    for instruction in data.splitlines():
        direction, steps = instruction.split()
        for _ in range(int(steps)):
            move = MOVES[direction]
            head = (head[0] + move[0], head[1] + move[1])
            tail = _do_step(head[0], head[1], tail[0], tail[1])
            visited.add(tail)
    return len(visited)


def part2(data: str) -> str | int:
    knots = [(0, 0) for _ in range(10)]
    visited: set[tuple[int, int]] = set()
    for instruction in data.splitlines():
        direction, steps = instruction.split()
        for _ in range(int(steps)):
            move = MOVES[direction]
            for i, knot in enumerate(knots):
                if not i:
                    knots[i] = (knot[0] + move[0], knot[1] + move[1])
                else:
                    knots[i] = _do_step(
                        knots[i - 1][0], knots[i - 1][1], knot[0], knot[1]
                    )
            visited.add(knots[9])
    return len(visited)
