"""
Lesson 4: Numbers and Mathematical Operations
============================================

Numbers are fundamental in programming. Python makes it easy to work with
different types of numbers and perform mathematical calculations.

Key Concepts in this lesson:
- Integer and float numbers
- Basic mathematical operations
- Order of operations
- Assignment operators
- Built-in math functions
- Working with the math module
"""

print("=== Types of Numbers ===")

# Integers (whole numbers)
age = 16
year = 2024
temperature = -5

print("Integers:")
print(f"Age: {age}")
print(f"Year: {year}")
print(f"Temperature: {temperature}")

# Floats (decimal numbers)
height = 5.75
pi = 3.14159
price = 19.99

print("\nFloats:")
print(f"Height: {height}")
print(f"Pi: {pi}")
print(f"Price: {price}")

# You can check the type of a number
print(f"\nType of age: {type(age)}")
print(f"Type of height: {type(height)}")

print("\n=== Basic Mathematical Operations ===")

a = 10
b = 3

print(f"a = {a}, b = {b}")
print(f"Addition: {a} + {b} = {a + b}")
print(f"Subtraction: {a} - {b} = {a - b}")
print(f"Multiplication: {a} * {b} = {a * b}")
print(f"Division: {a} / {b} = {a / b}")
print(f"Floor division: {a} // {b} = {a // b}")  # Rounds down to nearest integer
print(f"Modulus (remainder): {a} % {b} = {a % b}")
print(f"Exponentiation: {a} ** {b} = {a ** b}")

print("\n=== Order of Operations (PEMDAS) ===")
# Python follows the same order as math: Parentheses, Exponents, Multiplication/Division, Addition/Subtraction

result1 = 2 + 3 * 4
result2 = (2 + 3) * 4
result3 = 2 ** 3 + 1
result4 = (2 ** 3) + 1

print(f"2 + 3 * 4 = {result1}")        # Multiplication first: 2 + 12 = 14
print(f"(2 + 3) * 4 = {result2}")      # Parentheses first: 5 * 4 = 20
print(f"2 ** 3 + 1 = {result3}")       # Exponent first: 8 + 1 = 9
print(f"(2 ** 3) + 1 = {result4}")     # Same as above

print("\n=== Assignment Operators ===")
# These are shortcuts for common operations

x = 10
print(f"Starting value: x = {x}")

x += 5    # Same as x = x + 5
print(f"After x += 5: x = {x}")

x -= 3    # Same as x = x - 3
print(f"After x -= 3: x = {x}")

x *= 2    # Same as x = x * 2
print(f"After x *= 2: x = {x}")

x /= 4    # Same as x = x / 4
print(f"After x /= 4: x = {x}")

x **= 2   # Same as x = x ** 2
print(f"After x **= 2: x = {x}")

print("\n=== Built-in Math Functions ===")

numbers = [3.7, -2.1, 5, -8, 12.5]
print(f"Numbers: {numbers}")

print(f"Absolute value of -2.1: {abs(-2.1)}")
print(f"Round 3.7: {round(3.7)}")
print(f"Round 3.7 to 0 decimal places: {round(3.7, 0)}")
print(f"Round 3.14159 to 2 decimal places: {round(3.14159, 2)}")
print(f"Maximum: {max(numbers)}")
print(f"Minimum: {min(numbers)}")
print(f"Sum: {sum(numbers)}")

# Converting between number types
print("\n=== Converting Number Types ===")
float_num = 3.8
int_num = 7

print(f"Float to int: int({float_num}) = {int(float_num)}")  # Truncates decimal
print(f"Int to float: float({int_num}) = {float({int_num})}")

# Converting strings to numbers
string_number = "42"
string_float = "3.14"

print(f"String to int: int('{string_number}') = {int(string_number)}")
print(f"String to float: float('{string_float}') = {float(string_float)}")

print("\n=== Math Module ===")
# Python has a math module with more advanced functions
import math

print(f"Square root of 16: {math.sqrt(16)}")
print(f"Ceiling of 3.2: {math.ceil(3.2)}")    # Round up
print(f"Floor of 3.8: {math.floor(3.8)}")     # Round down
print(f"Pi: {math.pi}")
print(f"e: {math.e}")
print(f"Sin of 90 degrees: {math.sin(math.radians(90))}")
print(f"Log base 10 of 100: {math.log10(100)}")

print("\n=== Practical Examples ===")

# Calculate area of a circle
radius = 5
area = math.pi * radius ** 2
print(f"Area of circle with radius {radius}: {area:.2f}")

# Calculate compound interest
principal = 1000    # Starting amount
rate = 0.05        # 5% interest rate
time = 3           # 3 years
amount = principal * (1 + rate) ** time
print(f"${principal} at {rate*100}% for {time} years becomes: ${amount:.2f}")

# Temperature conversion
celsius = 25
fahrenheit = (celsius * 9/5) + 32
print(f"{celsius}°C = {fahrenheit}°F")

# Calculate average
test_scores = [85, 92, 78, 96, 88]
average = sum(test_scores) / len(test_scores)
print(f"Test scores: {test_scores}")
print(f"Average score: {average:.1f}")

print("\n=== Working with Random Numbers ===")
import random

print("Random numbers:")
print(f"Random float between 0 and 1: {random.random():.3f}")
print(f"Random integer between 1 and 10: {random.randint(1, 10)}")
print(f"Random choice from list: {random.choice(['apple', 'banana', 'orange'])}")

# Simulate rolling a dice
dice_roll = random.randint(1, 6)
print(f"Dice roll: {dice_roll}")

"""
Exercise for you:
1. Create a simple calculator:
   - Ask for two numbers (you can just assign them to variables for now)
   - Perform all basic operations (+, -, *, /, //, %, **)
   - Display the results

2. Calculate the area and perimeter of a rectangle:
   - Length = 8, Width = 5
   - Area = length * width
   - Perimeter = 2 * (length + width)

3. Work with a shopping cart:
   - Item 1: $12.99, Item 2: $8.50, Item 3: $15.25
   - Calculate total cost
   - Calculate tax (8.5%)
   - Calculate final total

4. Temperature converter:
   - Convert 32°F to Celsius: (F - 32) * 5/9
   - Convert 100°C to Fahrenheit: (C * 9/5) + 32

5. Use the math module:
   - Calculate the hypotenuse of a right triangle with sides 3 and 4
   - Find the square root of your age
   - Round pi to 3 decimal places

Bonus challenges:
- Generate 5 random numbers and find their average
- Calculate how long it takes to double money at 7% annual interest
- Create a tip calculator (bill amount, tip percentage)
"""

# Your practice space - add your code below: 