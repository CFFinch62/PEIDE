# Project Euler Data Files

This directory contains data files required for solving certain Project Euler problems. All required data files are included in this directory and are automatically loaded by the application when needed.

## Available Data Files

The following data files are available and ready to use:

1. `names.txt` (Problem 22)
   - Contains over five thousand first names
   - Used for sorting and calculating name scores

2. `words.txt` (Problems 42 and 98)
   - Contains nearly 2000 common English words
   - Used for word value calculations and anagram detection

3. `poker.txt` (Problem 54)
   - Contains one thousand random hands dealt to two players
   - Used for poker hand comparison and winner determination

4. `cipher.txt` (Problem 59)
   - Contains encrypted ASCII codes
   - Used for decryption and XOR cipher analysis

5. `triangle.txt` (Problem 67)
   - Contains a triangle of numbers (100 rows)
   - Used for finding maximum path sums

6. `keylog.txt` (Problem 79)
   - Contains fifty successful login attempts
   - Used for determining the shortest possible secret passcode

7. `matrix.txt` (Problems 81, 82, and 83)
   - Contains an 80×80 matrix
   - Used for finding minimal path sums in different directions

8. `roman.txt` (Problem 89)
   - Contains one thousand numbers written in valid Roman numerals
   - Used for Roman numeral optimization

9. `sudoku.txt` (Problem 96)
   - Contains 50 Sudoku puzzles
   - Used for solving Sudoku puzzles

10. `base_exp.txt` (Problem 99)
    - Contains 1000 base/exponent pairs
    - Used for comparing large numbers

## Using the Data Files

The `ProblemManager` class provides helper methods to load these files:

```python
# Load triangle data for Problem 67
triangle = problem_manager.load_triangle_data()

# Load names for Problem 22
names = problem_manager.load_names_data()

# Load words for Problems 42 and 98
words = problem_manager.load_words_data()

# Load poker hands for Problem 54
hands = problem_manager.load_poker_data()

# Load cipher data for Problem 59
cipher = problem_manager.load_cipher_data()

# Load keylog data for Problem 79
keylog = problem_manager.load_keylog_data()

# Load matrix data for Problems 81, 82, and 83
matrix = problem_manager.load_matrix_data()

# Load Roman numerals for Problem 89
romans = problem_manager.load_roman_data()

# Load Sudoku puzzles for Problem 96
puzzles = problem_manager.load_sudoku_data()

# Load base/exponent pairs for Problem 99
pairs = problem_manager.load_base_exp_data()
```

Each method returns the data in a format suitable for solving the corresponding problem. If a file is missing, the method will return `None`.

## Obtaining Missing Files

If any data file is missing from this directory, you can obtain it by:

1. Visit the Project Euler website (https://projecteuler.net)
2. Log in to your account
3. Navigate to the specific problem page
4. Click the "Download" link next to the data file
5. Save the file in this directory with the exact name specified above

Note: All required data files should already be present in this directory. You should only need to download files if they have been accidentally deleted or corrupted. 