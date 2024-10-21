from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass

from helpers.algos import breadth_first_search


@dataclass
class Path:
    """A path that stores the visited/opened valves."""

    name: str
    release_per_minute: int
    released: int
    opened: set[str]
    minutes: int


def _create_graph(data: str) -> dict[str, tuple[int, list[str]]]:
    """Create a dict with vertices: (release_per_minute, reachable_vertices)."""
    graph: dict[str, tuple[int, list[str]]] = {}
    for line in data.splitlines():
        if "valves" in line:
            valves = line.split("valves ")[1].split(", ")
        else:
            valves = [line[-2:]]
        graph[line[6:8]] = (int(line.split("=")[1].split(";")[0]), valves)
    return graph


def _calculate_routes(
    graph: dict[str, tuple[int, list[str]]]
) -> dict[str, dict[str, int]]:
    """Calculate the shortest path between all vertices that release >0 gas."""
    graph_without_weights = {k: set(v[1]) for k, v in graph.items()}
    distances: defaultdict[str, dict[str, int]] = defaultdict(dict)
    for k in graph_without_weights.keys():
        for second_key in graph_without_weights.keys():
            if k != second_key and graph[second_key][0]:
                distances[k][second_key] = len(
                    breadth_first_search(graph_without_weights, k, second_key)
                )
    return distances


def _get_best_route(
    path: Path,
    graph: dict[str, tuple[int, list[str]]],
    routes: dict[str, dict[str, int]],
) -> Path:
    """Recursively find the best paths and their release values."""
    time_till_end = 30 - path.minutes

    # One solution is too always stay
    possible_paths = [
        Path(
            path.name,
            path.release_per_minute,
            path.released + (time_till_end * path.release_per_minute),
            path.opened,
            path.minutes + time_till_end,
        )
    ]

    for route, cost in routes[path.name].items():
        if path.minutes + cost > 30 or route in path.opened:
            continue

        # Find next step and all of its subpaths
        potential_path = Path(
            route,
            path.release_per_minute + graph[route][0],
            path.released + (cost * path.release_per_minute),
            path.opened | {route},
            path.minutes + cost,
        )
        possible_paths.append(_get_best_route(potential_path, graph, routes))

    # Find best path
    maximum, best_path = 0, path
    for possible_path in possible_paths:
        if possible_path.released > maximum:
            maximum, best_path = possible_path.released, possible_path

    return best_path


def _get_all_possible_routes(
    path: Path,
    graph: dict[str, tuple[int, list[str]]],
    routes: dict[str, dict[str, int]],
) -> Iterator[Path]:
    """Recursively find all possible paths and their release values."""
    time_till_end = 26 - path.minutes

    # One solution is too always stay
    yield Path(
        path.name,
        path.release_per_minute,
        path.released + (time_till_end * path.release_per_minute),
        path.opened,
        path.minutes + time_till_end,
    )

    for route, cost in routes[path.name].items():
        if path.minutes + cost > 26 or route in path.opened:
            continue

        # Find next step and all of its subpaths
        potential_path = Path(
            route,
            path.release_per_minute + graph[route][0],
            path.released + (cost * path.release_per_minute),
            path.opened | {route},
            path.minutes + cost,
        )
        yield from _get_all_possible_routes(potential_path, graph, routes)


def part1(data: str) -> str | int:
    graph = _create_graph(data)
    routes = _calculate_routes(graph)
    best = _get_best_route(Path("AA", 0, 0, set(), 0), graph, routes)
    return best.released


def part2(data: str) -> str | int:
    graph = _create_graph(data)
    routes = _calculate_routes(graph)

    best_solution_for_visiting_set: defaultdict[frozenset[str], int] = defaultdict(int)
    for solution in _get_all_possible_routes(Path("AA", 0, 0, set(), 0), graph, routes):
        if (
            solution.released
            > best_solution_for_visiting_set[frozenset(solution.opened)]
        ):
            best_solution_for_visiting_set[frozenset(solution.opened)] = (
                solution.released
            )

    # This only works because for the final input there are too many vertices to visit
    # For the test input the player/elephant will stay still and thus this doesn't work
    maximum = 0
    for visit, result in best_solution_for_visiting_set.items():
        for visit2, result2 in best_solution_for_visiting_set.items():
            if not visit.intersection(visit2):
                if result + result2 > maximum:
                    maximum = result + result2

    return maximum
