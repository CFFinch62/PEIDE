"""
Run the examples in every helper module's docstrings as tests.

Any docstring line starting with >>> is run, and its output must match the
line below it:

    >>> digit_sum(2 ** 15)
    26

Run from the project root:
    python -m tools.test_helpers
"""

import doctest
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HELPERS = ROOT / "helpers"


def main():
    sys.path.insert(0, str(ROOT))
    modules = sorted(p.stem for p in HELPERS.glob("*.py") if not p.stem.startswith("_"))
    if not modules:
        print("No helper modules found in helpers/")
        return 0

    failed_total = tried_total = 0
    for name in modules:
        try:
            module = importlib.import_module(f"helpers.{name}")
        except Exception as e:
            print(f"ERROR  helpers/{name}.py could not be imported: {type(e).__name__}: {e}")
            failed_total += 1
            continue
        failed, tried = doctest.testmod(module, optionflags=doctest.ELLIPSIS)
        failed_total += failed
        tried_total += tried
        status = "ok   " if failed == 0 else "FAIL "
        note = "no examples yet" if tried == 0 else f"{tried - failed} of {tried} examples passed"
        print(f"{status} helpers/{name}.py: {note}")

    print(f"\n{tried_total - failed_total} of {tried_total} examples passed" if tried_total
          else "\nNo examples found. Add >>> lines to your docstrings.")
    return 1 if failed_total else 0


if __name__ == "__main__":
    sys.exit(main())
