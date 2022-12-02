from __future__ import annotations

import time
from collections.abc import Callable
from functools import partial


class Profiler:
    """Simple helper class to do some profiling/time reporting."""

    def __init__(
        self,
        day1: Callable[[str], str | int],
        day2: Callable[[str], str | int],
        data: str,
        runs: int,
    ) -> None:
        self.day1 = partial(day1, data)
        self.day2 = partial(day2, data)
        self.runs = runs

    def run(self) -> None:
        times_day1: list[int] = []
        times_day2: list[int] = []
        times_total: list[int] = []
        for _ in range(self.runs):
            start = time.monotonic_ns()
            self.day1()
            times_day1.append(time.monotonic_ns() - start)
            start_two = time.monotonic_ns()
            self.day2()
            times_day2.append(time.monotonic_ns() - start_two)
            times_total.append(time.monotonic_ns() - start)
        print(
            f"""\
Statistics after {self.runs} runs:

Part 1:
    Average: {sum(times_day1) / len(times_day1) / 1000:.3f}μs
    Min: {min(times_day1) / 1000:.3f}μs
    Max: {max(times_day1) / 1000:.3f}μs
Part 2:
    Average: {sum(times_day2) / len(times_day2) / 1000:.3f}μs
    Min: {min(times_day2) / 1000:.3f}μs
    Max: {max(times_day2) / 1000:.3f}μs
Total:
    Average: {sum(times_total) / len(times_total) / 1000:.3f}μs
    Min: {min(times_total) / 1000:.3f}μs
    Max: {max(times_total) / 1000:.3f}μs
"""
        )
