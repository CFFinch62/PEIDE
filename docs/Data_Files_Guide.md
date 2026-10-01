# Project Euler Data Files

This directory contains data files required for solving certain Project Euler problems. The data files for problems 1-100 are included. Data files for later problems are added as you reach them (see below).

## Included Data Files (Problems 1-100)

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

Each method returns the data in a format suitable for solving the corresponding problem. If a file is missing, the method raises `FileNotFoundError`.

## Data Files for Problems Above 100

Data files for later problems are not included. When a problem needs one:

1. Download the file from the problem's page on https://projecteuler.net.
2. In the editor, open the problem, go to the **Data Files** tab and click **Add Data File...**, then choose the downloaded file.

The file is copied into the `data` folder with the problem number at the front of its name (e.g. `0102_triangles.txt`), which is how the editor matches it to the problem. If the problem already has a data file, the button reads **Replace Data File...**.

Files saved directly into the `data` folder are also recognised if their name starts with the problem number, as Project Euler's downloads do (`0102_triangles.txt`, or `p102_triangles.txt` for older downloads). Restart the editor after adding a file this way.

Load the file in your solution with:

```python
lines = problem_manager.load_data(102)
```

`load_data` returns the file as a list of strings, one per line; parse each line as the problem requires. The **Insert Data Loading Code** button on the Data Files tab inserts this line for you.

## Replacing a Missing File for Problems 1-100

Download the file from the problem's page on https://projecteuler.net and save it in the `data` folder with the exact name listed above.
