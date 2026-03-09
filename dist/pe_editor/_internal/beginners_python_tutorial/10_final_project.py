"""
Lesson 10: Final Project - Building a Complete Program
======================================================

Congratulations! You've learned the fundamentals of Python programming.
Now let's put it all together by building a complete program that uses
all the concepts you've learned.

This lesson includes:
- A complete student grade management system
- Multiple smaller projects to practice
- Code organization and best practices
- Next steps for your programming journey
"""

print("=== Final Project: Student Grade Management System ===")
print("This system demonstrates all the concepts you've learned!\n")

# Global data storage
students_database = {}
subjects_list = ["Math", "Science", "English", "History", "Art"]

def display_menu():
    """Display the main menu options"""
    print("\n" + "="*50)
    print("    STUDENT GRADE MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add New Student")
    print("2. Add Grade for Student")
    print("3. View Student Report")
    print("4. View All Students")
    print("5. Calculate Class Statistics")
    print("6. Find Top Performers")
    print("7. Export Data")
    print("8. Exit")
    print("="*50)

def add_student():
    """Add a new student to the database"""
    print("\n--- Adding New Student ---")
    
    name = input("Enter student name: ").strip().title()
    if not name:
        print("Error: Name cannot be empty!")
        return
    
    if name in students_database:
        print(f"Error: Student '{name}' already exists!")
        return
    
    # Get student information
    try:
        age = int(input("Enter student age: "))
        if age < 5 or age > 25:
            print("Warning: Age seems unusual for a student")
    except ValueError:
        print("Error: Please enter a valid age!")
        return
    
    grade_level = input("Enter grade level (e.g., 9th, 10th): ").strip()
    
    # Initialize student record
    students_database[name] = {
        "age": age,
        "grade_level": grade_level,
        "subjects": {subject: [] for subject in subjects_list},
        "date_added": "2024"  # In a real app, you'd use datetime
    }
    
    print(f"✓ Student '{name}' added successfully!")

def add_grade():
    """Add a grade for an existing student"""
    print("\n--- Adding Grade ---")
    
    if not students_database:
        print("No students in database. Please add students first.")
        return
    
    # Show available students
    print("Available students:")
    for i, name in enumerate(students_database.keys(), 1):
        print(f"{i}. {name}")
    
    student_name = input("\nEnter student name: ").strip().title()
    
    if student_name not in students_database:
        print(f"Error: Student '{student_name}' not found!")
        return
    
    # Show available subjects
    print("\nAvailable subjects:")
    for i, subject in enumerate(subjects_list, 1):
        print(f"{i}. {subject}")
    
    subject = input("Enter subject name: ").strip().title()
    
    if subject not in subjects_list:
        print(f"Error: Subject '{subject}' not available!")
        return
    
    # Get grade
    try:
        grade = float(input("Enter grade (0-100): "))
        if grade < 0 or grade > 100:
            print("Error: Grade must be between 0 and 100!")
            return
    except ValueError:
        print("Error: Please enter a valid grade!")
        return
    
    # Add grade to student record
    students_database[student_name]["subjects"][subject].append(grade)
    print(f"✓ Grade {grade} added for {student_name} in {subject}")

def calculate_student_average(student_data):
    """Calculate overall average for a student"""
    all_grades = []
    for grades in student_data["subjects"].values():
        all_grades.extend(grades)
    
    if not all_grades:
        return 0
    
    return sum(all_grades) / len(all_grades)

def get_letter_grade(average):
    """Convert numerical grade to letter grade"""
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"

def view_student_report():
    """Display detailed report for a specific student"""
    print("\n--- Student Report ---")
    
    if not students_database:
        print("No students in database.")
        return
    
    student_name = input("Enter student name: ").strip().title()
    
    if student_name not in students_database:
        print(f"Error: Student '{student_name}' not found!")
        return
    
    student = students_database[student_name]
    
    print(f"\n{'='*60}")
    print(f"STUDENT REPORT: {student_name}")
    print(f"{'='*60}")
    print(f"Age: {student['age']}")
    print(f"Grade Level: {student['grade_level']}")
    print(f"Date Added: {student['date_added']}")
    print(f"\nSUBJECT GRADES:")
    print("-" * 40)
    
    subject_averages = {}
    total_grades = 0
    
    for subject, grades in student["subjects"].items():
        if grades:
            average = sum(grades) / len(grades)
            subject_averages[subject] = average
            total_grades += len(grades)
            print(f"{subject:12}: {grades} → Average: {average:.1f} ({get_letter_grade(average)})")
        else:
            print(f"{subject:12}: No grades recorded")
    
    if subject_averages:
        overall_average = calculate_student_average(student)
        print(f"\n{'='*40}")
        print(f"OVERALL AVERAGE: {overall_average:.1f} ({get_letter_grade(overall_average)})")
        print(f"TOTAL GRADES: {total_grades}")
        print(f"{'='*40}")

