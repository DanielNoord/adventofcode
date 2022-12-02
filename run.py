import argparse
import importlib
import time
from pathlib import Path

from helpers.connect import fetch_input
from helpers.profile import Profiler


def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Main entry for AOC.")

    # General options
    parser.add_argument("--year", required=True, type=int, help="Year to solve")
    parser.add_argument("--day", required=True, type=int, help="Day to solve")

    parser.add_argument("--submit", action="store_true", help="Submit the solution")

    # Profiling
    parser.add_argument("--profile", action="store_true", help="Profile the solution")
    parser.add_argument(
        "--runs", type=int, default=10, help="Number of runs to profile"
    )

    # Storing the solution locally and comparing against it
    parser.add_argument("--store", action="store_true", help="Store the solution")
    parser.add_argument(
        "--force", action="store_true", help="Force storing the solution"
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare the solution against known correct solution",
    )

    return parser.parse_args()


def main() -> int:
    args = _parse_arguments()

    year_path = Path("solutions") / f"year{args.year}"

    # Create the solution file if it doesn't exist yet
    if not (year_path / f"day{args.day}.py").exists():
        print(f"🎅 🎅 Creating solution file for {args.year} day {args.day} 🎅 🎅")
        with open(year_path / f"day{args.day}.py", mode="w", encoding="utf-8") as file:
            file.write(
                f"""\
from __future__ import annotations


def part1(data: str) -> str | int:
    raise NotImplementedError("Part 1 not implemented for {args.year} day {args.day}")


def part2(data: str) -> str | int:
    raise NotImplementedError("Part 2 not implemented for {args.year} day {args.day}")
"""
            )

    # Fetch the input file if it doesn't exist yet
    if not (year_path / "inputs" / f"day{args.day}.txt").exists():
        data = fetch_input(args.year, args.day)
    else:
        with open(
            year_path / "inputs" / f"day{args.day}.txt", encoding="utf-8"
        ) as file:
            data = file.read()
    data = data[:-1]  # Remove trailing newline

    # Dynamically import the module
    day_module = importlib.import_module(f"solutions.year{args.year}.day{args.day}")

    # Run part 1
    start_time = time.monotonic_ns()
    part_1 = day_module.part1(data)
    print(
        f"🎁 Part 1: '{part_1}' in {(time.monotonic_ns() - start_time) / 1000:.3f}μs 🎁"
    )

    # Run part 2
    second_time = time.monotonic_ns()
    part_2 = day_module.part2(data)
    done = time.monotonic_ns()
    print(
        f"🎁 Part 2: '{part_2}' in {(done - second_time) / 1000:.3f}μs "
        f"in total {(done - start_time) / 1000:.3f}μs 🎁"
    )

    if args.submit:
        raise NotImplementedError()  # TODO
    if args.profile:
        Profiler(day_module.part1, day_module.part2, data, args.runs).run()

    # Store the solution to a local file
    if args.store:
        if (
            not args.force
            and (year_path / "inputs" / f"day{args.day}solution.txt").exists()
        ):
            print(
                "Input file already exists, not overwriting. Use --force to overwrite"
            )
        else:
            with open(
                year_path / "inputs" / f"day{args.day}solution.txt",
                "w",
                encoding="utf-8",
            ) as file:
                file.write(str(part_1) + "\n" + str(part_2) + "\n")
    if args.compare:
        if not (year_path / "inputs" / f"day{args.day}solution.txt").exists():
            print("No solution file found, cannot compare")
        else:
            with open(
                year_path / "inputs" / f"day{args.day}solution.txt", encoding="utf-8"
            ) as file:
                correct_part_1, correct_part_2, _ = file.read().split("\n")
            assert (
                str(part_1) == correct_part_1
            ), f"Part 1 is incorrect, expected {correct_part_1}"
            assert (
                str(part_2) == correct_part_2
            ), f"Part 2 is incorrect, expected {correct_part_2}"

    return 0  # TODO: Add bitwise return values


if __name__ == "__main__":
    raise SystemExit(main())
