#! /usr/bin/env python3
"""Solutions to year 2021"""

import time

INPUT_FILES = dict((f"day{i+1}", f"2021/inputs/input{i+1}.txt") for i in range(25))

# https://adventofcode.com/2021/day/1
def day1(input_file: str) -> None:
    lines = [int(i) for i in input_file.split("\n") if i]
    increases = 0
    for index, line in enumerate(lines[:-1]):
        if lines[index + 1] > line:
            increases += 1
    print("Number of depth increases is:", increases)
    assert increases == 1226

    increases_window = 0
    for index, line in enumerate(lines[:-3]):
        if (
            line + lines[index + 1] + lines[index + 2]
            < lines[index + 1] + lines[index + 2] + lines[index + 3]
        ):
            increases_window += 1
    print("Number of 3-measure windo increases is:", increases_window)
    assert increases_window == 1252


# https://adventofcode.com/2021/day/2
def day2(input_file: str) -> None:
    lines = [i.split(" ") for i in input_file.strip().split("\n")]
    coords = (0, 0)
    actions = {"forward": (1, 0), "up": (0, -1), "down": (0, 1)}
    for move in lines:
        action = actions[move[0]]
        coords = (
            coords[0] + action[0] * int(move[1]),
            coords[1] + action[1] * int(move[1]),
        )
    print("Multiplying the final coords gives:", coords[0] * coords[1])
    assert coords[0] * coords[1] == 2039256

    coords_aim = (0, 0, 0)
    actions_aim = {
        "forward": (1, lambda x: x[2], 0),
        "up": (0, lambda x: 0, -1),
        "down": (0, lambda x: 0, 1),
    }
    for move in lines:
        action_aim = actions_aim[move[0]]
        coords_aim = (
            coords_aim[0] + action_aim[0] * int(move[1]),
            coords_aim[1] + action_aim[1](coords_aim) * int(move[1]),  # type: ignore[no-untyped-call]
            coords_aim[2] + action_aim[2] * int(move[1]),
        )
    print("Multiplying the final coords gives:", coords_aim[0] * coords_aim[1])
    assert coords_aim[0] * coords_aim[1] == 1856459736


# https://adventofcode.com/2021/day/3
def day3(input_file: str) -> None:
    pass


def solver(day: str) -> None:
    """Solve one exercise"""
    start = time.time()
    with open(INPUT_FILES[day], "r", encoding="utf-8") as file:
        globals()[day](file.read())
    print(
        f"Execution of solution for {day} took {round((time.time() - start) * 1000, 5)} ms"
    )


def all_days() -> None:
    """Run all days at once"""
    totaltime = time.time()
    for i in range(2):
        print(f"===== DAY {i+1:2d} =====")
        solver(f"day{i+1}")
        print()
    print(
        f"Execution of all solutions took {round((time.time() - totaltime) * 1000, 5)} ms"
    )


if __name__ == "__main__":
    solver("day3")
    # all_days()
