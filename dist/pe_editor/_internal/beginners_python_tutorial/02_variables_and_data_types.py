"""
Lesson 2: Variables and Data Types
==================================

In programming, we use variables to store information that we can use later.
Think of variables like labeled boxes where you can put different types of data.

Key Concepts in this lesson:
- What are variables?
- Different types of data (strings, numbers, booleans)
- How to create and use variables
- Naming rules for variables
"""

# Variables are like containers that hold data
# You create a variable by giving it a name and assigning a value with =

# String variables (text)
name = "Alice"
favorite_color = "blue"
message = "Learning Python is fun!"

print("String variables:")
print(name)
print(favorite_color)
print(message)

# Number variables
# Integers (whole numbers)
age = 16
number_of_pets = 2
year = 2024

print("\nInteger variables:")
print(age)
print(number_of_pets)
print(year)

# Floats (decimal numbers)
height = 5.6
temperature = 98.6
pi = 3.14159

print("\nFloat variables:")
print(height)
print(temperature)
print(pi)

# Boolean variables (True or False)
is_student = True
likes_pizza = True
is_raining = False

print("\nBoolean variables:")
print(is_student)
print(likes_pizza)
print(is_raining)

# You can change the value of a variable
print("\nChanging variable values:")
age = 16
print("Age was:", age)
age = 17  # Now age has a new value
print("Age is now:", age)

# Using variables together
print("\nUsing variables together:")
print("Hi, my name is", name)
print("I am", age, "years old")
print("My favorite color is", favorite_color)

# Variable naming rules:
# - Use letters, numbers, and underscores
# - Start with a letter or underscore (not a number)
# - Use descriptive names
# - Python is case-sensitive (Name and name are different)

first_name = "Bob"        # Good: descriptive and clear
last_name = "Smith"       # Good: uses underscore for multiple words
age_in_years = 15         # Good: very descriptive
x = 10                    # Okay for simple examples, but not very descriptive

print("\nMore examples:")
print("Full name:", first_name, last_name)
print("Age in years:", age_in_years)
print("Mystery number:", x)

"""
Exercise for you:
1. Create variables for your own information:
   - Your name (string)
   - Your age (integer)
   - Your height in feet (float)
   - Whether you like coding (boolean)

2. Print all your variables with descriptive messages

3. Try changing one of your variables and print it again

4. Create a variable with a bad name (like 2name) and see what error you get
"""

# Your practice space - add your code below: 