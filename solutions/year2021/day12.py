from __future__ import annotations

from typing import ClassVar

# pylint: disable=missing-class-docstring


class Node:
    visit_small_twice: ClassVar[bool] = False

    def __init__(self, name: str) -> None:
        self.children: set[Node] = set()
        self.name = name
        self.lower_case = name.islower()

    def find_sub_path(self, visited_small_too_often: bool, cur_path: list[str]) -> int:
        subpaths = 0

        # Handle exclusion of twice visiting small nodes
        if self.lower_case:
            if visited_small_too_often and self.name in cur_path:
                return 0
            if not self.visit_small_twice or self.name in cur_path:
                visited_small_too_often = True

        for child in self.children:
            subpaths += child.find_sub_path(
                visited_small_too_often, cur_path + [self.name]
            )
        return subpaths


class EndNode(Node):
    def find_sub_path(self, visited_small_too_often: bool, cur_path: list[str]) -> int:
        return 1


class PartTwoNode(Node):
    visit_small_twice = True


def _make_connections_dict(
    paths: list[tuple[str, str]], base_node: type[Node]
) -> dict[str, Node]:
    connections: dict[str, Node] = {}
    for first, second in paths:
        if first not in connections:
            if first == "end":
                connections[first] = EndNode(first)
            else:
                connections[first] = base_node(first)
        if second not in connections:
            if second == "end":
                connections[second] = EndNode(second)
            else:
                connections[second] = base_node(second)
        if not second == "start":
            connections[first].children.add(connections[second])
        if not first == "start":
            connections[second].children.add(connections[first])
    return connections


def part1(data: str) -> str | int:
    paths = [tuple(path.split("-")) for path in data.splitlines()]
    connections = _make_connections_dict(paths, Node)  # type: ignore[arg-type]

    return connections.pop("start").find_sub_path(False, cur_path=[])


def part2(data: str) -> str | int:
    paths = [tuple(path.split("-")) for path in data.splitlines()]
    connections = _make_connections_dict(paths, PartTwoNode)  # type: ignore[arg-type]

    return connections["start"].find_sub_path(False, cur_path=[])
