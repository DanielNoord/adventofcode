from __future__ import annotations


def part1(data: str) -> str | int:
    marker: list[str] = []
    for index, char in enumerate(data):
        if char not in marker:
            if len(marker) == 3:
                return index + 1
            marker.append(char)
        else:
            marker = marker[marker.index(char) + 1 :] + [char]
    raise AssertionError()


def part2(data: str) -> str | int:
    marker: list[str] = []
    for index, char in enumerate(data):
        if char not in marker:
            if len(marker) == 13:
                return index + 1
            marker.append(char)
        else:
            marker = marker[marker.index(char) + 1 :] + [char]
    raise AssertionError()
