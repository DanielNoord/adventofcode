from __future__ import annotations

from itertools import count

# pylint: disable=compare-to-zero


def _convert_to_snafu(value: int) -> str:
    snafu = ""
    power = 0
    # Get the highest power of 5 that is larger than the value
    for power in count():
        if value / (5**power) > 1:
            continue
        break

    for index in range(power, -1, -1):
        index_power = 5**index
        # Get the value if all next indices are 2
        max_second = sum(5**i for i in range(index)) * 2

        if abs(value - index_power * 2) <= max_second:
            snafu += "2"
            value -= index_power * 2
        elif abs(value - index_power) <= max_second:
            snafu += "1"
            value -= index_power
        elif abs(value + (index_power * 2)) <= max_second:
            snafu += "="
            value += index_power * 2
        elif abs(value + index_power) <= max_second:
            snafu += "-"
            value += index_power
        else:
            snafu += "0"

    # Remove leading zeros
    return snafu.lstrip("0") or "0"


def part1(data: str) -> str | int:
    total_value = 0
    for line in data.splitlines():
        line_value = 0
        for index, value in enumerate(line[::-1]):
            if value == "0":
                continue

            if value == "1":
                line_value += 5**index
            elif value == "2":
                line_value += 5**index * 2
            elif value == "-":
                line_value -= 5**index
            elif value == "=":
                line_value -= 5**index * 2
            else:
                raise AssertionError(value)
        total_value += line_value
    return _convert_to_snafu(total_value)


def part2(data: str) -> str | int:
    return data
