"""
Lesson 6: Loops - Repeating Code
================================

Loops allow you to repeat code multiple times without writing it over and over.
They're essential for processing lists, counting, and automating repetitive tasks.

Key Concepts in this lesson:
- for loops with range()
- for loops with lists and strings
- while loops
- Loop control: break and continue
- Nested loops
- Practical loop examples
"""

print("=== Introduction to Loops ===")

# Without loops, repeating code is tedious:
print("Manual repetition:")
print("Hello 1")
print("Hello 2")
print("Hello 3")
print("Hello 4")
print("Hello 5")

# With loops, it's much easier:
print("\nUsing a loop:")
for i in range(1, 6):
    print(f"Hello {i}")

print("\n=== For Loops with range() ===")

# range(stop) - counts from 0 to stop-1
print("range(5):")
for i in range(5):
    print(f"Count: {i}")

# range(start, stop) - counts from start to stop-1
print("\nrange(1, 6):")
for i in range(1, 6):
    print(f"Number: {i}")

# range(start, stop, step) - counts with custom step
print("\nrange(0, 10, 2) - even numbers:")
for i in range(0, 10, 2):
    print(f"Even: {i}")

print("\nrange(10, 0, -1) - counting backwards:")
for i in range(10, 0, -1):
    print(f"Countdown: {i}")

print("\n=== For Loops with Lists ===")

# Looping through a list
fruits = ["apple", "banana", "orange", "grape"]
print("Fruits in my basket:")
for fruit in fruits:
    print(f"- {fruit}")

# Getting both index and value with enumerate()
print("\nFruits with numbers:")
for index, fruit in enumerate(fruits):
    print(f"{index + 1}. {fruit}")

# Looping through numbers
numbers = [10, 20, 30, 40, 50]
total = 0
for number in numbers:
    total += number
    print(f"Adding {number}, total so far: {total}")
print(f"Final total: {total}")

print("\n=== For Loops with Strings ===")

# You can loop through each character in a string
word = "Python"
print(f"Letters in '{word}':")
for letter in word:
    print(f"- {letter}")

# Counting vowels in a string
sentence = "Hello World"
vowels = "aeiouAEIOU"
vowel_count = 0

print(f"\nCounting vowels in '{sentence}':")
for letter in sentence:
    if letter in vowels:
        print(f"Found vowel: {letter}")
        vowel_count += 1

print(f"Total vowels: {vowel_count}")

print("\n=== While Loops ===")

# While loops continue as long as a condition is True
print("Counting with while loop:")
count = 1
while count <= 5:
    print(f"Count: {count}")
    count += 1  # Don't forget to update the variable!

# While loop with user input simulation
print("\nGuessing game simulation:")
secret_number = 7
guess = 0
attempts = 0

while guess != secret_number:
    attempts += 1
    # Simulating different guesses
    if attempts == 1:
        guess = 5
    elif attempts == 2:
        guess = 9
    else:
        guess = 7
    
    print(f"Attempt {attempts}: Guessing {guess}")
    
    if guess < secret_number:
        print("Too low!")
    elif guess > secret_number:
        print("Too high!")
    else:
        print(f"Correct! Found it in {attempts} attempts!")

print("\n=== Loop Control: break and continue ===")

# break - exits the loop immediately
print("Using break to exit early:")
for i in range(10):
    if i == 5:
        print(f"Breaking at {i}")
        break
    print(f"Number: {i}")

# continue - skips the rest of the current iteration
print("\nUsing continue to skip even numbers:")
for i in range(10):
    if i % 2 == 0:  # If even number
        continue    # Skip the rest and go to next iteration
    print(f"Odd number: {i}")

# Practical example: finding first negative number
numbers = [5, 10, -3, 8, -1, 12]
print(f"\nFinding first negative in {numbers}:")
for number in numbers:
    if number < 0:
        print(f"First negative number found: {number}")
        break
    print(f"Checking {number} - positive")

print("\n=== Nested Loops ===")

# Loops inside loops
print("Multiplication table (3x3):")
for i in range(1, 4):
    for j in range(1, 4):
        result = i * j
        print(f"{i} x {j} = {result}")
    print()  # Empty line after each row

