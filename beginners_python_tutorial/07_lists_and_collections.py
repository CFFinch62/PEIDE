"""
Lesson 7: Lists and Collections
===============================

Collections allow you to store multiple pieces of data together.
Python has several types of collections, each with different characteristics.

Key Concepts in this lesson:
- Creating and using lists
- List methods (append, remove, etc.)
- List indexing and slicing
- Tuples (immutable lists)
- Sets (unique collections)
- List comprehensions
- Practical collection examples
"""

print("=== Creating Lists ===")

# Different ways to create lists
empty_list = []
numbers = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "orange"]
mixed = [1, "hello", 3.14, True]  # Lists can contain different types

print(f"Empty list: {empty_list}")
print(f"Numbers: {numbers}")
print(f"Fruits: {fruits}")
print(f"Mixed types: {mixed}")

# Creating lists with range
range_list = list(range(5))
print(f"From range: {range_list}")

# Creating lists with repetition
repeated = ["hello"] * 3
zeros = [0] * 5
print(f"Repeated: {repeated}")
print(f"Zeros: {zeros}")

print("\n=== Accessing List Elements ===")

colors = ["red", "green", "blue", "yellow", "purple"]
print(f"Colors: {colors}")

# Indexing (starts at 0)
print(f"First color: {colors[0]}")
print(f"Second color: {colors[1]}")
print(f"Last color: {colors[-1]}")
print(f"Second to last: {colors[-2]}")

# Length of list
print(f"Number of colors: {len(colors)}")

# Check if item exists
print(f"Is 'blue' in colors? {'blue' in colors}")
print(f"Is 'pink' in colors? {'pink' in colors}")

print("\n=== List Slicing ===")

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"Numbers: {numbers}")

print(f"First 3: {numbers[:3]}")
print(f"Last 3: {numbers[-3:]}")
print(f"Middle (index 3-6): {numbers[3:7]}")
print(f"Every other: {numbers[::2]}")
print(f"Reverse: {numbers[::-1]}")
print(f"Every 3rd from index 1: {numbers[1::3]}")

print("\n=== Modifying Lists ===")

# Lists are mutable (can be changed)
shopping_list = ["milk", "bread", "eggs"]
print(f"Original: {shopping_list}")

# Adding items
shopping_list.append("cheese")  # Add to end
print(f"After append: {shopping_list}")

shopping_list.insert(1, "butter")  # Insert at specific position
print(f"After insert: {shopping_list}")

shopping_list.extend(["apples", "bananas"])  # Add multiple items
print(f"After extend: {shopping_list}")

# Removing items
shopping_list.remove("bread")  # Remove first occurrence
print(f"After remove: {shopping_list}")

last_item = shopping_list.pop()  # Remove and return last item
print(f"Popped item: {last_item}")
print(f"After pop: {shopping_list}")

second_item = shopping_list.pop(1)  # Remove and return item at index
print(f"Popped item at index 1: {second_item}")
print(f"After pop(1): {shopping_list}")

# Changing items
shopping_list[0] = "almond milk"  # Change first item
print(f"After change: {shopping_list}")

print("\n=== List Methods ===")

numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"Original numbers: {numbers}")

# Sorting
numbers_copy = numbers.copy()  # Make a copy first
numbers_copy.sort()  # Sort in place
print(f"Sorted: {numbers_copy}")

# Sorting without changing original
sorted_numbers = sorted(numbers)  # Returns new sorted list
print(f"Original unchanged: {numbers}")
print(f"New sorted list: {sorted_numbers}")

# Reverse
numbers.reverse()
print(f"Reversed: {numbers}")

# Count occurrences
count_of_1 = numbers.count(1)
print(f"Number of 1s: {count_of_1}")

# Find index
index_of_4 = numbers.index(4)
print(f"Index of 4: {index_of_4}")

# Clear all items
temp_list = [1, 2, 3]
temp_list.clear()
print(f"After clear: {temp_list}")

print("\n=== List Comprehensions ===")

# Traditional way to create a list
squares = []
for i in range(5):
    squares.append(i ** 2)
print(f"Squares (traditional): {squares}")

# List comprehension way
squares_comp = [i ** 2 for i in range(5)]
print(f"Squares (comprehension): {squares_comp}")

# With condition
even_squares = [i ** 2 for i in range(10) if i % 2 == 0]
print(f"Even squares: {even_squares}")

# Processing existing list
words = ["hello", "world", "python", "programming"]
lengths = [len(word) for word in words]
print(f"Word lengths: {lengths}")

uppercase_words = [word.upper() for word in words if len(word) > 5]
print(f"Long words uppercase: {uppercase_words}")

print("\n=== Tuples (Immutable Lists) ===")

# Tuples are like lists but cannot be changed
coordinates = (3, 5)
rgb_color = (255, 128, 0)
person = ("Alice", 25, "Engineer")

print(f"Coordinates: {coordinates}")
print(f"RGB color: {rgb_color}")
print(f"Person: {person}")

# Accessing tuple elements (same as lists)
print(f"X coordinate: {coordinates[0]}")
print(f"Y coordinate: {coordinates[1]}")
print(f"Person's name: {person[0]}")

