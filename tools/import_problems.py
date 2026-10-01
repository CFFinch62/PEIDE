"""
Re-import problem descriptions from projecteuler.net as HTML.

Uses Project Euler's official "minimal" API:
    https://projecteuler.net/minimal=problems   list of problem ids and titles
    https://projecteuler.net/minimal=N          problem N's content as HTML

Each problem file keeps the same layout as before:

    Problem N: Title
    <blank line>
    <problem HTML exactly as shown on the website>
    <blank line>
    Hint:
    ...

The existing hint section of a file is kept unchanged. Images are downloaded
into problems/resources/images/ so problems display offline, and relative
links (data files, other problems) are made absolute so they open the website.

Usage (from the project root):
    python tools/import_problems.py                 re-import all existing problems
    python tools/import_problems.py 101 110         re-import problems 101 to 110
    python tools/import_problems.py --new           only import problems that don't have a file yet
    python tools/import_problems.py --cache DIR     keep downloaded HTML in DIR
"""

import argparse
import html
import os
import re
import sys
import time
import urllib.parse
import urllib.request

SITE = "https://projecteuler.net/"
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS_DIR = os.path.join(PROJECT_DIR, "problems")
USER_AGENT = "PE-Editor problem importer"

DEFAULT_HINTS = """Hint:
1. Break down the problem into smaller steps
2. Consider mathematical properties that might simplify the solution
3. Think about efficient algorithms to solve this type of problem"""

HINT_START = re.compile(r"^Hints?:", re.MULTILINE)
IMG_SRC = re.compile(r'(<img\b[^>]*?\bsrc=")([^"]+)(")', re.IGNORECASE)
A_HREF = re.compile(r'(<a\b[^>]*?\bhref=")([^"]+)(")', re.IGNORECASE)


class Fetcher:
    """Downloads from the website, waiting between requests to be polite."""

    def __init__(self, delay, cache_dir=None):
        self.delay = delay
        self.cache_dir = cache_dir
        self.last_request = 0.0

    def get(self, url):
        elapsed = time.time() - self.last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read()
        finally:
            self.last_request = time.time()

    def problem_html(self, number):
        """Return problem's HTML, from the cache if it has been downloaded before."""
        cache_file = None
        if self.cache_dir:
            cache_file = os.path.join(self.cache_dir, f"{number}.html")
            if os.path.exists(cache_file):
                with open(cache_file, encoding="utf-8") as f:
                    return f.read()

        text = self.get(f"{SITE}minimal={number}").decode("utf-8")
        if cache_file:
            os.makedirs(self.cache_dir, exist_ok=True)
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write(text)
        return text


def group_dir(problems_dir, number):
    """Folder a problem belongs in, matching ProblemManager.load_problem()."""
    start = ((number - 1) // 100) * 100 + 1
    return os.path.join(problems_dir, f"{start}-{start + 99}")


def existing_problem_files(problems_dir=PROBLEMS_DIR):
    """Map problem number -> path for every problem file in the project."""
    files = {}
    if not os.path.isdir(problems_dir):
        return files
    for dirname in os.listdir(problems_dir):
        subdir = os.path.join(problems_dir, dirname)
        if not (os.path.isdir(subdir) and re.match(r"\d+-\d+$", dirname)):
            continue
        for filename in os.listdir(subdir):
            match = re.match(r"problem_(\d+)\.txt$", filename)
            if match:
                files[int(match.group(1))] = os.path.join(subdir, filename)
    return files


def fetch_titles(fetcher):
    """Return {problem number: title} from the problem list."""
    titles = {}
    for line in fetcher.get(f"{SITE}minimal=problems").decode("utf-8").splitlines()[1:]:
        fields = line.split("##")
        if len(fields) >= 2 and fields[0].isdigit():
            titles[int(fields[0])] = html.unescape(fields[1])
    return titles


def localise(content, problems_dir, fetcher):
    """Download the problem's images and make its links absolute."""

    def fix_image(match):
        url = urllib.parse.urljoin(SITE, html.unescape(match.group(2)))
        parsed = urllib.parse.urlparse(url)
        if parsed.netloc != urllib.parse.urlparse(SITE).netloc:
            return match.group(0)  # leave images hosted elsewhere alone

        # e.g. "resources/images/0107_1.png", stored under the problems folder
        relative_path = urllib.parse.unquote(parsed.path).lstrip("/")
        local_file = os.path.join(problems_dir, *relative_path.split("/"))
        if not os.path.exists(local_file):
            os.makedirs(os.path.dirname(local_file), exist_ok=True)
            data = fetcher.get(url)
            with open(local_file, "wb") as f:
                f.write(data)
        return match.group(1) + html.escape(relative_path) + match.group(3)

    def fix_link(match):
        href = html.unescape(match.group(2))
        if href.startswith(("#", "mailto:")):
            return match.group(0)
        return match.group(1) + html.escape(urllib.parse.urljoin(SITE, href)) + match.group(3)

    content = IMG_SRC.sub(fix_image, content)
    return A_HREF.sub(fix_link, content)


def import_problem(number, title, path, problems_dir, fetcher):
    hints = DEFAULT_HINTS
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = f.read()
        match = HINT_START.search(old)
        if match:
            hints = old[match.start():].rstrip()

    content = localise(fetcher.problem_html(number).strip(), problems_dir, fetcher)
    if not content:
        raise ValueError("website returned no content")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Problem {number}: {title}\n\n{content}\n\n{hints}\n")


def import_problems(problems_dir=PROBLEMS_DIR, first=None, last=None, new=False,
                    delay=1.0, cache_dir=None, report=print):
    """Import problems from the website and return (imported, failed) lists.

    Imports every problem that already has a file, or with new=True only the
    problems that don't have one yet, limited to first..last if given.
    Progress messages are passed to report().
    """
    fetcher = Fetcher(delay, cache_dir)
    titles = fetch_titles(fetcher)
    files = existing_problem_files(problems_dir)

    numbers = set(titles) - set(files) if new else set(files)
    if first and not last:
        last = first  # a single problem
    numbers = sorted(n for n in numbers
                     if (not first or n >= first) and (not last or n <= last))
    if not numbers:
        report("No problems to import.")
        return [], []

    imported, failed = [], []
    for number in numbers:
        if number not in titles:
            report(f"Problem {number}: not on the website, skipped")
            continue
        path = files.get(number) or os.path.join(group_dir(problems_dir, number),
                                                 f"problem_{number}.txt")
        try:
            import_problem(number, titles[number], path, problems_dir, fetcher)
            imported.append(number)
            report(f"Problem {number}: {titles[number]}")
        except Exception as e:
            failed.append(number)
            report(f"Problem {number}: FAILED ({e})")
    return imported, failed


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("first", type=int, nargs="?", help="first problem to import")
    parser.add_argument("last", type=int, nargs="?", help="last problem to import")
    parser.add_argument("--new", action="store_true",
                        help="only import problems that don't have a file yet")
    parser.add_argument("--delay", type=float, default=1.0,
                        help="seconds to wait between requests (default 1)")
    parser.add_argument("--cache", help="folder to keep downloaded problem HTML in")
    args = parser.parse_args()

    imported, failed = import_problems(first=args.first, last=args.last, new=args.new,
                                       delay=args.delay, cache_dir=args.cache)
    print(f"\nImported {len(imported)} problems.")
    if failed:
        print(f"Failed: {', '.join(map(str, failed))}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
