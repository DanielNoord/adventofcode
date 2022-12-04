from __future__ import annotations


def _get_bit(numbers: list[str], index: int, middle: float, most_common: bool) -> str:
    """Get the most or least common bit for a given index."""
    if sum(number[index] == "1" for number in numbers) >= middle:
        return "1" if most_common else "0"
    return "0" if most_common else "1"


def part1(data: str) -> str | int:
    numbers = data.splitlines()

    most_common_bits = ""
    middle = len(numbers) // 2
    for index in range(len(numbers[0])):
        most_common_bits += _get_bit(numbers, index, middle, True)
    gamma = int("".join(most_common_bits), 2)
    epsilon = int("".join("0" if i == "1" else "1" for i in most_common_bits), 2)
    return gamma * epsilon


def part2(data: str) -> str | int:
    oxy_numbers = data.splitlines()
    bit_pattern, index = "", 0
    while len(oxy_numbers) > 1:
        bit_pattern += _get_bit(oxy_numbers, index, len(oxy_numbers) / 2, True)
        oxy_numbers = [i for i in oxy_numbers if i.startswith(bit_pattern)]
        index += 1

    co2_numbers = data.splitlines()
    bit_pattern, index = "", 0
    while len(co2_numbers) > 1:
        bit_pattern += _get_bit(co2_numbers, index, len(co2_numbers) / 2, False)
        co2_numbers = [i for i in co2_numbers if i.startswith(bit_pattern)]
        index += 1
    return int(oxy_numbers[0], 2) * int(co2_numbers[0], 2)
