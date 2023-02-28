from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from functools import cache

# pylint: disable=missing-class-docstring,too-many-instance-attributes,too-many-branches


def _get_blueprints(
    data: str,
) -> dict[int, Blueprint]:
    blueprints: dict[int, Blueprint] = {}
    for index, blueprint in enumerate(data.splitlines()):
        parts = blueprint.split("costs ")
        blueprints[index + 1] = Blueprint(
            int(parts[1].split(" ")[0]),
            int(parts[2].split(" ")[0]),
            (int(parts[3].split(" ")[0]), int(parts[3].split(" ")[3])),
            (int(parts[4].split(" ")[0]), int(parts[4].split(" ")[3])),
        )
    return blueprints


@dataclass(frozen=True)
class Blueprint:
    ore: int
    clay: int
    obsidian: tuple[int, int]
    geode: tuple[int, int]

    @cache  # pylint: disable=method-cache-max-size-none
    def max_ore(self) -> int:
        return max(self.ore, self.clay, self.obsidian[0], self.geode[0])


class Action(Enum):
    START = auto()
    NOTHING = auto()
    BUILD = auto()


@dataclass(frozen=True)
class State:
    ore: int
    clay: int
    obsidian: int
    geode: int
    robots_ore: int
    robots_clay: int
    robots_obsidian: int
    robots_geode: int
    last_action: Action

    def do_round(self) -> State:
        return State(
            ore=self.ore + self.robots_ore,
            clay=self.clay + self.robots_clay,
            obsidian=self.obsidian + self.robots_obsidian,
            geode=self.geode + self.robots_geode,
            robots_ore=self.robots_ore,
            robots_clay=self.robots_clay,
            robots_obsidian=self.robots_obsidian,
            robots_geode=self.robots_geode,
            last_action=Action.NOTHING,
        )

    def buy_ore(self, blueprint: Blueprint) -> State:
        return State(
            ore=self.ore + self.robots_ore - blueprint.ore,
            clay=self.clay + self.robots_clay,
            obsidian=self.obsidian + self.robots_obsidian,
            geode=self.geode + self.robots_geode,
            robots_ore=self.robots_ore + 1,
            robots_clay=self.robots_clay,
            robots_obsidian=self.robots_obsidian,
            robots_geode=self.robots_geode,
            last_action=Action.BUILD,
        )

    def buy_clay(self, blueprint: Blueprint) -> State:
        return State(
            ore=self.ore + self.robots_ore - blueprint.clay,
            clay=self.clay + self.robots_clay,
            obsidian=self.obsidian + self.robots_obsidian,
            geode=self.geode + self.robots_geode,
            robots_ore=self.robots_ore,
            robots_clay=self.robots_clay + 1,
            robots_obsidian=self.robots_obsidian,
            robots_geode=self.robots_geode,
            last_action=Action.BUILD,
        )

    def buy_obsidian(self, blueprint: Blueprint) -> State:
        return State(
            ore=self.ore + self.robots_ore - blueprint.obsidian[0],
            clay=self.clay + self.robots_clay - blueprint.obsidian[1],
            obsidian=self.obsidian + self.robots_obsidian,
            geode=self.geode + self.robots_geode,
            robots_ore=self.robots_ore,
            robots_clay=self.robots_clay,
            robots_obsidian=self.robots_obsidian + 1,
            robots_geode=self.robots_geode,
            last_action=Action.BUILD,
        )

    def buy_geode(self, blueprint: Blueprint) -> State:
        return State(
            ore=self.ore + self.robots_ore - blueprint.geode[0],
            clay=self.clay + self.robots_clay,
            obsidian=self.obsidian + self.robots_obsidian - blueprint.geode[1],
            geode=self.geode + self.robots_geode,
            robots_ore=self.robots_ore,
            robots_clay=self.robots_clay,
            robots_obsidian=self.robots_obsidian,
            robots_geode=self.robots_geode + 1,
            last_action=Action.BUILD,
        )


