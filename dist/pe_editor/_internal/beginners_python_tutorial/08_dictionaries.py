"""
Lesson 8: Dictionaries - Key-Value Data Storage
===============================================

Dictionaries are one of Python's most powerful data structures.
They store data as key-value pairs, making them perfect for organizing
related information and creating fast lookups.

Key Concepts in this lesson:
- Creating and using dictionaries
- Dictionary methods and operations
- Nested dictionaries
- Dictionary comprehensions
- Real-world dictionary applications
"""

print("=== Creating Dictionaries ===")

# Different ways to create dictionaries
empty_dict = {}
person = {"name": "Alice", "age": 25, "city": "Boston"}
scores = {"math": 95, "science": 87, "english": 92}

print(f"Empty dictionary: {empty_dict}")
print(f"Person: {person}")
print(f"Scores: {scores}")

# Using dict() constructor
colors = dict(red="#FF0000", green="#00FF00", blue="#0000FF")
print(f"Colors: {colors}")

# Creating from lists of tuples
items = [("apple", 1.50), ("banana", 0.75), ("orange", 2.00)]
prices = dict(items)
print(f"Prices: {prices}")

print("\n=== Accessing Dictionary Values ===")

student = {
    "name": "Bob",
    "age": 17,
    "grade": "11th",
    "subjects": ["math", "science", "english"],
    "gpa": 3.8
}

print(f"Student data: {student}")

# Accessing values with keys
print(f"Name: {student['name']}")
print(f"Age: {student['age']}")
print(f"Subjects: {student['subjects']}")

# Using get() method (safer - doesn't crash if key doesn't exist)
print(f"GPA: {student.get('gpa')}")
print(f"Phone: {student.get('phone', 'Not provided')}")  # Default value

# Check if key exists
print(f"Has 'name' key: {'name' in student}")
print(f"Has 'phone' key: {'phone' in student}")

print("\n=== Modifying Dictionaries ===")

inventory = {"apples": 50, "bananas": 30, "oranges": 25}
print(f"Original inventory: {inventory}")

# Adding new items
inventory["grapes"] = 40
print(f"After adding grapes: {inventory}")

# Updating existing items
inventory["apples"] = 45
print(f"After updating apples: {inventory}")

# Adding multiple items at once
inventory.update({"pears": 20, "kiwis": 15})
print(f"After update: {inventory}")

# Removing items
removed_item = inventory.pop("bananas")  # Remove and return value
print(f"Removed {removed_item} bananas")
print(f"After removing bananas: {inventory}")

# Remove item (alternative way)
del inventory["oranges"]
print(f"After deleting oranges: {inventory}")

print("\n=== Dictionary Methods ===")

book = {
    "title": "Python Programming",
    "author": "Jane Smith",
    "year": 2023,
    "pages": 450,
    "isbn": "978-1234567890"
}

print(f"Book: {book}")

# Get all keys, values, and items
print(f"Keys: {list(book.keys())}")
print(f"Values: {list(book.values())}")
print(f"Items: {list(book.items())}")

# Iterating through dictionary
print("\nIterating through book:")
for key in book:
    print(f"{key}: {book[key]}")

print("\nUsing items():")
for key, value in book.items():
    print(f"{key}: {value}")

# Copy dictionary
book_copy = book.copy()
print(f"Copy: {book_copy}")

# Clear dictionary
temp_dict = {"a": 1, "b": 2}
temp_dict.clear()
print(f"After clear: {temp_dict}")

print("\n=== Nested Dictionaries ===")

# Dictionaries can contain other dictionaries
company = {
    "name": "Tech Solutions",
    "employees": {
        "alice": {
            "position": "Developer",
            "salary": 75000,
            "skills": ["Python", "JavaScript", "SQL"]
        },
        "bob": {
            "position": "Designer",
            "salary": 65000,
            "skills": ["Photoshop", "Illustrator", "CSS"]
        },
        "charlie": {
            "position": "Manager",
            "salary": 85000,
            "skills": ["Leadership", "Project Management"]
        }
    },
    "departments": ["Engineering", "Design", "Sales"]
}

print("Company structure:")
print(f"Company name: {company['name']}")
print(f"Departments: {company['departments']}")

# Accessing nested data
print(f"\nAlice's position: {company['employees']['alice']['position']}")
print(f"Bob's skills: {company['employees']['bob']['skills']}")

# Iterating through nested structure
print("\nEmployee details:")
for name, details in company["employees"].items():
    print(f"{name.title()}:")
    print(f"  Position: {details['position']}")
    print(f"  Salary: ${details['salary']:,}")
    print(f"  Skills: {', '.join(details['skills'])}")

print("\n=== Dictionary Comprehensions ===")

# Creating dictionaries with comprehensions
numbers = [1, 2, 3, 4, 5]

# Traditional way
squares_dict = {}
for num in numbers:
    squares_dict[num] = num ** 2
print(f"Squares (traditional): {squares_dict}")

# Dictionary comprehension
squares_comp = {num: num ** 2 for num in numbers}
print(f"Squares (comprehension): {squares_comp}")

# With condition
even_squares = {num: num ** 2 for num in numbers if num % 2 == 0}
print(f"Even squares: {even_squares}")

# From existing dictionary
grades = {"Alice": 85, "Bob": 92, "Charlie": 78, "Diana": 96}
passed = {name: grade for name, grade in grades.items() if grade >= 80}
print(f"Students who passed: {passed}")

# Transform values
grade_letters = {name: "A" if grade >= 90 else "B" if grade >= 80 else "C" 
                for name, grade in grades.items()}
