"""
Update problems/difficulty.json from a saved copy of Project Euler's progress page.

Project Euler only shows difficulty ratings to signed-in members, so they
can't be downloaded directly. Instead:

  1. Sign in at https://projecteuler.net and open https://projecteuler.net/progress
  2. Save the page (Ctrl+S, "Webpage, HTML only"), e.g. as ~/Downloads/progress.html
  3. From the project folder run:
         python -m tools.import_difficulty ~/Downloads/progress.html

Each problem's tooltip on that page reads "Difficulty: Level L [P%]". The
percentage is stored as-is and turned into 1-5 stars in even 20% bands:
1-20% = 1, 21-40% = 2, 41-60% = 3, 61-80% = 4, 81-100% = 5.
Problems the page does not rate yet keep whatever difficulty.json has.
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

DIFFICULTY_FILE = Path(__file__).resolve().parent.parent / "problems" / "difficulty.json"
# One problem's link up to its rating, never running on into the next problem's cell
TOOLTIP = re.compile(r'href="problem=(\d+)">(?:(?!href="problem=).)*?Difficulty: Level \d+ \[(\d+)%\]',
                     re.DOTALL)


def stars(percentage):
    """Return the 1-5 star rating for a Project Euler difficulty percentage."""
    return min(5, max(1, (percentage + 19) // 20))


def read_ratings(page_path):
    """Return {problem: percentage} from a saved progress page."""
    html = Path(page_path).read_text(encoding="utf-8")
    ratings = {}
    for number, percentage in TOOLTIP.findall(html):
        number, percentage = int(number), int(percentage)
        if ratings.get(number, percentage) != percentage:
            raise ValueError(f"problem {number} is listed with two different ratings")
        ratings[number] = percentage
    return ratings


def main():
    parser = argparse.ArgumentParser(description="Update problems/difficulty.json from a saved progress page.")
    parser.add_argument("page", help="the saved https://projecteuler.net/progress page")
    args = parser.parse_args()

    ratings = read_ratings(args.page)
    if not ratings:
        print("No difficulty ratings found. Was the page saved while signed in?")
        return 1

    try:
        data = json.loads(DIFFICULTY_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    data.setdefault("ratings", {})
    data.setdefault("percentages", {})

    changed = 0
    for number, percentage in ratings.items():
        key = str(number)
        if data["percentages"].get(key) != percentage or data["ratings"].get(key) != stars(percentage):
            changed += 1
        data["percentages"][key] = percentage
        data["ratings"][key] = stars(percentage)
    for section in ("ratings", "percentages"):
        data[section] = dict(sorted(data[section].items(), key=lambda item: int(item[0])))
    data["last_updated"] = datetime.now().isoformat(timespec="seconds")
    data["source"] = "projecteuler.net/progress"

    DIFFICULTY_FILE.write_text(json.dumps(data, indent=4) + "\n", encoding="utf-8")
    print(f"Read ratings for {len(ratings)} problems ({min(ratings)}-{max(ratings)}); "
          f"{changed} changed. Wrote {DIFFICULTY_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
