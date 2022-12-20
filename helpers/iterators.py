from collections.abc import Iterator


def one_dimensional_neighbours(
    x: int, y: int, z: int
) -> Iterator[tuple[int, int, int]]:
    yield x - 1, y, z
    yield x + 1, y, z
    yield x, y - 1, z
    yield x, y + 1, z
    yield x, y, z - 1
    yield x, y, z + 1
