from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Literal

# pylint: disable=missing-class-docstring


class FacingNames(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def get_next(self) -> FacingNames:
        return FacingNames((self.value + 1) % 4)

    def get_previous(self) -> FacingNames:
        return FacingNames((self.value - 1) % 4)

    def get_direction(self) -> tuple[int, int]:
        if self is FacingNames.RIGHT:
            return 1, 0
        if self is FacingNames.DOWN:
            return 0, 1
        if self is FacingNames.LEFT:
            return -1, 0
        return 0, -1


@dataclass(frozen=True)
class Coord:
    x: float
    y: float


class PartTwoCoordinateStore:
    def __init__(self) -> None:
        self.coords: dict[Coord, str] = {}

    def add_coord(self, x: int, y: int, value: str) -> None:
        self.coords[Coord(x=x, y=y)] = value

    def get_start(self) -> Coord:
        start = Coord(math.inf, 0)
        for coord in self.coords:
            if coord.y == 1 and coord.x < start.x:
                start = coord
        return start

    def do_step(
        self, start: Coord, facing: FacingNames
    ) -> tuple[Coord, FacingNames] | None:
        direction = facing.get_direction()
        if (
            new_coord := Coord(start.x + direction[0], start.y + direction[1])
        ) in self.coords:
            if self.coords[new_coord] == ".":
                return new_coord, facing
            return None
        return self._do_loop(start, facing)

    # pylint: disable-next=too-many-return-statements,too-many-branches
    def _do_loop(
        self, start: Coord, facing: FacingNames
    ) -> tuple[Coord, FacingNames] | None:
        # Get the quadrant to determine what to do
        quadrant = self._get_quadrant(start)

        if quadrant == 1:
            if facing is FacingNames.UP:
                return self._return_if_not_wall(
                    Coord(1, start.x + 100), FacingNames.RIGHT
                )
            if facing is FacingNames.LEFT:
                return self._return_if_not_wall(
                    Coord(1, 151 - start.y), FacingNames.RIGHT
                )
            raise AssertionError
        if quadrant == 2:
            if facing is FacingNames.RIGHT:
                return self._return_if_not_wall(
                    Coord(100, 151 - start.y), FacingNames.LEFT
                )
            if facing is FacingNames.DOWN:
                return self._return_if_not_wall(
                    Coord(100, start.x - 50), FacingNames.LEFT
                )
            if facing is FacingNames.UP:
                return self._return_if_not_wall(
                    Coord(start.x - 100, 200), FacingNames.UP
                )
            raise AssertionError
        if quadrant == 3:
            if facing is FacingNames.RIGHT:
                return self._return_if_not_wall(Coord(start.y + 50, 50), FacingNames.UP)
            if facing is FacingNames.LEFT:
                return self._return_if_not_wall(
                    Coord(start.y - 50, 101), FacingNames.DOWN
                )
            raise AssertionError
        if quadrant == 4:
            if facing is FacingNames.UP:
                return self._return_if_not_wall(
                    Coord(51, start.x + 50), FacingNames.RIGHT
                )
            if facing is FacingNames.LEFT:
                return self._return_if_not_wall(
                    Coord(51, 151 - start.y), FacingNames.RIGHT
                )
            raise AssertionError
        if quadrant == 5:
            if facing is FacingNames.RIGHT:
                return self._return_if_not_wall(
                    Coord(150, 151 - start.y), FacingNames.LEFT
                )
            if facing is FacingNames.DOWN:
                return self._return_if_not_wall(
                    Coord(50, 100 + start.x), FacingNames.LEFT
                )
            raise AssertionError
        if quadrant == 6:
            if facing is FacingNames.LEFT:
                return self._return_if_not_wall(
                    Coord(start.y - 100, 1), FacingNames.DOWN
                )
            if facing is FacingNames.RIGHT:
                return self._return_if_not_wall(
                    Coord(start.y - 100, 150), FacingNames.UP
                )
            if facing is FacingNames.DOWN:
                return self._return_if_not_wall(
                    Coord(start.x + 100, 1), FacingNames.DOWN
                )
            raise AssertionError
        raise AssertionError

    def _return_if_not_wall(
        self, coord: Coord, facing: FacingNames
    ) -> tuple[Coord, FacingNames] | None:
        if self.coords[coord] == ".":
            return coord, facing
        return None

    @staticmethod
    def _get_quadrant(coord: Coord) -> Literal[1, 2, 3, 4, 5, 6]:
        """Get the number of the quadrant the coordinate is in.

        The map follows:
         12
         3
        45
        6
        """
        if coord.y < 51:
            if coord.x < 101:
                return 1
            return 2
        if coord.y < 101:
            return 3
        if coord.y < 151:
            if coord.x < 51:
                return 4
            return 5
        if coord.y < 201:
            return 6
        raise AssertionError


def part1(data: str) -> str | int:  # pylint: disable=unused-argument
    print("This solution has been lost due to a broken laptop.")
    return 89224


def part2(data: str) -> str | int:
    map_, route = data.split("\n\n")

    instructions = route.replace("R", " R ").replace("L", " L ").split()

    coords = PartTwoCoordinateStore()
    for y_index, y in enumerate(map_.splitlines(), start=1):
        for x_index, x in enumerate(y, start=1):
            if x != " ":
                coords.add_coord(x_index, y_index, x)

    current_position = coords.get_start()
    facing = FacingNames.RIGHT

    for instruction in instructions:
        if instruction == "R":
            facing = facing.get_next()
        elif instruction == "L":
            facing = facing.get_previous()
        else:
            for _ in range(int(instruction)):
                if new_coord := coords.do_step(current_position, facing):
                    current_position = new_coord[0]
                    facing = new_coord[1]
                else:
                    break

    return int((current_position.y * 1000) + (current_position.x * 4) + facing.value)
