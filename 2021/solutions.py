#! /usr/bin/env python3
"""Solutions to year 2021"""

import time
from typing import Optional

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
    lines = [i.split(" ") for i in input_file.split("\n")]
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
        force = int(move[1])
        coords_aim = (
            coords_aim[0] + action_aim[0] * force,
            coords_aim[1] + action_aim[1](coords_aim) * force,  # type: ignore[no-untyped-call]
            coords_aim[2] + action_aim[2] * force,
        )
    print("Multiplying the final coords gives:", coords_aim[0] * coords_aim[1])
    assert coords_aim[0] * coords_aim[1] == 1856459736


# https://adventofcode.com/2021/day/3
def day3(input_file: str) -> None:
    numbers = input_file.split("\n")

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
    inputs = input_file.split("\n\n")
    numbers = [int(i) for i in inputs[0].split(",")]

    def make_card(card: str) -> list[list[Optional[int]]]:
        """Creates a bingo card"""
        new_card: list[list[Optional[int]]] = []
        rows = card.split("\n")
        for row in rows:
            new_row: list[Optional[int]] = []
            for i in range(5):
                new_row.append(int(row[i * 3 : i * 3 + 2]))
            new_card.append(new_row)
        return new_card

    cards = [make_card(i) for i in inputs[1:]]

    def check_card_for_number(
        card: list[list[Optional[int]]], number: int
    ) -> list[list[Optional[int]]]:
        """Check card for occurence of number"""
        for index, row in enumerate(card):
            for lower_index, num in enumerate(row):
                if num == number:
                    card[index][lower_index] = None
        return card

    def check_card_for_bingo(card: list[list[Optional[int]]]) -> bool:
        """Check a card for potential bingo"""
        # pylint: disable=consider-using-any-or-all
        for row in card:
            if all(i is None for i in row):
                return True
        for index in range(len(card[0])):
            if all(i[index] is None for i in card):
                return True
        return False

    def iterate_over_numbers(
        numbers: list[int], cards: list[list[list[Optional[int]]]]
    ) -> int:
        """Iterate over all numbers and get the bingo + score"""
        for num in numbers:
            cards = [check_card_for_number(i, num) for i in cards]
            for card in cards:
                if check_card_for_bingo(card):
                    remaining = sum(sum(i for i in row if i) for row in card)
                    return num * remaining
        return 0

    answer_one = iterate_over_numbers(numbers, cards)
    print("The sum of remaining numbers times last number is:", answer_one)
    assert answer_one == 89001

    def iterate_over_numbers_with_removal(
        numbers: list[int], cards: list[list[list[Optional[int]]]]
    ) -> int:
        """Iterate over the numbers but remove all winning cards until one is left"""
        for num in numbers:
            cards = [check_card_for_number(i, num) for i in cards]
            if len(cards) == 1:
                if check_card_for_bingo(cards[0]):
                    return num * sum(sum(i for i in row if i) for row in cards[0])
            else:
                cards = [card for card in cards if not check_card_for_bingo(card)]
        return 0

    answer_two = iterate_over_numbers_with_removal(numbers, cards)
    print(
        "The sum of remaning numbers times last number of last winning card is:",
        answer_two,
    )
    assert answer_two == 7296


# https://adventofcode.com/2021/day/5
def day5(input_file: str) -> None:
    lines = []
    for string in input_file.split("\n"):
        new_coords = []
        for coords in string.split(" -> "):
            new_coords.append([int(i) for i in coords.split(",")])
        lines.append(new_coords)

    map_one = [[0 for _ in range(1000)] for __ in range(1000)]
    map_two = [[0 for _ in range(1000)] for __ in range(1000)]

    for line in lines:
        x1, y1 = line[0][0], line[0][1]
        x2, y2 = line[1][0], line[1][1]
        x_step, y_step = 1, 1
        if y1 > y2:
            y_step = -1
        if x1 > x2:
            x_step = -1
        if x1 == x2:
            for index in range(y1, y2 + y_step, y_step):
                map_one[index][x1] += 1
                map_two[index][x1] += 1
        elif y1 == y2:
            for index in range(x1, x2 + x_step, x_step):
                map_one[y1][index] += 1
                map_two[y1][index] += 1
        else:
            for coords in zip(
                range(x1, x2 + x_step, x_step), range(y1, y2 + y_step, y_step)
            ):
                map_two[coords[1]][coords[0]] += 1
    overlap = sum(sum(i > 1 for i in row) for row in map_one)
    print("The amount of points with overlap is:", overlap)
    assert overlap == 5835

    overlap_two = sum(sum(i > 1 for i in row) for row in map_two)
    print("The amount of overlapping points with diagonal clouds is:", overlap_two)
    assert overlap_two == 17013


# https://adventofcode.com/2021/day/6
def day6(input_file: str) -> None:
    pass


def solver(day: str) -> None:
    """Solve one exercise"""
    start = time.time()
    with open(INPUT_FILES[day], "r", encoding="utf-8") as file:
        globals()[day](file.read().strip())
    print(
        f"Execution of solution for {day} took {round((time.time() - start) * 1000, 5)} ms"
    )


def all_days() -> None:
    """Run all days at once"""
    totaltime = time.time()
    for i in range(5):
        print(f"===== DAY {i+1:2d} =====")
        solver(f"day{i+1}")
        print()
    print(
        f"Execution of all solutions took {round((time.time() - totaltime) * 1000, 5)} ms"
    )


if __name__ == "__main__":
    solver("day6")
    # all_days()
