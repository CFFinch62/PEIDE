"""
example.py - a sample helper module showing how to build your own library.

Group functions by the idea they support (primes, digits, divisors, ...),
one module per idea. Give every function a docstring that:
  * says what it returns,
  * shows an example as a >>> line followed by the expected result
    (python -m tools.test_helpers runs these as tests), and
  * ends with a "Problems:" line listing the problems you used it for
    (python -m tools.build_helper_index turns these into helpers/INDEX.md).

Rename, extend or delete this file as your own library grows.
"""

from math import isqrt


def is_prime(n):
    """Return True if n is prime.

    Only divisors up to sqrt(n) need checking, and after 2 and 3 every
    prime has the form 6k - 1 or 6k + 1.

    >>> is_prime(97)
    True
    >>> is_prime(1)
    False
    >>> [k for k in range(20) if is_prime(k)]
    [2, 3, 5, 7, 11, 13, 17, 19]

    Problems:
    """
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, isqrt(n) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


def digit_sum(n):
    """Return the sum of the decimal digits of n.

    >>> digit_sum(2 ** 15)
    26

    Problems:
    """
    return sum(int(d) for d in str(n))


def is_palindrome(x):
    """Return True if x reads the same forwards and backwards (number or string).

    >>> is_palindrome(9009)
    True
    >>> is_palindrome("abca")
    False

    Problems:
    """
    s = str(x)
    return s == s[::-1]
