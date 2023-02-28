from __future__ import annotations

from collections.abc import Iterable


def pretty_print_iterable_of_coords(
    coords: Iterable[tuple[int, int]], reverse: bool = False
) -> None:
    """Transform an iterable of coordinates into a grid with filled in squares."""
    max_x = max(c[0] for c in coords)
    min_x = min(c[0] for c in coords)
    max_y = max(c[1] for c in coords)
    min_y = min(c[1] for c in coords)

    strings: list[str] = []
    for y_coord in range(max_y, min_y - 1, -1):
        string = [
            "#" if (x, y_coord) in coords else "." for x in range(min_x, max_x + 1)
        ]
        strings.append("".join(string))

    if reverse:
        strings.reverse()

    print("\n".join(strings))


def pretty_print_dict_of_coords(
    coords: dict[tuple[int, int], str], reverse: bool = False, filler: str = " "
) -> None:
    """Transform a dictionary of coordinates into a grid with the filler."""
    max_x = max(c[0] for c in coords.keys())
    min_x = min(c[0] for c in coords.keys())
    max_y = max(c[1] for c in coords.keys())
    min_y = min(c[1] for c in coords.keys())

    strings: list[str] = []
    for y_coord in range(max_y, min_y - 1, -1):
        string = [coords.get((x, y_coord), filler) for x in range(min_x, max_x + 1)]
        strings.append("".join(string))

    if reverse:
        strings.reverse()

    print("\n".join(strings))