@cache
def _exhaust_state(blueprint: Blueprint, state: State, rounds_to_go: int) -> State:
    # In the last round we don't need to try any buying
    if rounds_to_go == 1:
        return state.do_round()

    ore_path, clay_path, obsidian_path, geode_path, wait_path = (
        None,
        None,
        None,
        None,
        None,
    )

    # This pruning is based on the writeup/comment found at
    # https://github.com/mebeim/aoc/tree/master/2022#day-19---not-enough-minerals
    # We should never consider buying a robot that was already available on the
    # previous state. This gives the biggest speed up out of all the pruning
    if (
        state.last_action is Action.NOTHING
        and state.ore - state.robots_ore >= blueprint.geode[0]
        and state.obsidian - state.robots_obsidian >= blueprint.geode[1]
    ):
        geode_path = None
    # Case: We can buy a geode
    elif state.ore >= blueprint.geode[0] and state.obsidian >= blueprint.geode[1]:
        geode_path = _exhaust_state(
            blueprint, state.buy_geode(blueprint), rounds_to_go - 1
        )
    # Case: If we can't buy a geode in round 2 we should just wait 2 times
    elif rounds_to_go == 2:
        return state.do_round().do_round()

    # Case: We didn't buy a clay robot last time while we could
    elif (
        state.last_action is Action.NOTHING
        and state.ore - state.robots_ore >= blueprint.clay
    ):
        clay_path = None
    # Case: We reached the maximum amount of clay robots we need per minute
    elif blueprint.obsidian[1] == state.robots_clay:
        clay_path = None
    # Case: We have stored enough clay for the next round till the end so we
    # don't need more robots
    elif state.clay >= blueprint.obsidian[1] * (rounds_to_go - 1):
        clay_path = None
    # Case: We can buy a clay robot
    elif state.ore >= blueprint.clay:
        clay_path = _exhaust_state(
            blueprint, state.buy_clay(blueprint), rounds_to_go - 1
        )

    # Case: We didn't buy an obsidian robot last time while we could
    if (
        state.last_action is Action.NOTHING
        and state.ore - state.robots_ore >= blueprint.obsidian[0]
        and state.clay - state.robots_clay >= blueprint.obsidian[1]
    ):
        obsidian_path = None
    # Case: We reached the maximum amount of obsidian robots we need per minute
    elif blueprint.geode[1] == state.robots_obsidian:
        obsidian_path = None
    # Case: We have stored enough obsidian for the next round till the end so
    # we don't need more robots
    elif state.obsidian >= blueprint.geode[1] * (rounds_to_go - 1):
        obsidian_path = None
    # Case: We can buy an obsidian robot
    elif state.ore >= blueprint.obsidian[0] and state.clay >= blueprint.obsidian[1]:
        obsidian_path = _exhaust_state(
            blueprint, state.buy_obsidian(blueprint), rounds_to_go - 1
        )

    # Case: We didn't buy an ore robot last time while we could
    if (
        state.last_action is Action.NOTHING
        and state.ore - state.robots_ore >= blueprint.ore
    ):
        ore_path = None
    # Case: We reached the maximum amount of ore robots we need per minute
    elif blueprint.max_ore() == state.robots_ore:
        ore_path = None
    # Case: We have stored enough ore for the next round till the end so we
    elif state.ore >= blueprint.max_ore() * (rounds_to_go - 1):
        ore_path = None
    # Case: We can buy an ore robot
    elif state.ore >= blueprint.ore:
        ore_path = _exhaust_state(blueprint, state.buy_ore(blueprint), rounds_to_go - 1)

    # Case: An important ore is below its maximum amount so waiting "might" be good
    if state.ore < blueprint.max_ore() or state.obsidian < blueprint.geode[1]:
        wait_path = _exhaust_state(blueprint, state.do_round(), rounds_to_go - 1)
    # Case: We have geode robots so waiting always makes sense
    elif state.robots_geode:
        wait_path = state
        for _ in range(rounds_to_go):
            wait_path = wait_path.do_round()

    return max(
        ore_path or state,
        clay_path or state,
        obsidian_path or state,
        geode_path or state,
        wait_path or state,
        key=lambda x: x.geode,
    )


def _find_maximum_geodes(blueprint: Blueprint, minutes: int) -> int:
    state = State(0, 0, 0, 0, 1, 0, 0, 0, Action.START)

    state = _exhaust_state(blueprint, state, minutes)
    _exhaust_state.cache_clear()

    return state.geode


def part1(data: str) -> str | int:
    blueprints = _get_blueprints(data)
    blueprints_scores = 0

    for blue_id, blueprint in blueprints.items():
        geodes = _find_maximum_geodes(blueprint, 24)
        blueprints_scores += geodes * blue_id

    return blueprints_scores


def part2(data: str) -> str | int:
    blueprints = _get_blueprints(data)

    return (
        _find_maximum_geodes(blueprints[1], 32)
        * _find_maximum_geodes(blueprints[2], 32)
        * _find_maximum_geodes(blueprints[3], 32)
    )
