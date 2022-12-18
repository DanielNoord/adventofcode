from __future__ import annotations


def _count_faces(x: int, y: int, z: int, droplets: set[tuple[int, int, int]]) -> int:
    faces = 0
    if (x - 1, y, z) not in droplets:
        faces += 1
    if (x + 1, y, z) not in droplets:
        faces += 1
    if (x, y - 1, z) not in droplets:
        faces += 1
    if (x, y + 1, z) not in droplets:
        faces += 1
    if (x, y, z - 1) not in droplets:
        faces += 1
    if (x, y, z + 1) not in droplets:
        faces += 1
    return faces


def part1(data: str) -> str | int:
    seen_droplets: set[tuple[int, int, int]] = set()
    exposed_faces = 0
    for droplet in data.splitlines():
        seen_droplets.add(tuple(map(int, droplet.split(","))))  # type: ignore[arg-type]
    for parsed_droplet in seen_droplets:
        exposed_faces += _count_faces(*parsed_droplet, seen_droplets)
    return exposed_faces


def part2(data: str) -> str | int:
    return len(data)
