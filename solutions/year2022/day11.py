from __future__ import annotations

import operator
from collections.abc import Callable
from math import floor, prod
from typing import Literal

# pylint: disable=too-many-arguments


OPERATORS: dict[str, Callable[[int, int], int]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
}


class Monkey:
    """Monkey for monkey business."""

    def __init__(
        self,
        items: list[int],
        operation: Callable[[int, int], int],
        var: Literal["old"] | int,
        test: int,
        monkey_if_true: int,
        monkey_if_false: int,
    ) -> None:
        self.items = items
        self.operation = operation
        self.var = var
        self.test = test
        self.monkey_if_true = monkey_if_true
        self.monkey_if_false = monkey_if_false


def _do_round(
    monkeys: list[Monkey], inspections: list[int]
) -> tuple[list[Monkey], list[int]]:
    for index, monkey in enumerate(monkeys):
        for item in monkey.items:
            inspections[index] += 1
            if monkey.var == "old":
                item = monkey.operation(item, item)
            else:
                item = monkey.operation(item, monkey.var)
            item = floor(item // 3)
            if not item % monkey.test:
                new_monkey = monkey.monkey_if_true
            else:
                new_monkey = monkey.monkey_if_false
            monkeys[new_monkey].items.append(item)
        monkey.items = []
    return monkeys, inspections


def _do_round_without_divide(
    monkeys: list[Monkey], inspections: list[int], prod_of_tests: int
) -> tuple[list[Monkey], list[int]]:
    for index, monkey in enumerate(monkeys):
        for item in monkey.items:
            inspections[index] += 1
            if monkey.var == "old":
                item = monkey.operation(item, item)
            else:
                item = monkey.operation(item, monkey.var)
            if not item % monkey.test:
                new_monkey = monkey.monkey_if_true
            else:
                new_monkey = monkey.monkey_if_false
            item %= prod_of_tests
            monkeys[new_monkey].items.append(item)
        monkey.items = []
    return monkeys, inspections


def part1(data: str) -> str | int:
    monkeys: list[Monkey] = []
    for monkey in data.split("\n\n"):
        info = monkey.splitlines()
        items = [int(i) for i in info[1][18:].split(", ")]
        op_name, var = info[2][23:].split()
        if var != "old":
            var_int: Literal["old"] | int = int(var)
        else:
            var_int = "old"
        monkeys.append(
            Monkey(
                items,
                OPERATORS[op_name],
                var_int,
                int(info[3][21:]),
                int(info[4][-1]),
                int(info[5][-1]),
            )
        )

    inspections = [0 for _ in range(len(monkeys))]
    for _ in range(20):
        monkeys, inspections = _do_round(monkeys, inspections)
    inspections = sorted(inspections, reverse=True)
    return inspections[0] * inspections[1]


def part2(data: str) -> str | int:
    monkeys: list[Monkey] = []
    for monkey in data.split("\n\n"):
        info = monkey.splitlines()
        items = [int(i) for i in info[1][18:].split(", ")]
        op_name, var = info[2][23:].split()
        if var != "old":
            var_int: Literal["old"] | int = int(var)
        else:
            var_int = "old"
        monkeys.append(
            Monkey(
                items,
                OPERATORS[op_name],
                var_int,
                int(info[3][21:]),
                int(info[4][-1]),
                int(info[5][-1]),
            )
        )

    inspections = [0 for _ in range(len(monkeys))]
    for _ in range(10000):
        monkeys, inspections = _do_round_without_divide(
            monkeys, inspections, prod(m.test for m in monkeys)
        )
    inspections = sorted(inspections, reverse=True)
    return inspections[0] * inspections[1]
