"""
Lesson 3: Strings and Text Formatting
=====================================

Strings are one of the most important data types in programming.
They represent text and have many useful methods for manipulation.

Key Concepts in this lesson:
- String creation and basic operations
- String methods (upper, lower, etc.)
- String formatting with f-strings
- Combining strings
- String indexing and slicing
"""

# Creating strings
first_name = "Python"
last_name = "Programmer"
language = "Python"

print("=== Basic String Operations ===")

# Combining strings (concatenation)
full_name = first_name + " " + last_name
print("Full name:", full_name)

# String length
print("Length of full name:", len(full_name))

# String methods - these don't change the original string, they return a new one
print("\n=== String Methods ===")
print("Original:", full_name)
print("Uppercase:", full_name.upper())
print("Lowercase:", full_name.lower())
print("Title case:", full_name.title())

# Check what's in a string
sentence = "I love learning Python programming!"
print("\nSentence:", sentence)
print("Contains 'Python':", "Python" in sentence)
print("Contains 'Java':", "Java" in sentence)
print("Starts with 'I':", sentence.startswith("I"))
print("Ends with '!':", sentence.endswith("!"))

# String formatting with f-strings (the modern way!)
print("\n=== F-String Formatting ===")
name = "Alex"
age = 16
height = 5.8
is_student = True

# f-strings let you put variables directly in strings
print(f"Hi, I'm {name}")
print(f"I am {age} years old")
print(f"My height is {height} feet")
print(f"Am I a student? {is_student}")

# You can do calculations inside f-strings
print(f"Next year I'll be {age + 1} years old")
print(f"My height in inches is approximately {height * 12:.1f}")

# Formatting numbers
price = 19.99
print(f"The price is ${price:.2f}")  # .2f means 2 decimal places

# String indexing - accessing individual characters
print("\n=== String Indexing ===")
word = "Python"
print("Word:", word)
print("First letter:", word[0])    # Indexing starts at 0
print("Second letter:", word[1])
print("Last letter:", word[-1])    # Negative indexing starts from the end
print("Second to last:", word[-2])

# String slicing - getting parts of a string
print("\n=== String Slicing ===")
message = "Hello, World!"
print("Original message:", message)
print("First 5 characters:", message[0:5])   # or message[:5]
print("Characters 7 to end:", message[7:])
print("Last 6 characters:", message[-6:])
print("Every other character:", message[::2])
print("Reverse the string:", message[::-1])

# Multi-line strings
print("\n=== Multi-line Strings ===")
poem = """Roses are red,
Violets are blue,
Python is awesome,
And so are you!"""
print(poem)

# Escape characters
print("\n=== Escape Characters ===")
print("This has a \"quote\" inside")
print("This has a \\ backslash")
print("Line 1\nLine 2")  # \n creates a new line
print("Column 1\tColumn 2")  # \t creates a tab

# String replacement
print("\n=== String Replacement ===")
text = "I love Java programming"
new_text = text.replace("Java", "Python")
print("Original:", text)
print("Modified:", new_text)

# Splitting strings
print("\n=== Splitting Strings ===")
fruits = "apple,banana,orange,grape"
fruit_list = fruits.split(",")
print("Original string:", fruits)
print("Split into list:", fruit_list)

# Joining strings
print("\n=== Joining Strings ===")
words = ["Python", "is", "really", "cool"]
sentence = " ".join(words)
print("List of words:", words)
print("Joined sentence:", sentence)

"""
Exercise for you:
1. Create variables for your first name, last name, and favorite hobby
2. Use f-strings to create a sentence introducing yourself
3. Try different string methods on your name (upper, lower, title)
4. Get the first and last letter of your first name using indexing
5. Create a multi-line string with a short poem or message
6. Replace a word in a sentence with a different word
7. Split your full name into a list of words

Bonus challenges:
- Create a string with your favorite quote and count how many words it has
- Reverse your name using string slicing
- Create a formatted string showing a price with exactly 2 decimal places
"""

# Your practice space - add your code below: 