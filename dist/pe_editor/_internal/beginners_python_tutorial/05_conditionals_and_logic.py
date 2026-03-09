"""
Lesson 5: Conditionals and Boolean Logic
========================================

Conditionals allow your programs to make decisions and respond differently
based on various conditions. This is where your programs start to become "smart"!

Key Concepts in this lesson:
- Boolean values (True/False)
- Comparison operators
- Logical operators (and, or, not)
- if, elif, and else statements
- Nested conditionals
- Practical decision-making examples
"""

print("=== Boolean Values ===")

# Boolean values are either True or False
is_sunny = True
is_raining = False
is_student = True

print(f"Is sunny: {is_sunny}")
print(f"Is raining: {is_raining}")
print(f"Is student: {is_student}")

# You can also get boolean values from expressions
print(f"5 > 3: {5 > 3}")
print(f"10 == 5: {10 == 5}")

print("\n=== Comparison Operators ===")

age = 16
height = 5.8
name = "Alex"

print(f"Age: {age}")
print(f"age == 16: {age == 16}")        # Equal to
print(f"age != 18: {age != 18}")        # Not equal to
print(f"age > 15: {age > 15}")          # Greater than
print(f"age < 20: {age < 20}")          # Less than
print(f"age >= 16: {age >= 16}")        # Greater than or equal to
print(f"age <= 15: {age <= 15}")        # Less than or equal to

# Comparing strings
print(f"\nname == 'Alex': {name == 'Alex'}")
print(f"name == 'alex': {name == 'alex'}")  # Case sensitive!

print("\n=== Logical Operators ===")

is_teenager = age >= 13 and age <= 19
is_tall = height > 6.0
likes_pizza = True

print(f"Is teenager (13-19): {is_teenager}")
print(f"Is tall (>6.0): {is_tall}")

# AND operator - both conditions must be True
print(f"Is teenager AND tall: {is_teenager and is_tall}")

# OR operator - at least one condition must be True
print(f"Is teenager OR tall: {is_teenager or is_tall}")

# NOT operator - flips True to False and vice versa
print(f"NOT is_tall: {not is_tall}")
print(f"NOT likes_pizza: {not likes_pizza}")

print("\n=== Basic if Statements ===")

temperature = 75

if temperature > 80:
    print("It's hot outside!")

if temperature <= 80:
    print("It's not too hot.")

# You can have multiple statements in an if block
if temperature >= 70:
    print("Nice weather!")
    print("Good day for a walk.")

print("\n=== if-else Statements ===")

score = 85

if score >= 90:
    print("Excellent! You got an A!")
else:
    print("Good job, but you can do better!")

# Another example
hour = 14  # 2 PM in 24-hour format

if hour < 12:
    print("Good morning!")
else:
    print("Good afternoon or evening!")

print("\n=== if-elif-else Statements ===")

# elif lets you check multiple conditions
grade = 87

if grade >= 90:
    letter_grade = "A"
elif grade >= 80:
    letter_grade = "B"
elif grade >= 70:
    letter_grade = "C"
elif grade >= 60:
    letter_grade = "D"
else:
    letter_grade = "F"

print(f"Grade {grade} is a {letter_grade}")

# Weather example
weather = "sunny"

if weather == "sunny":
    print("Wear sunglasses!")
elif weather == "rainy":
    print("Bring an umbrella!")
elif weather == "snowy":
    print("Wear a warm coat!")
elif weather == "cloudy":
    print("Might want a light jacket.")
else:
    print("Check the weather forecast!")

print("\n=== Nested Conditionals ===")

# You can put if statements inside other if statements
age = 17
has_license = True
has_car = False

if age >= 16:
    print("You're old enough to drive!")
    if has_license:
        print("You have a license!")
        if has_car:
            print("You can drive your own car!")
        else:
            print("You might need to borrow a car.")
    else:
        print("You need to get your license first.")
else:
    print("You're too young to drive.")

print("\n=== Complex Conditions ===")

