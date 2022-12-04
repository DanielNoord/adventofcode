import argparse
import importlib
import time
from pathlib import Path

from helpers.connect import fetch_input
from helpers.profile import Profiler


class AdventOfCodeRunner:
    """Main runner for the AOC program with various helper methods."""

    def __init__(self) -> None:
        self.args = self._parse_arguments()
        self.part1: str | None = None
        self.part2: str | None = None
        self.year: int = self.args.year
        self.day: int = self.args.day
        self.year_path = Path("solutions") / f"year{self.year}"

    def run(self) -> int:
        """Do a full run."""
        self._create_solution_file()
        data = self._get_input_files()

        # Dynamically import the module to use
        day_module = importlib.import_module(f"solutions.year{self.year}.day{self.day}")

        # Run part 1
        start_time = time.monotonic_ns()
        self.part1 = str(day_module.part1(data))
        print(
            f"🎁 Part 1: '{self.part1}' in "
            f"{(time.monotonic_ns() - start_time) / 1000:.3f}μs 🎁"
        )

        # Run part 2
        second_time = time.monotonic_ns()
        self.part2 = str(day_module.part2(data))
        done = time.monotonic_ns()
        print(
            f"🎁 Part 2: '{self.part2}' in {(done - second_time) / 1000:.3f}μs "
            f"in total {(done - start_time) / 1000:.3f}μs 🎁"
        )

        # Perform subsequent stages based on flags
        if self.args.submit:
            raise NotImplementedError()  # TODO
        if self.args.profile:
            Profiler(day_module.part1, day_module.part2, data, self.args.runs).run()
        if self.args.store:
            self._store_answers()
        if self.args.compare:
            self._compare_answers()

        return 0  # TODO: Add bitwise return values

    @staticmethod
    def _parse_arguments() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Main entry for AOC.")

        # General options
        parser.add_argument("--year", required=True, type=int, help="Year to solve")
        parser.add_argument("--day", required=True, type=int, help="Day to solve")

        parser.add_argument("--submit", action="store_true", help="Submit the solution")

        # Profiling
        parser.add_argument(
            "--profile", action="store_true", help="Profile the solution"
        )
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

    def _create_solution_file(self) -> None:
        """Create the solution file if they don't exist yet."""
        if not (self.year_path / f"day{self.day}.py").exists():
            print(f"🎅 🎅 Creating solution file for {self.year} day {self.day} 🎅 🎅")
            with open(
                self.year_path / f"day{self.day}.py", mode="w", encoding="utf-8"
            ) as file:
                file.write(
                    f"""\
from __future__ import annotations


def part1(data: str) -> str | int:
    raise NotImplementedError(
        "Part 1 not implemented for {self.year} day {self.day}. "
        "You can find it on https://adventofcode.com/{self.year}/day/{self.day}"
    )


def part2(data: str) -> str | int:
    raise NotImplementedError(
        "Part 2 not implemented for {self.year} day {self.day}"
        "You can find it on https://adventofcode.com/{self.year}/day/{self.day}"
    )
    """
                )

    def _get_input_files(self) -> str:
        """Load or fetch the input file, even if it doesn't exist yet.

        This also removes the trailing new line from the input file.
        """
        if not (self.year_path / "inputs" / f"day{self.day}.txt").exists():
            data = fetch_input(self.year, self.day)
        else:
            with open(
                self.year_path / "inputs" / f"day{self.day}.txt", encoding="utf-8"
            ) as file:
                data = file.read()
        return data[:-1]  # Remove trailing newline

    def _store_answers(self) -> None:
        """Store the answers to compare against later."""
        if not self.part1:
            print("🎅 🎅 No part 1 answer to store 🎅 🎅")
            print("🎅 🎅 Assumning there is also no part 2 🎅 🎅")
            return

        # Write part 1 to a file
        if (
            not self.args.force
            and (
                Path("solutions")
                / f"year{self.args.year}"
                / "inputs"
                / f"day{self.args.day}part1.txt"
            ).exists()
        ):
            print(
                "Input file for part1 already exists, not overwriting. "
                "Use --force to overwrite"
            )
        else:
            with open(
                Path("solutions")
                / f"year{self.args.year}"
                / "inputs"
                / f"day{self.args.day}part1.txt",
                "w",
                encoding="utf-8",
            ) as file:
                file.write(self.part1 + "\n")  # Add trailing newline
                print("🎅 🎅 Stored part 1 answer 🎅 🎅")

        if not self.part2:
            print("🎅 🎅 No part 2 answer to store 🎅 🎅")
            return

        # Write part 2 to a file
        if (
            not self.args.force
            and (
                Path("solutions")
                / f"year{self.args.year}"
                / "inputs"
                / f"day{self.args.day}part2.txt"
            ).exists()
        ):
            print(
                "Input file for part2 already exists, not overwriting. "
                "Use --force to overwrite"
            )
        else:
            with open(
                Path("solutions")
                / f"year{self.args.year}"
                / "inputs"
                / f"day{self.args.day}part2.txt",
                "w",
                encoding="utf-8",
            ) as file:
                file.write(self.part2 + "\n")  # Add trailing newline
                print("🎅 🎅 Stored part 2 answer 🎅 🎅")

    def _compare_answers(self) -> None:
        """Compare the answers against the stored answers."""
        if not self.part1:
            print("🎅 🎅 No part 1 answer to compare 🎅 🎅")
            print("🎅 🎅 Assumning there is also no part 2 🎅 🎅")
            return

        # Compare part 1
        if not (self.year_path / "inputs" / f"day{self.day}part1.txt").exists():
            print("No part 1 file found, cannot compare")
            return

        with open(
            self.year_path / "inputs" / f"day{self.day}part1.txt", encoding="utf-8"
        ) as file:
            correct_part_1 = file.read()[:-1]  # Remove trailing newline

        assert (
            self.part1 == correct_part_1
        ), f"Part 1 answer is incorrect. Expected {correct_part_1} but got {self.part1}"

        # Compare part 2
        if not self.part2:
            print("🎅 🎅 No part 2 answer to compare 🎅 🎅")
            return

        if not (self.year_path / "inputs" / f"day{self.day}part2.txt").exists():
            print("No part 2 file found, cannot compare")
            return

        with open(
            self.year_path / "inputs" / f"day{self.day}part2.txt", encoding="utf-8"
        ) as file:
            correct_part_2 = file.read()[:-1]  # Remove trailing newline
        assert (
            self.part2 == correct_part_2
        ), f"Part 2 answer is incorrect. Expected {correct_part_2} but got {self.part2}"


def main() -> int:
    return AdventOfCodeRunner().run()


if __name__ == "__main__":
    raise SystemExit(main())
