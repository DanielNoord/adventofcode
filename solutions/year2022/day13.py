from __future__ import annotations

from functools import cmp_to_key
from typing import Any

IntegerList = list["int | IntegerList"]


def _make_packet(line: str) -> list[IntegerList]:
    stack: list[IntegerList] = []

    # Replace 10's as then we don't need to split on , but can just continue
    for value in line.replace("10", "X"):
        if value == "[":
            stack.append([])
        elif value == "X":
            stack[-1].append(10)
        elif value in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
            stack[-1].append(int(value))
        elif value == "]":
            if len(stack) == 1:
                continue
            stack[-2].append(stack.pop())
    return stack


def _are_packets_in_order(pack_one: list[Any], pack_two: list[Any]) -> bool:
    for index, value in enumerate(pack_one):
        try:
            value_two = pack_two[index]
        except IndexError:
            return False

        if isinstance(value, int) and isinstance(value_two, int):
            if value == value_two:
                continue
            return value < value_two
        if isinstance(value, list) and isinstance(value_two, list):
            return _are_packets_in_order(value, value_two)
        if isinstance(value, list) and isinstance(value_two, int):
            return _are_packets_in_order(value, [value_two])
        if isinstance(value, int) and isinstance(value_two, list):
            return _are_packets_in_order([value], value_two)
    return True


def part1(data: str) -> str | int:
    indices = 0
    for index, packet in enumerate(data.split("\n\n"), start=1):
        line_one, line_two = packet.splitlines()
        if _are_packets_in_order(_make_packet(line_one), _make_packet(line_two)):
            indices += index
    return indices


def part2(data: str) -> str | int:
    packets: list[list[IntegerList]] = []
    for packet in data.replace("\n\n", "\n").splitlines():
        packets.append(_make_packet(packet))

    def compare(packet_one: list[Any], packet_two: list[Any]) -> int:
        if _are_packets_in_order(packet_one, packet_two):
            return -1
        return 1

    # Add dividers
    packets.append([[6]])
    packets.append([[2]])

    packets.sort(key=cmp_to_key(compare))
    return (packets.index([[6]]) + 1) * (packets.index([[2]]) + 1)
