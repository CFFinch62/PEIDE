"""
Lesson 9: Functions - Organizing and Reusing Code
=================================================

Functions are reusable blocks of code that perform specific tasks.
They help organize your code, avoid repetition, and make programs easier to understand.

Key Concepts in this lesson:
- Defining and calling functions
- Parameters and arguments
- Return values
- Local vs global scope
- Default parameters
- Lambda functions
- Best practices for function design
"""

print("=== Basic Function Definition ===")

# Simple function with no parameters
def greet():
    print("Hello, World!")
    print("Welcome to Python functions!")

# Calling the function
print("Calling greet():")
greet()

# Function with parameters
def greet_person(name):
    print(f"Hello, {name}!")
    print("Nice to meet you!")

print("\nCalling greet_person():")
greet_person("Alice")
greet_person("Bob")

# Function with multiple parameters
def introduce(name, age, city):
    print(f"Hi, I'm {name}")
    print(f"I'm {age} years old")
    print(f"I live in {city}")

print("\nCalling introduce():")
introduce("Charlie", 25, "Boston")

print("\n=== Return Values ===")

# Function that returns a value
def add_numbers(a, b):
    result = a + b
    return result

# Using the returned value
sum_result = add_numbers(5, 3)
print(f"5 + 3 = {sum_result}")

# Function can return different types
def get_circle_info(radius):
    import math
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    return area, circumference  # Returns a tuple

# Unpacking returned values
area, circumference = get_circle_info(5)
print(f"Circle with radius 5:")
print(f"Area: {area:.2f}")
print(f"Circumference: {circumference:.2f}")

# Function that returns early
def check_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

print(f"\nGrade for 85: {check_grade(85)}")
print(f"Grade for 92: {check_grade(92)}")
print(f"Grade for 55: {check_grade(55)}")

print("\n=== Default Parameters ===")

# Function with default parameter values
def greet_with_title(name, title="Mr./Ms."):
    print(f"Hello, {title} {name}!")

print("Using default title:")
greet_with_title("Smith")

print("Using custom title:")
greet_with_title("Johnson", "Dr.")

# Multiple default parameters
def create_profile(name, age=18, city="Unknown", occupation="Student"):
    profile = {
        "name": name,
        "age": age,
        "city": city,
        "occupation": occupation
    }
    return profile

print("\nProfiles with different parameters:")
profile1 = create_profile("Alice")
profile2 = create_profile("Bob", 25)
profile3 = create_profile("Charlie", 30, "New York", "Engineer")

print(f"Profile 1: {profile1}")
print(f"Profile 2: {profile2}")
print(f"Profile 3: {profile3}")

print("\n=== Variable Scope ===")

# Global variable
global_message = "I'm a global variable"

def scope_example():
    # Local variable
    local_message = "I'm a local variable"
    print(f"Inside function: {local_message}")
    print(f"Inside function: {global_message}")

print("Before function call:")
print(f"Global message: {global_message}")

scope_example()

print("After function call:")
print(f"Global message: {global_message}")
# print(local_message)  # This would cause an error!

# Modifying global variables
counter = 0

def increment_counter():
    global counter  # Declare that we want to modify the global variable
    counter += 1
    print(f"Counter is now: {counter}")

print(f"\nInitial counter: {counter}")
increment_counter()
increment_counter()
increment_counter()

print("\n=== Practical Function Examples ===")

