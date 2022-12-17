from __future__ import annotations

from typing import TypeVar

_T = TypeVar("_T")


def breadth_first_search(
    graph: dict[_T, set[_T]], start: _T, destination: _T
) -> list[_T]:
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next_vertex in graph[vertex] - set(path):
            if next_vertex == destination:
                return path + [next_vertex]
            queue.append((next_vertex, path + [next_vertex]))
    raise ValueError("No BFS path found.")
