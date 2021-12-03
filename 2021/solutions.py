#! /usr/bin/env python3
"""Solutions to year 2021"""

import time
from collections import Counter

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
    numbers = input_file.strip().split("\n")

    def get_bit(
        numbers: list[str], index: int, middle: float, most_common: bool
    ) -> str:
        """Get the most or least common bit for a given index"""
        if sum(number[index] == "1" for number in numbers) >= middle:
            return "1" if most_common else "0"
        return "0" if most_common else "1"

    most_common_bits = ""
    middle = len(numbers) // 2
    for index in range(len(numbers[0])):
        most_common_bits += get_bit(numbers, index, middle, True)
    gamma = int("".join(most_common_bits), 2)
    epsilon = int("".join("0" if i == "1" else "1" for i in most_common_bits), 2)
    print("Power consumption is:", gamma * epsilon)
    assert gamma * epsilon == 3309596

    oxy_numbers = numbers
    bit_pattern, index = "", 0
    while len(oxy_numbers) > 1:
        bit_pattern += get_bit(oxy_numbers, index, len(oxy_numbers) / 2, True)
        oxy_numbers = [i for i in oxy_numbers if i.startswith(bit_pattern)]
        index += 1

    co2_numbers = numbers
    bit_pattern, index = "", 0
    while len(co2_numbers) > 1:
        bit_pattern += get_bit(co2_numbers, index, len(co2_numbers) / 2, False)
        co2_numbers = [i for i in co2_numbers if i.startswith(bit_pattern)]
        index += 1
    print("Life support rating is:", int(oxy_numbers[0], 2) * int(co2_numbers[0], 2))
    assert int(oxy_numbers[0], 2) * int(co2_numbers[0], 2) == 2981085


# https://adventofcode.com/2021/day/4
def day4(input_file: str) -> None:
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
    for i in range(3):
        print(f"===== DAY {i+1:2d} =====")
        solver(f"day{i+1}")
        print()
    print(
        f"Execution of all solutions took {round((time.time() - totaltime) * 1000, 5)} ms"
    )


if __name__ == "__main__":
    solver("day4")
    # all_days()