# Tuple unpacking
x, y = coordinates
name, age, job = person
print(f"Unpacked coordinates: x={x}, y={y}")
print(f"Unpacked person: {name} is {age} years old and works as {job}")

# Tuples are useful for returning multiple values from functions
def get_name_age():
    return "Bob", 30

name, age = get_name_age()
print(f"Function returned: {name}, {age}")

print("\n=== Sets (Unique Collections) ===")

# Sets contain only unique elements
numbers_set = {1, 2, 3, 4, 5}
fruits_set = {"apple", "banana", "orange"}
mixed_set = {1, "hello", 3.14}

print(f"Numbers set: {numbers_set}")
print(f"Fruits set: {fruits_set}")

# Sets automatically remove duplicates
duplicates = {1, 2, 2, 3, 3, 3, 4}
print(f"Set with duplicates removed: {duplicates}")

# Converting list to set (removes duplicates)
numbers_with_dupes = [1, 2, 2, 3, 3, 3, 4, 4]
unique_numbers = set(numbers_with_dupes)
print(f"Original list: {numbers_with_dupes}")
print(f"Unique set: {unique_numbers}")

# Set operations
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

print(f"Set 1: {set1}")
print(f"Set 2: {set2}")
print(f"Union (all elements): {set1 | set2}")
print(f"Intersection (common elements): {set1 & set2}")
print(f"Difference (in set1 but not set2): {set1 - set2}")

# Adding to sets
fruits_set.add("grape")
print(f"After adding grape: {fruits_set}")

print("\n=== Nested Lists (2D Lists) ===")

# Lists can contain other lists
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print("Matrix:")
for row in matrix:
    print(row)

# Accessing elements in 2D list
print(f"Element at row 1, column 2: {matrix[1][2]}")  # Should be 6

# Creating a multiplication table
table = []
for i in range(1, 4):
    row = []
    for j in range(1, 4):
        row.append(i * j)
    table.append(row)

print("\nMultiplication table:")
for row in table:
    print(row)

print("\n=== Practical Examples ===")

# Example 1: Grade book
students = [
    {"name": "Alice", "grades": [85, 92, 78, 96]},
    {"name": "Bob", "grades": [79, 85, 88, 82]},
    {"name": "Charlie", "grades": [92, 95, 89, 94]}
]

print("Grade Report:")
for student in students:
    name = student["name"]
    grades = student["grades"]
    average = sum(grades) / len(grades)
    print(f"{name}: {grades} -> Average: {average:.1f}")

# Example 2: Inventory management
inventory = [
    {"item": "laptop", "quantity": 5, "price": 999.99},
    {"item": "mouse", "quantity": 20, "price": 25.50},
    {"item": "keyboard", "quantity": 15, "price": 75.00}
]

print("\nInventory Report:")
total_value = 0
for item in inventory:
    item_value = item["quantity"] * item["price"]
    total_value += item_value
    print(f"{item['item']}: {item['quantity']} units @ ${item['price']:.2f} = ${item_value:.2f}")

print(f"Total inventory value: ${total_value:.2f}")

# Example 3: Text analysis
text = "the quick brown fox jumps over the lazy dog"
words = text.split()
print(f"\nText: {text}")
print(f"Words: {words}")
print(f"Word count: {len(words)}")

# Count word frequencies
word_count = {}
for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

print("Word frequencies:")
for word, count in word_count.items():
    print(f"'{word}': {count}")

# Example 4: Data filtering and processing
temperatures = [72, 68, 75, 82, 79, 85, 71, 77, 80, 73]
print(f"\nTemperatures: {temperatures}")

# Filter temperatures above 75
hot_days = [temp for temp in temperatures if temp > 75]
print(f"Hot days (>75°F): {hot_days}")

# Calculate statistics
average_temp = sum(temperatures) / len(temperatures)
max_temp = max(temperatures)
min_temp = min(temperatures)

print(f"Average temperature: {average_temp:.1f}°F")
print(f"Highest temperature: {max_temp}°F")
print(f"Lowest temperature: {min_temp}°F")

"""
Exercise for you:
1. List basics:
   - Create a list of your favorite movies
   - Add a new movie to the end
   - Insert a movie at the beginning
   - Remove a movie you don't like anymore
   - Sort the list alphabetically

2. Number processing:
   - Create a list of random numbers [23, 45, 12, 67, 34, 89, 56]
   - Find the sum, average, maximum, and minimum
   - Create a new list with only even numbers
   - Create a new list with each number doubled

3. String manipulation:
   - Create a list of words: ["python", "programming", "is", "fun"]
   - Create a new list with word lengths
   - Create a new list with words longer than 3 characters
   - Join all words into a single sentence

4. Tuple practice:
   - Create tuples for 3 different cities with (name, population, country)
   - Unpack each tuple and print formatted information
   - Find the city with the largest population

5. Set operations:
   - Create two sets of your friends' names
   - Find friends that are in both sets
   - Find friends that are only in the first set
   - Combine both sets to get all unique friends

Bonus challenges:
- Create a simple contact book using lists of dictionaries
- Build a shopping cart that calculates totals and applies discounts
- Make a simple gradebook that tracks multiple students and subjects
- Create a word game that finds anagrams using sets
"""

# Your practice space - add your code below: 