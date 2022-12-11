from __future__ import annotations


def pretty_print_list_of_coords(coords: list[tuple[int, int]]) -> None:
    """Transform a list of coordinates into a grid with filled in squares."""
    max_x = max(c[0] for c in coords)
    min_x = min(c[0] for c in coords)
    max_y = max(c[1] for c in coords)
    min_y = min(c[1] for c in coords)

    for y_coord in range(max_y, min_y - 1, -1):
        string = [
            "#" if (x, y_coord) in coords else "." for x in range(min_x, max_x + 1)
        ]
        print("".join(string))
