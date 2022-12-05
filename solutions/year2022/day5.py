from __future__ import annotations

import re


def _get_initial_stacks(data: str) -> list[list[str]]:
    individual_stacks = data.split("\n")
    length = int(individual_stacks[-1][-2])
    stacks: list[list[str]] = [[] for _ in range(length)]

    for stack in individual_stacks[:-1]:
        for index, match in enumerate(re.findall(r"....", stack)):
            if match[1] != " ":
                stacks[index].append(match[1])
        if stack[-2] != " ":
            stacks[length - 1].append(stack[-2])
    return stacks


def part1(data: str) -> str | int:
    stacks_data, operations = data.split("\n\n")
    stacks = _get_initial_stacks(stacks_data)

    for operation in operations.split("\n"):
        _, amount, _, fro_tmp, _, to_tmp = operation.split(" ")
        fro = int(fro_tmp) - 1
        to = int(to_tmp) - 1  # pylint: disable=invalid-name
        for _ in range(int(amount)):
            stacks[to] = [stacks[fro][0]] + stacks[to]
            stacks[fro] = stacks[fro][1:]
    return "".join(s[0] for s in stacks if s[0])


def part2(data: str) -> str | int:
    stacks_data, operations = data.split("\n\n")
    stacks = _get_initial_stacks(stacks_data)

    for operation in operations.split("\n"):
        _, amount_tmp, _, fro_tmp, _, to_tmp = operation.split(" ")
        amount = int(amount_tmp)
        fro = int(fro_tmp) - 1
        to = int(to_tmp) - 1  # pylint: disable=invalid-name
        stacks[to] = stacks[fro][:amount] + stacks[to]
        stacks[fro] = stacks[fro][amount:]
    return "".join(s[0] for s in stacks if s[0])
