from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

# pylint: disable=confusing-consecutive-elif, too-many-nested-blocks
# pylint: disable=missing-class-docstring

TOTAL_SIZE = 70_000_000
NEEDED = 30_000_000


@dataclass
class File:
    name: str
    size: int


class Directory:
    def __init__(self, name: str, parent: Directory | None) -> None:
        self.name = name
        self.parent = parent
        self.children: list[Directory] = []
        self.files: list[File] = []

    @cached_property
    def size(self) -> int:
        return sum(file.size for file in self.files) + sum(
            child.size for child in self.children
        )


def _check_size(pointer: Directory) -> int:
    total_size = 0
    if (size := pointer.size) <= 100000:
        total_size += size
    for child in pointer.children:
        total_size += _check_size(child)
    return total_size


def _create_file_structure(data: str) -> Directory:
    root = Directory(".", None)
    pointer = root

    for line in data.splitlines():
        if line.startswith("$"):
            # cd command
            if line[2] == "c":
                if line[-1] == ".":
                    assert pointer.parent
                    pointer = pointer.parent
                else:
                    for child in pointer.children:
                        if child.name == line[5:]:
                            pointer = child
                            break
        elif line[:3] == "dir":
            pointer.children.append(Directory(line[4:], pointer))
        else:
            size, name = line.split()
            pointer.files.append(File(name, int(size)))
    return root


def _find_matches(pointer: Directory, to_get: int) -> int | float:
    best_size: int | float = float("inf")
    for child in pointer.children:
        if (size := child.size) >= to_get:
            if (best_child := _find_matches(child, to_get)) < best_size:
                best_size = best_child
            elif size < best_size:
                best_size = size
    return best_size


def part1(data: str) -> str | int:
    root = _create_file_structure(data)
    sum_of_small_directories = _check_size(root)
    return sum_of_small_directories


def part2(data: str) -> str | int:
    root = _create_file_structure(data)
    to_get = NEEDED - TOTAL_SIZE + root.size

    return int(_find_matches(root, to_get))
