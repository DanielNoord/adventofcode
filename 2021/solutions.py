#! /usr/bin/env python3
"""Solutions to year 2021"""

import time

INPUT_FILES = dict((f"day{i+1}", f"2021/inputs/input{i+1}.txt") for i in range(25))

# https://adventofcode.com/2021/day/1
def day1(input_file: str) -> None:
    """Answer 1 is 1226
    Answer 2 is 1252
    """
    lines = [int(i) for i in input_file.split("\n") if i]
    increases = 0
    for index, line in enumerate(lines[:-1]):
        if lines[index + 1] > line:
            increases += 1
    print("Number of depth increases is:", increases)

    increases_window = 0
    for index, line in enumerate(lines[:-3]):
        if (
            line + lines[index + 1] + lines[index + 2]
            < lines[index + 1] + lines[index + 2] + lines[index + 3]
        ):
            increases_window += 1
    print("Number of 3-measure windo increases is:", increases_window)


# https://adventofcode.com/2021/day/2
def day2(input_file: str) -> None:
    """Answer 1 is ...
    Anser 2 is ...
    """
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
    solver("day2")
    # all_days()