# Creating a pattern
print("Star pattern:")
for row in range(5):
    for col in range(row + 1):
        print("*", end="")
    print()  # New line after each row

print("\n=== Practical Examples ===")

# Example 1: Calculate factorial
number = 5
factorial = 1
print(f"Calculating factorial of {number}:")
for i in range(1, number + 1):
    factorial *= i
    print(f"{i}! = {factorial}")

# Example 2: Find maximum in a list
numbers = [23, 67, 12, 89, 45, 34]
maximum = numbers[0]  # Start with first number
print(f"\nFinding maximum in {numbers}:")
for number in numbers:
    if number > maximum:
        maximum = number
        print(f"New maximum found: {maximum}")
print(f"Final maximum: {maximum}")

# Example 3: Password validation
password = "mypassword123"
has_digit = False
has_letter = False

print(f"\nValidating password: '{password}'")
for char in password:
    if char.isdigit():
        has_digit = True
    elif char.isalpha():
        has_letter = True

if has_digit and has_letter:
    print("Password is valid (has both letters and numbers)")
else:
    print("Password is invalid (needs both letters and numbers)")

# Example 4: Shopping cart total
cart = [
    {"item": "apple", "price": 1.50, "quantity": 3},
    {"item": "bread", "price": 2.99, "quantity": 1},
    {"item": "milk", "price": 3.49, "quantity": 2}
]

total = 0
print("\nShopping cart:")
for item in cart:
    item_total = item["price"] * item["quantity"]
    total += item_total
    print(f"{item['item']}: ${item['price']:.2f} x {item['quantity']} = ${item_total:.2f}")

print(f"Total: ${total:.2f}")

print("\n=== List Comprehensions (Advanced) ===")

# List comprehensions are a compact way to create lists using loops
numbers = [1, 2, 3, 4, 5]

# Traditional way with loop
squares = []
for number in numbers:
    squares.append(number ** 2)
print(f"Squares (traditional): {squares}")

# List comprehension way
squares_comp = [number ** 2 for number in numbers]
print(f"Squares (comprehension): {squares_comp}")

# With condition
even_squares = [number ** 2 for number in numbers if number % 2 == 0]
print(f"Even squares: {even_squares}")

print("\n=== Common Loop Patterns ===")

# Pattern 1: Accumulator (building up a total)
numbers = [1, 2, 3, 4, 5]
sum_total = 0
for number in numbers:
    sum_total += number
print(f"Sum of {numbers}: {sum_total}")

# Pattern 2: Counter (counting occurrences)
text = "hello world"
letter_count = 0
for char in text:
    if char == 'l':
        letter_count += 1
print(f"Letter 'l' appears {letter_count} times in '{text}'")

# Pattern 3: Filter (collecting items that meet criteria)
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = []
for number in numbers:
    if number % 2 == 0:
        even_numbers.append(number)
print(f"Even numbers from {numbers}: {even_numbers}")

# Pattern 4: Transform (changing each item)
words = ["hello", "world", "python"]
uppercase_words = []
for word in words:
    uppercase_words.append(word.upper())
print(f"Uppercase words: {uppercase_words}")

"""
Exercise for you:
1. Number games:
   - Print all numbers from 1 to 20
   - Print only odd numbers from 1 to 15
   - Print numbers from 20 down to 1

2. String processing:
   - Count how many times each vowel appears in "programming"
   - Reverse a string using a loop
   - Check if a word is a palindrome (reads same forwards and backwards)

3. List operations:
   - Find the average of a list of test scores
   - Find both the minimum and maximum in a list
   - Count how many positive and negative numbers are in a list

4. Pattern printing:
   - Print a right triangle of stars (5 rows)
   - Print numbers in a pyramid pattern
   - Create a checkerboard pattern with X and O

5. Practical applications:
   - Calculate compound interest year by year for 5 years
   - Simulate rolling two dice 10 times and count doubles
   - Create a simple times table (1-10 x 1-10)

Bonus challenges:
- Create a prime number checker using loops
- Build a simple text-based progress bar
- Make a word frequency counter for a sentence
"""

# Your practice space - add your code below: 