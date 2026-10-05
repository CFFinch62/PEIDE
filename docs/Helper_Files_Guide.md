# Building Your Own Helper Library

As you solve Project Euler problems, the same ideas keep coming back:
testing for primes, adding up digits, counting divisors, walking a grid.
The editor gives you two places to keep reusable code so you write each idea
once and then reuse it:

- **Helpers** (`helpers/`, the Helper Files tab) are Python modules of
  *functions* you import into your solutions.
- **Templates** (`templates/`, the Templates tab) are *code patterns* you
  insert into the editor and then adapt: how to load a data file, how to
  search with an early exit, how to set up a dynamic programming table.

A good rule: if you would call it, it is a helper; if you would copy it and
change it, it is a template.

## Why bother

A solution that imports its tools tells you, at a glance, how it works:

```python
from helpers.primes import prime_sieve
from helpers.digits import is_palindrome
```

Those two lines already say "sieve the primes, then test palindromes". Months
later, that is far easier to understand than fifty lines of inline code.

## Organizing helpers

Group functions by the *idea* they support, one module per idea. A layout
that works well after a hundred or so problems:

| Module | What goes in it |
|---|---|
| `primes.py` | primality tests, prime lists, factorization |
| `sieves.py` | tables of a value for every number up to n (smallest factor, totient, ...) |
| `divisors.py` | divisors, divisor sums, perfect and abundant numbers, gcd and lcm |
| `digits.py` | digit sums, palindromes, pandigitals, digit permutations |
| `sequences.py` | sum formulas, Fibonacci, triangle and other figurate numbers, chains |
| `combinatorics.py` | binomial coefficients, permutations, partitions, counting ways |
| `grids.py` | paths through grids and triangles |
| `text.py` | letter scores, words, number names |

You do not need all of these on day one. Start with the sample module,
`helpers/example.py`, and split it into modules as it grows.

## Writing a helper function

Every helper function gets a docstring with three parts:

```python
def digit_sum(n):
    """Return the sum of the decimal digits of n.

    >>> digit_sum(2 ** 15)
    26

    Problems: 16, 20
    """
    return sum(int(d) for d in str(n))
```

1. **What it returns**, in one line. This line also appears in the index.
2. **An example**: a `>>>` line, then the result it should give. This is
   documentation and a test at the same time.
3. **A `Problems:` line** listing the problems you have used it for. Leave it
   empty (`Problems:`) until you use the function in a solution.

## Importing helpers

Always import from the `helpers` package, and import the functions by name:

```python
from helpers.digits import digit_sum, is_palindrome   # correct
from digits import digit_sum                          # wrong: missing "helpers."
```

Helpers can use each other the same way (`from helpers.primes import is_prime`).

## The two helper tools

Run these from the project folder.

**Test your helpers**: runs every `>>>` example in every helper module and
reports any whose result has changed.

```bash
python -m tools.test_helpers
```

Run it after you change a helper, so a "small improvement" can't quietly
break solutions that depend on it.

**Build the index**: writes `helpers/INDEX.md`, a table of every helper
function with the problems it applies to, and every solved problem with the
helpers it uses. It also adds each solution's helper imports to the Helpers
panel, so opening a problem shows the helper files it uses. (Files you
assigned by hand in the Helpers panel are kept.)

```bash
python -m tools.build_helper_index
```

## Templates

The editor ships with ten templates. Insert one from the Templates tab, then
replace the parts the comments point out:

| Template | Use it when |
|---|---|
| Basic Problem Structure | starting any new solution |
| Check Against the Example | the problem statement works a small case you can test against |
| Load Data File | the problem comes with a data file |
| Search Upward Until Found | you want the first number that passes a test |
| Search Downward With Early Exit | you want the largest result and can stop once nothing left can beat it |
| Sieve Once, Then Scan | you need a fact (prime, divisor count, ...) about every number up to a limit |
| Dynamic Programming Table | the answer for a big case is built from answers for smaller cases |
| Backtracking Search | you build an answer one choice at a time and can rule out dead ends early |
| Memoized Recursion and Chains | the same sub-results or chain values come up again and again |
| Group By Signature | items belong together when they share a key, such as anagrams or digit permutations |

Each template runs as-is on a small example (not a Project Euler problem),
so you can use **Test Template** to see it work before adapting it. Save your
own templates from the Templates tab as you discover patterns of your own.

## A suggested routine

1. Start a problem with **Basic Problem Structure**, and note the idea in the
   docstring.
2. Write the solution. If you write something you have written before, move it
   into a helper with a docstring, an example and a `Problems:` line.
3. When it is solved, add the problem number to the `Problems:` line of each
   helper you used, then run the two tools.

## Sharing your work

Project Euler asks solvers not to publish solutions beyond the first hundred
problems. Keep your own `solutions/` and any problem-specific helpers private;
general tools such as a prime sieve are fine to share.