# Example 1: Temperature converter
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius"""
    celsius = (fahrenheit - 32) * 5/9
    return celsius

print("Temperature conversions:")
print(f"25°C = {celsius_to_fahrenheit(25):.1f}°F")
print(f"77°F = {fahrenheit_to_celsius(77):.1f}°C")

# Example 2: Calculator functions
def calculate(operation, a, b):
    """Perform basic arithmetic operations"""
    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        if b != 0:
            return a / b
        else:
            return "Error: Division by zero"
    else:
        return "Error: Unknown operation"

print("\nCalculator examples:")
print(f"10 + 5 = {calculate('+', 10, 5)}")
print(f"10 - 5 = {calculate('-', 10, 5)}")
print(f"10 * 5 = {calculate('*', 10, 5)}")
print(f"10 / 5 = {calculate('/', 10, 5)}")
print(f"10 / 0 = {calculate('/', 10, 0)}")

# Example 3: List processing functions
def find_maximum(numbers):
    """Find the maximum value in a list"""
    if not numbers:  # Empty list
        return None
    
    max_value = numbers[0]
    for number in numbers:
        if number > max_value:
            max_value = number
    return max_value

def calculate_average(numbers):
    """Calculate the average of a list of numbers"""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def filter_even_numbers(numbers):
    """Return a new list with only even numbers"""
    even_numbers = []
    for number in numbers:
        if number % 2 == 0:
            even_numbers.append(number)
    return even_numbers

test_numbers = [12, 7, 23, 45, 8, 34, 19, 56]
print(f"\nTest numbers: {test_numbers}")
print(f"Maximum: {find_maximum(test_numbers)}")
print(f"Average: {calculate_average(test_numbers):.2f}")
print(f"Even numbers: {filter_even_numbers(test_numbers)}")

print("\n=== Functions with Lists and Dictionaries ===")

def analyze_grades(student_grades):
    """Analyze a dictionary of student grades"""
    if not student_grades:
        return "No grades to analyze"
    
    all_grades = []
    for grades in student_grades.values():
        all_grades.extend(grades)
    
    analysis = {
        "total_students": len(student_grades),
        "total_grades": len(all_grades),
        "average_grade": sum(all_grades) / len(all_grades),
        "highest_grade": max(all_grades),
        "lowest_grade": min(all_grades)
    }
    
    return analysis

grades = {
    "Alice": [85, 92, 78, 96],
    "Bob": [79, 85, 88, 82],
    "Charlie": [92, 95, 89, 94]
}

analysis = analyze_grades(grades)
print("Grade analysis:")
for key, value in analysis.items():
    if isinstance(value, float):
        print(f"{key}: {value:.2f}")
    else:
        print(f"{key}: {value}")

def create_shopping_list(*items):
    """Create a shopping list from variable number of arguments"""
    shopping_list = []
    for item in items:
        shopping_list.append(item.title())
    return shopping_list

def add_to_inventory(inventory, **items):
    """Add items to inventory using keyword arguments"""
    for item, quantity in items.items():
        if item in inventory:
            inventory[item] += quantity
        else:
            inventory[item] = quantity
    return inventory

print("\nShopping list:")
my_list = create_shopping_list("apples", "bread", "milk", "eggs")
print(my_list)

print("\nInventory management:")
store_inventory = {"apples": 10, "bread": 5}
print(f"Initial inventory: {store_inventory}")

updated_inventory = add_to_inventory(store_inventory, apples=5, bananas=12, milk=8)
print(f"Updated inventory: {updated_inventory}")

print("\n=== Lambda Functions (Anonymous Functions) ===")

# Lambda functions are short, one-line functions
square = lambda x: x ** 2
add = lambda x, y: x + y
is_even = lambda x: x % 2 == 0

print("Lambda function examples:")
print(f"Square of 5: {square(5)}")
print(f"Add 3 and 7: {add(3, 7)}")
print(f"Is 8 even? {is_even(8)}")
print(f"Is 7 even? {is_even(7)}")

# Using lambda with built-in functions
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Filter even numbers
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"\nEven numbers: {even_numbers}")

# Square all numbers
squared_numbers = list(map(lambda x: x ** 2, numbers))
print(f"Squared numbers: {squared_numbers}")

# Sort by custom criteria
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
students_by_grade = sorted(students, key=lambda student: student[1])
print(f"Students sorted by grade: {students_by_grade}")

print("\n=== Function Documentation ===")

def calculate_compound_interest(principal, rate, time, compound_frequency=1):
    """
    Calculate compound interest.
    
    Args:
        principal (float): Initial amount of money
        rate (float): Annual interest rate (as decimal, e.g., 0.05 for 5%)
        time (float): Time period in years
        compound_frequency (int): Number of times interest is compounded per year
    
    Returns:
        tuple: (final_amount, interest_earned)
    
    Example:
        >>> calculate_compound_interest(1000, 0.05, 2)
        (1102.5, 102.5)
    """
    final_amount = principal * (1 + rate/compound_frequency) ** (compound_frequency * time)
    interest_earned = final_amount - principal
    return final_amount, interest_earned

# Using the documented function
final, interest = calculate_compound_interest(1000, 0.05, 2)
print(f"Investment result:")
print(f"Final amount: ${final:.2f}")
print(f"Interest earned: ${interest:.2f}")

# Access function documentation
print(f"\nFunction documentation:")
print(calculate_compound_interest.__doc__)

print("\n=== Error Handling in Functions ===")

def safe_divide(a, b):
    """Safely divide two numbers with error handling"""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

def validate_age(age):
    """Validate age input"""
    if not isinstance(age, (int, float)):
        return False, "Age must be a number"
    if age < 0:
        return False, "Age cannot be negative"
    if age > 150:
        return False, "Age seems unrealistic"
    return True, "Valid age"

print("Safe division examples:")
print(f"10 / 2 = {safe_divide(10, 2)}")
print(f"10 / 0 = {safe_divide(10, 0)}")
print(f"'10' / 2 = {safe_divide('10', 2)}")

print("\nAge validation examples:")
ages_to_test = [25, -5, 200, "twenty", 16.5]
for age in ages_to_test:
    is_valid, message = validate_age(age)
    print(f"Age {age}: {message}")

"""
Exercise for you:
1. Basic functions:
   - Create a function that calculates the area of a rectangle
   - Create a function that checks if a number is prime
   - Create a function that reverses a string
   - Create a function that finds the factorial of a number

2. Functions with lists:
   - Create a function that finds the second largest number in a list
   - Create a function that removes duplicates from a list
   - Create a function that counts vowels in a string
   - Create a function that merges two sorted lists

3. Practical applications:
   - Create a password strength checker function
   - Create a function that calculates shipping costs based on weight and distance
   - Create a function that converts between different units (meters/feet, kg/pounds)
   - Create a grade point average calculator

4. Advanced functions:
   - Create a function that takes another function as a parameter
   - Create a function that returns different functions based on input
   - Create a decorator function (advanced topic)

5. Real-world scenarios:
   - Create a simple banking system with deposit/withdraw functions
   - Create a text analyzer that counts words, sentences, and paragraphs
   - Create a simple game scoring system
   - Create a data validation system for user input

Bonus challenges:
- Create a recursive function to calculate Fibonacci numbers
- Build a simple calculator with memory functions
- Create a function that generates random passwords
- Make a function that converts numbers to words (1 -> "one")
"""

# Your practice space - add your code below: 