# Combining multiple conditions
username = "student123"
password = "secret456"
is_logged_in = False

# Check login credentials
if username == "student123" and password == "secret456":
    is_logged_in = True
    print("Login successful!")
else:
    print("Invalid username or password!")

# Age and permission example
age = 15
has_parent_permission = True

if (age >= 18) or (age >= 13 and has_parent_permission):
    print("You can sign up for the program!")
else:
    print("You need to be 18 or have parent permission if you're 13-17.")

print("\n=== Checking Multiple Values ===")

# Using 'in' to check if a value is in a list
favorite_color = "blue"
primary_colors = ["red", "blue", "yellow"]

if favorite_color in primary_colors:
    print(f"{favorite_color} is a primary color!")
else:
    print(f"{favorite_color} is not a primary color.")

# Checking ranges
test_score = 92

if 90 <= test_score <= 100:
    print("Outstanding performance!")
elif 80 <= test_score < 90:
    print("Great job!")
elif 70 <= test_score < 80:
    print("Good work!")
else:
    print("Keep studying!")

print("\n=== Practical Examples ===")

# Example 1: Simple calculator decision
operation = "+"
num1 = 10
num2 = 5

if operation == "+":
    result = num1 + num2
elif operation == "-":
    result = num1 - num2
elif operation == "*":
    result = num1 * num2
elif operation == "/":
    if num2 != 0:  # Check for division by zero
        result = num1 / num2
    else:
        result = "Error: Cannot divide by zero"
else:
    result = "Error: Unknown operation"

print(f"{num1} {operation} {num2} = {result}")

# Example 2: Discount calculator
purchase_amount = 150
is_member = True
is_student = False

discount = 0

if is_member:
    discount += 10  # 10% member discount
if is_student:
    discount += 5   # Additional 5% student discount
if purchase_amount > 100:
    discount += 5   # 5% discount for purchases over $100

final_amount = purchase_amount * (1 - discount/100)
print(f"Purchase: ${purchase_amount}")
print(f"Total discount: {discount}%")
print(f"Final amount: ${final_amount:.2f}")

# Example 3: Game logic
player_health = 75
has_potion = True
enemy_nearby = True

if player_health < 50:
    if has_potion:
        print("Your health is low! Use a health potion.")
    else:
        print("Your health is low! Find a health potion quickly!")
elif enemy_nearby:
    print("Enemy detected! Prepare for battle!")
else:
    print("All clear! Continue exploring.")

print("\n=== Ternary Operator (One-line if) ===")

# Short way to write simple if-else statements
age = 17
status = "adult" if age >= 18 else "minor"
print(f"Age {age}: You are a {status}")

# Another example
temperature = 85
clothing = "shorts" if temperature > 75 else "pants"
print(f"Temperature {temperature}°F: Wear {clothing}")

# With numbers
x = 10
y = 5
larger = x if x > y else y
print(f"The larger number between {x} and {y} is {larger}")

"""
Exercise for you:
1. Create a grade calculator:
   - Take a test score (0-100)
   - Assign letter grades: A (90-100), B (80-89), C (70-79), D (60-69), F (0-59)
   - Add special messages for perfect scores and failing grades

2. Build a simple login system:
   - Check if username is "admin" and password is "password123"
   - Give different messages for wrong username vs wrong password
   - Track number of failed attempts

3. Create a movie rating system:
   - Based on age, determine what movie ratings they can watch
   - G (all ages), PG (all ages), PG-13 (13+), R (17+)
   - Consider if they have parent permission

4. Weather clothing advisor:
   - Based on temperature and weather conditions, suggest clothing
   - Consider: temperature, rain, snow, wind
   - Give specific recommendations

5. Number guessing game logic:
   - Pick a secret number (1-10)
   - Check if a guess is too high, too low, or correct
   - Give encouraging messages

Bonus challenges:
- Create a tax calculator based on income brackets
- Build a shipping cost calculator based on weight and distance
- Make a password strength checker (length, special characters, etc.)
"""

# Your practice space - add your code below: 