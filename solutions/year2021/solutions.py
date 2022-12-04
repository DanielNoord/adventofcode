#! /usr/bin/env python3
"""Solutions to year 2021."""

import itertools
import math
import time

INPUT_FILES = {f"day{i+1}": f"2021/inputs/input{i+1}.txt" for i in range(25)}


# https://adventofcode.com/2021/day/4
def day4(input_file: str) -> None:
    inputs = input_file.split("\n\n")
    numbers = [int(i) for i in inputs[0].split(",")]

    def make_card(card: str) -> list[list[int | None]]:
        """Creates a bingo card."""
        new_card: list[list[int | None]] = []
        rows = card.split("\n")
        for row in rows:
            new_row: list[int | None] = []
            for i in range(5):
                new_row.append(int(row[i * 3 : i * 3 + 2]))
            new_card.append(new_row)
        return new_card

    cards = [make_card(i) for i in inputs[1:]]

    def check_card_for_number(
        card: list[list[int | None]], number: int
    ) -> list[list[int | None]]:
        """Check card for occurence of number."""
        for index, row in enumerate(card):
            for lower_index, num in enumerate(row):
                if num == number:
                    card[index][lower_index] = None
        return card

    def check_card_for_bingo(card: list[list[int | None]]) -> bool:
        """Check a card for potential bingo."""
        # pylint: disable=consider-using-any-or-all
        for row in card:
            if all(i is None for i in row):
                return True
        for index in range(len(card[0])):
            if all(i[index] is None for i in card):
                return True
        return False

    def iterate_over_numbers(
        numbers: list[int], cards: list[list[list[int | None]]]
    ) -> int:
        """Iterate over all numbers and get the bingo + score."""
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
        numbers: list[int], cards: list[list[list[int | None]]]
    ) -> int:
        """Iterate over the numbers but remove all winning cards until one is left."""
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
def day5(input_file: str) -> None:  # pylint: disable=too-many-locals
    lines = []
    for string in input_file.split("\n"):
        new_coords = []
        for coords_str in string.split(" -> "):
            new_coords.append([int(i) for i in coords_str.split(",")])
        lines.append(new_coords)

    map_one = [[0 for _ in range(1000)] for __ in range(1000)]
    map_two = [[0 for _ in range(1000)] for __ in range(1000)]

    for line in lines:
        # pylint: disable=invalid-name
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


# https://adventofcode.com/2021/day/8
def day8(input_file: str) -> None:
    displays = [i.split(" | ") for i in input_file.split("\n")]

    count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 0: 0}
    total = 0

    for numbers, output in displays:
        nums = sorted([set(i) for i in numbers.split(" ")], key=len)
        num_mapping: dict[int, set[str]] = {
            1: nums[0],
            2: set(),
            3: set(),
            4: nums[2],
            5: set(),
            6: set(),
            7: nums[1],
            8: nums[9],
            9: set(),
            0: set(),
        }

        # Find 0, 6, 9
        for i in (nums[6], nums[7], nums[8]):
            if len(i - num_mapping[4]) == 2:
                num_mapping[9] = i
                letter_e = nums[9] - i
            elif len(i - num_mapping[1]) == 4:
                num_mapping[0] = i
            else:
                num_mapping[6] = i

        # Find 2, 3, 5
        for i in (nums[3], nums[4], nums[5]):
            if len(i - num_mapping[1]) == 3:
                num_mapping[3] = i
            elif next(iter(letter_e)) in i:
                num_mapping[2] = i
            else:
                num_mapping[5] = i

        # Iterate over display numbers
        sub_total = ""
        for output_number in output.split(" "):
            for key, num_set in num_mapping.items():
                if set(output_number) == num_set:
                    count[key] += 1
                    sub_total += str(key)
        total += int(sub_total)

    print("The numbers 1, 4, 7 and 8 occur:", count[1] + count[4] + count[7] + count[8])
    assert count[1] + count[4] + count[7] + count[8] == 534

    print("The total count of numbers is:", total)
    assert total == 1070188


