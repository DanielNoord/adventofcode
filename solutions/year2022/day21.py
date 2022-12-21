from __future__ import annotations

import operator
from collections.abc import Callable

OPERATORS: dict[str, Callable[[float, float], float]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def _parse_monkeys(data: str) -> tuple[dict[str, str], dict[str, float]]:
    special_monkeys: dict[str, str] = {}
    normal_monkeys: dict[str, float] = {}
    for unparsed_monkey in data.splitlines():
        monkey_name, data = unparsed_monkey.split(": ")
        if data[0].isnumeric():
            normal_monkeys[monkey_name] = int(data)
        else:
            special_monkeys[monkey_name] = data
    return special_monkeys, normal_monkeys


def _find_monkey(
    monkey: str, special_monkeys: dict[str, str], normal_monkeys: dict[str, float]
) -> float:
    if monkey in normal_monkeys:
        return normal_monkeys[monkey]

    monkey_one, oper, monkey_two = special_monkeys[monkey].split()

    monk_one = _find_monkey(monkey_one, special_monkeys, normal_monkeys)
    monk_two = _find_monkey(monkey_two, special_monkeys, normal_monkeys)

    value = OPERATORS[oper](monk_one, monk_two)

    normal_monkeys[monkey] = value
    return value


def _guess_integer(
    index: int,
    side_one: str,
    side_two: str,
    special_monkeys: dict[str, str],
    normal_monkeys: dict[str, float],
) -> float:
    initial = _find_monkey(
        side_one, special_monkeys, normal_monkeys.copy()
    ) - _find_monkey(side_two, special_monkeys, normal_monkeys.copy())
    step = int(f'1{"0" * (index - 1)}')
    while True:
        normal_monkeys["humn"] -= step
        value = _find_monkey(
            side_one, special_monkeys, normal_monkeys.copy()
        ) - _find_monkey(side_two, special_monkeys, normal_monkeys.copy())
        if not value:
            break
        if normal_monkeys["humn"] < step:
            return _guess_integer(
                index - 1, side_one, side_two, special_monkeys, normal_monkeys
            )
        if 1 > value > initial:
            continue
        normal_monkeys["humn"] += step
        return _guess_integer(
            index - 1, side_one, side_two, special_monkeys, normal_monkeys
        )
    return normal_monkeys["humn"]


def part1(data: str) -> str | int:
    special_monkeys, normal_monkeys = _parse_monkeys(data)
    return int(_find_monkey("root", special_monkeys, normal_monkeys))


def part2(data: str) -> str | int:
    special_monkeys, normal_monkeys = _parse_monkeys(data)

    side_one, side_two = special_monkeys["root"].split(" + ")
    one = _find_monkey(side_one, special_monkeys, normal_monkeys.copy())
    two = _find_monkey(side_two, special_monkeys, normal_monkeys.copy())

    initial_difference = one - two

    length = len(str(int(initial_difference)))
    start = int("9" * length)
    normal_monkeys["humn"] = start
    return int(
        _guess_integer(length, side_one, side_two, special_monkeys, normal_monkeys)
    )