print(f"Letter grades: {grade_letters}")

print("\n=== Practical Examples ===")

# Example 1: Word frequency counter
text = "the quick brown fox jumps over the lazy dog the fox is quick"
words = text.split()

word_count = {}
for word in words:
    word_count[word] = word_count.get(word, 0) + 1

print("Word frequencies:")
for word, count in sorted(word_count.items()):
    print(f"'{word}': {count}")

# Example 2: Student grade tracker
gradebook = {
    "Alice": {"math": [85, 92, 78], "science": [90, 88, 95], "english": [87, 91, 89]},
    "Bob": {"math": [79, 85, 82], "science": [84, 87, 90], "english": [88, 85, 92]},
    "Charlie": {"math": [92, 95, 89], "science": [96, 93, 98], "english": [85, 88, 91]}
}

print("\nGrade Report:")
for student, subjects in gradebook.items():
    print(f"\n{student}:")
    total_points = 0
    total_assignments = 0
    
    for subject, grades in subjects.items():
        average = sum(grades) / len(grades)
        total_points += sum(grades)
        total_assignments += len(grades)
        print(f"  {subject}: {grades} -> Average: {average:.1f}")
    
    overall_average = total_points / total_assignments
    print(f"  Overall Average: {overall_average:.1f}")

# Example 3: Inventory management system
store_inventory = {
    "electronics": {
        "laptop": {"price": 999.99, "stock": 5, "supplier": "TechCorp"},
        "phone": {"price": 699.99, "stock": 12, "supplier": "MobileTech"},
        "tablet": {"price": 399.99, "stock": 8, "supplier": "TechCorp"}
    },
    "books": {
        "python_guide": {"price": 49.99, "stock": 20, "supplier": "BookWorld"},
        "web_design": {"price": 39.99, "stock": 15, "supplier": "BookWorld"},
        "data_science": {"price": 59.99, "stock": 10, "supplier": "TechBooks"}
    }
}

print("\nInventory Report:")
total_value = 0

for category, items in store_inventory.items():
    print(f"\n{category.title()}:")
    category_value = 0
    
    for item, details in items.items():
        item_value = details["price"] * details["stock"]
        category_value += item_value
        total_value += item_value
        
        print(f"  {item}: ${details['price']:.2f} x {details['stock']} = ${item_value:.2f}")
        print(f"    Supplier: {details['supplier']}")
    
    print(f"  Category total: ${category_value:.2f}")

print(f"\nTotal inventory value: ${total_value:.2f}")

# Example 4: Configuration settings
app_config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "myapp_db",
        "user": "admin"
    },
    "api": {
        "base_url": "https://api.example.com",
        "timeout": 30,
        "retries": 3
    },
    "features": {
        "dark_mode": True,
        "notifications": True,
        "auto_save": False
    }
}

print("\nApplication Configuration:")
for section, settings in app_config.items():
    print(f"\n{section.upper()}:")
    for key, value in settings.items():
        print(f"  {key}: {value}")

print("\n=== Advanced Dictionary Techniques ===")

# Merging dictionaries (Python 3.9+)
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
dict3 = {"b": 20, "e": 5}  # Note: 'b' will be overwritten

merged = dict1 | dict2 | dict3  # Python 3.9+
print(f"Merged dictionaries: {merged}")

# Alternative merging for older Python versions
merged_old = {**dict1, **dict2, **dict3}
print(f"Merged (older Python): {merged_old}")

# Default dictionaries concept (using get with default)
def count_letters(text):
    counts = {}
    for letter in text.lower():
        if letter.isalpha():
            counts[letter] = counts.get(letter, 0) + 1
    return counts

letter_counts = count_letters("Hello World")
print(f"Letter counts: {letter_counts}")

# Grouping data
students_data = [
    {"name": "Alice", "grade": "A", "subject": "Math"},
    {"name": "Bob", "grade": "B", "subject": "Math"},
    {"name": "Alice", "grade": "A", "subject": "Science"},
    {"name": "Charlie", "grade": "C", "subject": "Math"},
    {"name": "Bob", "grade": "A", "subject": "Science"}
]

# Group by student
by_student = {}
for record in students_data:
    name = record["name"]
    if name not in by_student:
        by_student[name] = []
    by_student[name].append({"subject": record["subject"], "grade": record["grade"]})

print("\nGrouped by student:")
for student, records in by_student.items():
    print(f"{student}: {records}")

"""
Exercise for you:
1. Personal information:
   - Create a dictionary with your personal info (name, age, hobbies, etc.)
   - Add a new key for your favorite foods (as a list)
   - Update your age
   - Print all keys and values

2. Shopping cart:
   - Create a dictionary with items and their prices
   - Add quantities for each item
   - Calculate the total cost
   - Apply a 10% discount and show the final total

3. Contact book:
   - Create a nested dictionary with contacts (name -> phone, email, address)
   - Add a new contact
   - Update an existing contact's information
   - Search for a contact by name

4. Grade calculator:
   - Create a dictionary with subjects and lists of grades
   - Calculate the average for each subject
   - Find the subject with the highest average
   - Determine overall GPA

5. Inventory system:
   - Create a multi-level dictionary for a store inventory
   - Include categories, items, prices, and stock levels
   - Find items that are low in stock (< 5 units)
   - Calculate total inventory value

Bonus challenges:
- Create a simple English-to-Spanish dictionary translator
- Build a menu system for a restaurant with categories and prices
- Make a simple database of movies with ratings, genres, and years
- Create a configuration system that can be easily modified
"""

# Your practice space - add your code below: 