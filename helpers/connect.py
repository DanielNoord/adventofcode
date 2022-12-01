from pathlib import Path

import requests

from helpers.secrets import AOC_COOKIE


def fetch_input(year: str, day: str) -> str:
    print(f"🔔 🔔 Fetching input for {year} day {day} 🔔 🔔")
    res = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        headers={"Cookie": AOC_COOKIE},
        timeout=5,
    )
    if res.status_code == 404:
        raise ValueError("This day is (probably) not yet unlocked!")
    if not res.status_code == 200:
        raise ConnectionError(f"Status code was not 200, but {res.status_code}")
    with open(
        Path("solutions") / f"year{year}" / "inputs" / f"day{day}.txt",
        mode="w",
        encoding="utf-8",
    ) as file:
        file.write(res.text)
    return res.text