# https://adventofcode.com/2021/day/9
def day9(input_file: str) -> None:
    height_map = [[int(i) for i in j] for j in input_file.split("\n")]
    y_len = len(height_map) - 1
    x_len = len(height_map[0]) - 1
    positions: dict[tuple[int, int], int] = {}

    def iterate_x_row(x_coord: int, y_coord: int, position: int) -> bool:
        """Iterate over all adjecent positions of position to find low point."""
        # pylint: disable=undefined-loop-variable
        if x_coord > 0 and row[x_coord - 1] <= position:
            return False
        if x_coord < x_len and row[x_coord + 1] <= position:
            return False
        if y_coord > 0 and height_map[y_coord - 1][x_coord] <= position:
            return False
        if y_coord < y_len and height_map[y_coord + 1][x_coord] <= position:
            return False
        return True

    for y_coord, row in enumerate(height_map):
        for x_coord, position in enumerate(row):
            if iterate_x_row(x_coord, y_coord, position):
                positions[(y_coord, x_coord)] = position
    print("Sum of all risk levels is:", sum(positions.values()) + len(positions))
    assert sum(positions.values()) + len(positions) == 506

    def iterate_basin(
        x_coord: int,
        y_coord: int,
        depth: int,
        visited: set[tuple[int, int]],
    ) -> int:
        """Iterate over adjecent positions to find basin."""
        size = 1
        visited.add((x_coord, y_coord))
        if x_coord > 0 and (x_coord - 1, y_coord) not in visited:
            if (pos := height_map[y_coord][x_coord - 1]) > depth and pos != 9:
                size += iterate_basin(x_coord - 1, y_coord, pos, visited)
        if x_coord < x_len and (x_coord + 1, y_coord) not in visited:
            if (pos := height_map[y_coord][x_coord + 1]) > depth and pos != 9:
                size += iterate_basin(x_coord + 1, y_coord, pos, visited)
        if y_coord > 0 and (x_coord, y_coord - 1) not in visited:
            if (pos := height_map[y_coord - 1][x_coord]) > depth and pos != 9:
                size += iterate_basin(x_coord, y_coord - 1, pos, visited)
        if y_coord < y_len and (x_coord, y_coord + 1) not in visited:
            if (pos := height_map[y_coord + 1][x_coord]) > depth and pos != 9:
                size += iterate_basin(x_coord, y_coord + 1, pos, visited)
        return size

    basin_sizes: dict[tuple[int, int], int] = {}
    for low_point, depth in positions.items():
        basin_sizes[low_point] = iterate_basin(low_point[1], low_point[0], depth, set())
    product_largest_basins = math.prod(sorted(basin_sizes.values())[-3:])

    print("The product of the largest basins is:", product_largest_basins)
    assert product_largest_basins == 931200


# https://adventofcode.com/2021/day/11
def day11(input_file: str) -> None:
    octopuses = [[int(i) for i in j] for j in input_file.split("\n")]
    y_len = len(octopuses) - 1
    x_len = len(octopuses[0]) - 1

    def raise_by_one(octo: list[list[int]]) -> list[list[int]]:
        """Raise all octopuses energy levels by one."""
        return [[i + 1 for i in j] for j in octo]

    def reset_to_zero(octo: list[list[int]]) -> tuple[list[list[int]], int]:
        """Resets all octopuses to zero and counts flashes."""
        flashes = 0
        for y_index, row_of_octos in enumerate(octo):
            for x_index, octopus in enumerate(row_of_octos):
                if octopus < 0:
                    octo[y_index][x_index] = 0
                    flashes += 1
        return octo, flashes

    def increase_neighbours(
        octo: list[list[int]], y_index: int, x_index: int
    ) -> list[list[int]]:
        """Increase energy levels of octopuses neighbouring a flashing one."""
        y_coords, x_coords = [0], [0]
        if y_index > 0:
            y_coords.append(-1)
        if y_index < y_len:
            y_coords.append(1)
        if x_index > 0:
            x_coords.append(-1)
        if x_index < x_len:
            x_coords.append(1)
        coords = list(itertools.product(y_coords, x_coords))

        for coord in coords:
            octo[y_index + coord[0]][x_index + coord[1]] += 1

        return octo

    def check_energy_levels(octo: list[list[int]]) -> list[list[int]]:
        """Checks energy levels of all octopuses and sees if one should flash."""
        for y_index, row_of_octos in enumerate(octo):
            for x_index, octopus in enumerate(row_of_octos):
                if octopus > 9:
                    octo[y_index][x_index] = -1000
                    octo = increase_neighbours(octo, y_index, x_index)
                    return check_energy_levels(octo)
        return octo

    def step(octo: list[list[int]]) -> tuple[list[list[int]], int]:
        """Do a step."""
        octo = raise_by_one(octo)
        octo = check_energy_levels(octo)
        return reset_to_zero(octo)

    def check_all_flashing(octo: list[list[int]]) -> bool:
        """See if all octopuses are flashing."""
        return all(all(not i for i in j) for j in octo)

    flash_count = 0
    for day in range(10000):
        octopuses, flashes = step(octopuses)
        if day < 100:
            flash_count += flashes
        if check_all_flashing(octopuses):
            all_flash_day = day + 1
            break

    print("The amount of flashes is:", flash_count)
    assert flash_count == 1755

    print("The first day all octopuses are flashing is:", all_flash_day)
    assert all_flash_day == 212


def solver(day: str) -> None:
    """Solve one exercise."""
    start = time.time()
    with open(INPUT_FILES[day], encoding="utf-8") as file:
        globals()[day](file.read().strip())
    print(
        f"Execution of solution for {day} took "
        f"{round((time.time() - start) * 1000, 5)} ms"
    )


def all_days() -> None:
    """Run all days at once."""
    totaltime = time.time()
    for i in range(12):
        print(f"===== DAY {i+1:2d} =====")
        solver(f"day{i+1}")
        print()
    print(
        "Execution of all solutions took "
        f"{round((time.time() - totaltime) * 1000, 5)} ms"
    )


if __name__ == "__main__":
    solver("day12")
    # all_days()