def view_all_students():
    """Display summary of all students"""
    print("\n--- All Students Summary ---")
    
    if not students_database:
        print("No students in database.")
        return
    
    print(f"{'Name':<15} {'Age':<5} {'Grade':<8} {'Avg':<6} {'Letter':<6} {'Total Grades'}")
    print("-" * 60)
    
    for name, data in students_database.items():
        average = calculate_student_average(data)
        letter = get_letter_grade(average)
        
        # Count total grades
        total_grades = sum(len(grades) for grades in data["subjects"].values())
        
        print(f"{name:<15} {data['age']:<5} {data['grade_level']:<8} {average:<6.1f} {letter:<6} {total_grades}")

def calculate_class_statistics():
    """Calculate and display class-wide statistics"""
    print("\n--- Class Statistics ---")
    
    if not students_database:
        print("No students in database.")
        return
    
    all_averages = []
    subject_stats = {subject: [] for subject in subjects_list}
    
    # Collect data
    for student_data in students_database.values():
        student_avg = calculate_student_average(student_data)
        if student_avg > 0:  # Only include students with grades
            all_averages.append(student_avg)
        
        for subject, grades in student_data["subjects"].items():
            if grades:
                subject_avg = sum(grades) / len(grades)
                subject_stats[subject].append(subject_avg)
    
    if not all_averages:
        print("No grades recorded yet.")
        return
    
    # Calculate overall statistics
    class_average = sum(all_averages) / len(all_averages)
    highest_avg = max(all_averages)
    lowest_avg = min(all_averages)
    
    print(f"Class Average: {class_average:.1f}")
    print(f"Highest Student Average: {highest_avg:.1f}")
    print(f"Lowest Student Average: {lowest_avg:.1f}")
    print(f"Total Students with Grades: {len(all_averages)}")
    
    # Subject statistics
    print(f"\nSubject Averages:")
    print("-" * 30)
    for subject, averages in subject_stats.items():
        if averages:
            subject_avg = sum(averages) / len(averages)
            print(f"{subject:12}: {subject_avg:.1f}")
        else:
            print(f"{subject:12}: No grades")

def find_top_performers():
    """Find and display top performing students"""
    print("\n--- Top Performers ---")
    
    if not students_database:
        print("No students in database.")
        return
    
    # Calculate averages for all students
    student_averages = []
    for name, data in students_database.items():
        average = calculate_student_average(data)
        if average > 0:
            student_averages.append((name, average))
    
    if not student_averages:
        print("No grades recorded yet.")
        return
    
    # Sort by average (highest first)
    student_averages.sort(key=lambda x: x[1], reverse=True)
    
    print("🏆 TOP PERFORMERS:")
    print("-" * 40)
    
    for i, (name, average) in enumerate(student_averages[:5], 1):
        letter = get_letter_grade(average)
        if i == 1:
            print(f"🥇 {i}. {name}: {average:.1f} ({letter})")
        elif i == 2:
            print(f"🥈 {i}. {name}: {average:.1f} ({letter})")
        elif i == 3:
            print(f"🥉 {i}. {name}: {average:.1f} ({letter})")
        else:
            print(f"   {i}. {name}: {average:.1f} ({letter})")

def export_data():
    """Export student data to a formatted text file"""
    print("\n--- Export Data ---")
    
    if not students_database:
        print("No data to export.")
        return
    
    filename = "student_grades_export.txt"
    
    try:
        with open(filename, 'w') as file:
            file.write("STUDENT GRADE MANAGEMENT SYSTEM - DATA EXPORT\n")
            file.write("=" * 60 + "\n\n")
            
            for name, data in students_database.items():
                file.write(f"Student: {name}\n")
                file.write(f"Age: {data['age']}, Grade Level: {data['grade_level']}\n")
                file.write("-" * 30 + "\n")
                
                for subject, grades in data["subjects"].items():
                    if grades:
                        average = sum(grades) / len(grades)
                        file.write(f"{subject}: {grades} (Avg: {average:.1f})\n")
                    else:
                        file.write(f"{subject}: No grades\n")
                
                overall_avg = calculate_student_average(data)
                file.write(f"Overall Average: {overall_avg:.1f} ({get_letter_grade(overall_avg)})\n")
                file.write("\n" + "="*60 + "\n\n")
        
        print(f"✓ Data exported successfully to '{filename}'")
        
    except Exception as e:
        print(f"Error exporting data: {e}")

