# Project Euler Helper Files

This document provides an overview of all helper files available in the `helpers` directory. These files contain utility functions that can be used across multiple Project Euler problems.

## Import Guidelines

When using helper functions, it's important to import them correctly. Here are some guidelines:

1. Always import from the `helpers` package:
   ```python
   # Correct
   from helpers.number_theory import gpf
   from helpers.primes import is_prime
   
   # Incorrect
   from number_theory import gpf  # Missing 'helpers' package
   ```

2. Import functions directly, not as modules:
   ```python
   # Correct
   from helpers.number_theory import gpf
   result = gpf(number)  # Use the function directly
   
   # Incorrect
   from helpers.number_theory import gpf
   result = gpf.gpf(number)  # Don't treat the function as a module
   ```

3. If you need multiple functions from the same module:
   ```python
   # Correct
   from helpers.number_theory import gpf, is_perfect, is_abundant
   
   # Also correct
   from helpers import number_theory
   result = number_theory.gpf(number)
   ```

## Number Theory Functions (`number_theory.py`)

Functions for number theory operations and number classification:

- `gpf(n)`: Returns the greatest prime factor of a number n
- `all_factors(n)`: Returns all factors of a number n
- `proper_factors(n)`: Returns all proper factors of n (excluding 1 and n)
- `proper_divisors(n)`: Returns all proper divisors of n (excluding n itself)
- `is_perfect(n)`: Checks if a number is perfect (sum of proper divisors equals the number)
- `is_abundant(n)`: Checks if a number is abundant (sum of proper divisors exceeds the number)
- `is_deficient(n)`: Checks if a number is deficient (sum of proper divisors is less than the number)
- `is_triangular(n)`: Checks if a number is triangular
- `is_pentagonal(n)`: Checks if a number is pentagonal
- `is_hexagonal(n)`: Checks if a number is hexagonal
- `is_pandigital(n, b, z)`: Checks if a number is pandigital in a given base

## String Utilities (`string_utils.py`)

Functions for string manipulation and text processing:

- `is_palindrome(s)`: Checks if a string is a palindrome
- `ltr_to_int(ltr)`: Converts a letter to its position in the alphabet (A=1, B=2, etc.)
- `int_to_ltr(num)`: Converts a number to its corresponding letter in the alphabet (1=A, 2=B, etc.)
- `word_score(w)`: Calculates the score of a word by summing the positions of its letters

## Cipher Functions (`ciphers.py`)

Functions for encryption and decryption:

- `caesar_cipher_decoder(message, offset)`: Decodes a message using the Caesar cipher
- `caesar_cipher_encoder(message, offset)`: Encodes a message using the Caesar cipher
- `vigenere_cipher_decoder(message, key)`: Decodes a message using the Vigenère cipher
- `vigenere_cipher_encoder(message, key)`: Encodes a message using the Vigenère cipher

## Array Utilities (`array_utils.py`)

Functions for array manipulation and sorting:

- `bubble_sort(arr, d=True)`: Sorts an array using bubble sort algorithm
- `get_2D_row(r, a)`: Gets a specific row from a 2D array
- `get_2D_col(c, a)`: Gets a specific column from a 2D array

## Number Conversion (`number_conversion.py`)

Functions for number conversion and binary operations:

- `decimalToBinary(n)`: Converts a decimal number to binary
- `genRandomBinaryString(n)`: Generates a random binary string of length n
- `sum_digits(n)`: Calculates the sum of digits in a number

## Sequence Functions (`sequences.py`)

Functions for generating and analyzing number sequences:

- `collatz_chain(n)`: Generates the Collatz chain for a number n
- `is_lychrel(n)`: Checks if a number is a Lychrel number
- `is_curzon(num)`: Checks if a number is a Curzon number

## Mathematical Utilities (`math_utils.py`)

General mathematical utility functions:

- `choose(r, d)`: Calculates the binomial coefficient (r choose d)
- `create_integer_set(start, limit)`: Creates a set containing integers from start up to the given limit (inclusive)
- `find_abundant_numbers(limit)`: Finds all abundant numbers up to a given limit
- `pairwise_sums(numbers)`: Generates all possible sums of combinations of 2 numbers from a list
- `is_square(x)`: Checks if a number is a perfect square
- `is_odd(n)`: Checks if a number is odd
- `progress_bar(progress, total)`: Displays a progress bar

## Usage Example

To use these helper functions in your Project Euler solutions:

```python
from helpers.number_theory import is_prime
from helpers.string_utils import is_palindrome
from helpers.math_utils import is_square

# Example usage
if is_prime(17):
    print("17 is prime")

if is_palindrome("racecar"):
    print("racecar is a palindrome")

if is_square(16):
    print("16 is a perfect square")
```

## Notes

- All functions include detailed docstrings explaining their purpose, arguments, and return values
- Functions are organized by category for easy reference
- Some functions may have dependencies on others within their category
- Most functions are optimized for performance and readability 