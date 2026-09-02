import sys
from collections import Counter
from datetime import datetime
from typing import Any

import requests


URL = "https://dmachek.github.io/meteorites-homework/meteorite_landings.json"
TIMEOUT = (5, 30)


def fetch_meteorites(
    url: str,
    timeout: int | tuple[int, int],
) -> list[dict[str, Any]]:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as error:
        raise ValueError("Invalid JSON") from error

    if not isinstance(data, list):
        raise ValueError("Expected JSON response to be a list")

    return data


# Sanity check only; not used to answer the assignment questions.
def count_present_masses(data: list[dict[str, Any]]) -> int:
    count = 0

    for meteorite in data:
        mass = meteorite.get("mass")

        if mass in (None, ""):
            continue

        count += 1

    return count


def find_largest_meteorite(
    data: list[dict[str, Any]],
) -> dict[str, Any]:
    largest_mass = None
    largest_meteorite = None

    for meteorite in data:
        mass = meteorite.get("mass")

        if mass in (None, ""):
            continue

        try:
            numeric_mass = float(mass)
        except (TypeError, ValueError):
            continue

        if largest_mass is None or numeric_mass > largest_mass:
            largest_mass = numeric_mass
            largest_meteorite = meteorite

    if largest_meteorite is None:
        raise ValueError("No valid meteorite masses found")

    return largest_meteorite


def find_most_frequent_year(
    data: list[dict[str, Any]],
) -> tuple[int, int]:
    years: Counter[int] = Counter()

    for meteorite in data:
        year = meteorite.get("year")

        if not year:
            continue

        try:
            parsed_year = datetime.fromisoformat(year).year
        except (TypeError, ValueError):
            continue

        years[parsed_year] += 1

    if not years:
        raise ValueError("No valid meteorite years found")

    return years.most_common(1)[0]


def main() -> int:
    try:
        meteorites = fetch_meteorites(URL, TIMEOUT)

        print(f"Number of entries: {len(meteorites)}")

        largest = find_largest_meteorite(meteorites)
        print(
            f"Most massive meteorite: {largest['name']} "
            f"({float(largest['mass']):,.0f} g)"
        )

        year, count = find_most_frequent_year(meteorites)
        print(
            f"Most frequent year: {year} "
            f"({count} entries)"
        )

        return 0

    except (requests.RequestException, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())