def main_program():
    """Main program loop"""
    print("Welcome to the Student Grade Management System!")
    print("This program demonstrates all Python concepts you've learned.")
    
    # Add some sample data for demonstration
    print("\nAdding sample data for demonstration...")
    students_database["Alice Johnson"] = {
        "age": 16,
        "grade_level": "10th",
        "subjects": {
            "Math": [85, 92, 78],
            "Science": [90, 88, 95],
            "English": [87, 91, 89],
            "History": [82, 85, 88],
            "Art": [95, 92, 98]
        },
        "date_added": "2024"
    }
    
    students_database["Bob Smith"] = {
        "age": 17,
        "grade_level": "11th",
        "subjects": {
            "Math": [79, 85, 82],
            "Science": [84, 87, 90],
            "English": [88, 85, 92],
            "History": [86, 89, 91],
            "Art": [78, 82, 85]
        },
        "date_added": "2024"
    }
    
    print("Sample students added: Alice Johnson and Bob Smith")
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == "1":
                add_student()
            elif choice == "2":
                add_grade()
            elif choice == "3":
                view_student_report()
            elif choice == "4":
                view_all_students()
            elif choice == "5":
                calculate_class_statistics()
            elif choice == "6":
                find_top_performers()
            elif choice == "7":
                export_data()
            elif choice == "8":
                print("\nThank you for using the Student Grade Management System!")
                print("Keep practicing and happy coding! 🐍")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.")

# Run a demonstration of the system
print("=== DEMONSTRATION MODE ===")
print("Let's see the system in action with sample data!\n")

# Add sample data
students_database["Alice Johnson"] = {
    "age": 16,
    "grade_level": "10th",
    "subjects": {
        "Math": [85, 92, 78],
        "Science": [90, 88, 95],
        "English": [87, 91, 89],
        "History": [82, 85, 88],
        "Art": [95, 92, 98]
    },
    "date_added": "2024"
}

students_database["Bob Smith"] = {
    "age": 17,
    "grade_level": "11th",
    "subjects": {
        "Math": [79, 85, 82],
        "Science": [84, 87, 90],
        "English": [88, 85, 92],
        "History": [86, 89, 91],
        "Art": [78, 82, 85]
    },
    "date_added": "2024"
}

# Demonstrate various functions
print("1. Viewing all students:")
view_all_students()

print("\n2. Class statistics:")
calculate_class_statistics()

print("\n3. Top performers:")
find_top_performers()

print("\n4. Detailed report for Alice:")
# Simulate user input for demonstration
import sys
from io import StringIO

# Temporarily redirect input for demonstration
old_input = input
def mock_input(prompt):
    print(prompt + "Alice Johnson")
    return "Alice Johnson"

input = mock_input
view_student_report()
input = old_input  # Restore original input

print("\n" + "="*60)
print("CONGRATULATIONS! 🎉")
print("="*60)
print("You've completed the Python Basics Tutorial!")
print("\nWhat you've learned:")
print("✓ Variables and data types")
print("✓ Strings and formatting")
print("✓ Numbers and math operations")
print("✓ Conditionals and logic")
print("✓ Loops and iteration")
print("✓ Lists and collections")
print("✓ Dictionaries")
print("✓ Functions")
print("✓ Building complete programs")

print("\nNext steps in your Python journey:")
print("1. Object-Oriented Programming (Classes and Objects)")
print("2. File handling and data persistence")
print("3. Error handling and debugging")
print("4. Working with external libraries")
print("5. Web development with frameworks like Flask or Django")
print("6. Data science with pandas and numpy")
print("7. GUI development with tkinter or PyQt")
print("8. API development and web scraping")

print("\nKeep practicing and building projects!")
print("The best way to learn programming is by doing. 🚀")

"""
Final Exercises - Build Your Own Projects:

1. Personal Finance Tracker:
   - Track income and expenses
   - Categorize transactions
   - Generate monthly reports
   - Calculate savings goals

2. Simple Library Management:
   - Add/remove books
   - Track borrowed books
   - Search functionality
   - Generate overdue reports

3. Weather Data Analyzer:
   - Store daily weather data
   - Calculate averages and trends
   - Find extreme weather days
   - Generate weather reports

4. Recipe Manager:
   - Store recipes with ingredients
   - Scale recipes up/down
   - Search by ingredient
   - Calculate nutritional info

5. Simple Game:
   - Number guessing game
   - Word guessing game
   - Simple quiz game
   - Rock, paper, scissors

6. Contact Manager:
   - Add/edit/delete contacts
   - Search contacts
   - Group contacts by category
   - Export contact lists

7. Inventory System:
   - Track products and quantities
   - Alert for low stock
   - Calculate inventory value
   - Generate reorder reports

8. Study Planner:
   - Track subjects and study time
   - Set study goals
   - Generate study schedules
   - Track progress

Remember: Start small, build incrementally, and don't be afraid to make mistakes!
Every error is a learning opportunity. Happy coding! 🐍✨
"""

# Uncomment the line below to run the interactive program
# main_program() 