#! /usr/bin/env python3
"""Solutions to year 2021"""

import time

INPUT_FILES = dict((f"day{i+1}", f"2021/inputs/input{i+1}.txt") for i in range(25))

# https://adventofcode.com/2021/day/1
def day1(input_file: str) -> None:
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
    for i in range(1):
        print(f"===== DAY {i+1:2d} =====")
        solver(f"day{i+1}")
        print()
    print(
        f"Execution of all solutions took {round((time.time() - totaltime) * 1000, 5)} ms"
    )


if __name__ == "__main__":
    solver("day1")
    # all_days()
