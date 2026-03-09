import os
import json
import time
import traceback
import re
import shutil
from typing import Dict, List, Optional
from datetime import datetime

class ProblemManager:
    def __init__(self):
        self.problems_dir = "problems"
        self.solutions_dir = "solutions"
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        self.problem_files = {}
        self.solution_files = {}
        self.data_files = {}
        self.helpers_dir = "helpers"  # Single directory for all helper files
        self.problem_assignments_file = "problem_assignments.json"  # File to track which helpers are used by which problems
        self.progress_file = "progress.json"
        self.difficulty_file = os.path.join(self.problems_dir, "difficulty.json")
        
        # Track current problem mode (basic or max)
        self.current_mode = "basic"
        self.max_problem_limit = 945  # Maximum problem number for Max mode
        self.basic_problem_limit = 100  # Maximum problem number for Basic mode

        # Map of problems to their required data files and loading methods
        self.problem_data_files = {
            22: {'file': 'names.txt', 'method': 'load_names_data', 'description': 'List of names'},
            42: {'file': 'words.txt', 'method': 'load_words_data', 'description': 'List of words'},
            54: {'file': 'poker.txt', 'method': 'load_poker_data', 'description': 'Poker hands'},
            59: {'file': 'cipher.txt', 'method': 'load_cipher_data', 'description': 'Encrypted ASCII codes'},
            67: {'file': 'triangle.txt', 'method': 'load_triangle_data', 'description': 'Triangle of numbers'},
            79: {'file': 'keylog.txt', 'method': 'load_keylog_data', 'description': 'Login attempts'},
            81: {'file': 'matrix.txt', 'method': 'load_matrix_data', 'description': '80x80 matrix'},
            82: {'file': 'matrix.txt', 'method': 'load_matrix_data', 'description': '80x80 matrix'},
            83: {'file': 'matrix.txt', 'method': 'load_matrix_data', 'description': '80x80 matrix'},
            89: {'file': 'roman.txt', 'method': 'load_roman_data', 'description': 'Roman numerals'},
            96: {'file': 'sudoku.txt', 'method': 'load_sudoku_data', 'description': 'Sudoku puzzles'},
            98: {'file': 'words.txt', 'method': 'load_words_data', 'description': 'List of words'},
            99: {'file': 'base_exp.txt', 'method': 'load_base_exp_data', 'description': 'Base/exponent pairs'}
        }

        # Default difficulty ratings (1-5 stars) based on Project Euler's official difficulty levels
        self.default_difficulty_ratings = {
            1: 1,   # Multiples of 3 and 5
            2: 1,   # Even Fibonacci numbers
            3: 1,   # Largest prime factor
            4: 2,   # Largest palindrome product
            5: 2,   # Smallest multiple
            6: 2,   # Sum square difference
            7: 2,   # 10001st prime
            8: 2,   # Largest product in a series
            9: 2,   # Special Pythagorean triplet
            10: 2,  # Summation of primes
            11: 2,  # Largest product in a grid
            12: 3,  # Highly divisible triangular number
            13: 2,  # Large sum
            14: 3,  # Longest Collatz sequence
            15: 2,  # Lattice paths
            16: 2,  # Power digit sum
            17: 2,  # Number letter counts
            18: 2,  # Maximum path sum I
            19: 3,  # Counting Sundays
            20: 2,  # Factorial digit sum
            21: 3,  # Amicable numbers
            22: 2,  # Names scores
            23: 3,  # Non-abundant sums
            24: 3,  # Lexicographic permutations
            25: 2,  # 1000-digit Fibonacci number
            26: 4,  # Reciprocal cycles
            27: 3,  # Quadratic primes
            28: 3,  # Number spiral diagonals
            29: 2,  # Distinct powers
            30: 3,  # Digit fifth powers
            31: 2,  # Coin sums
            32: 3,  # Pandigital products
            33: 3,  # Digit cancelling fractions
            34: 3,  # Digit factorials
            35: 3,  # Circular primes
            36: 3,  # Double-base palindromes
            37: 4,  # Truncatable primes
            38: 3,  # Pandigital multiples
            39: 3,  # Integer right triangles
            40: 3,  # Champernowne's constant
            41: 3,  # Pandigital prime
            42: 2,  # Coded triangle numbers
            43: 3,  # Sub-string divisibility
            44: 4,  # Pentagon numbers
            45: 3,  # Triangular, pentagonal, and hexagonal
            46: 4,  # Goldbach's other conjecture
            47: 4,  # Distinct primes factors
            48: 2,  # Self powers
            49: 3,  # Prime permutations
            50: 4,  # Consecutive prime sum
            51: 4,  # Prime digit replacements
            52: 4,  # Permuted multiples
            53: 2,  # Combinatoric selections
            54: 3,  # Poker hands
            55: 4,  # Lychrel numbers
            56: 3,  # Powerful digit sum
            57: 4,  # Square root convergents
            58: 4,  # Spiral primes
            59: 3,  # XOR decryption
            60: 5,  # Prime pair sets
            61: 4,  # Cyclical figurate numbers
            62: 4,  # Cubic permutations
            63: 3,  # Powerful digit counts
            64: 4,  # Odd period square roots
            65: 3,  # Convergents of e
            66: 5,  # Diophantine equation
            67: 2,  # Maximum path sum II
            68: 4,  # Magic 5-gon ring
            69: 4,  # Totient maximum
            70: 4,  # Totient permutation
            71: 3,  # Ordered fractions
            72: 4,  # Counting fractions
            73: 4,  # Counting fractions in a range
            74: 4,  # Digit factorial chains
            75: 4,  # Singular integer right triangles
            76: 4,  # Counting summations
            77: 4,  # Prime summations
            78: 5,  # Coin partitions
            79: 3,  # Passcode derivation
            80: 4,  # Square root digital expansion
            81: 3,  # Path sum: two ways
            82: 4,  # Path sum: three ways
            83: 4,  # Path sum: four ways
            84: 4,  # Monopoly odds
            85: 4,  # Counting rectangles
            86: 5,  # Cuboid route
            87: 4,  # Prime power triples
            88: 5,  # Product-sum numbers
            89: 2,  # Roman numerals
            90: 4,  # Cube digit pairs
            91: 4,  # Right triangles with integer coordinates
            92: 4,  # Square digit chains
            93: 5,  # Arithmetic expressions
            94: 5,  # Almost equilateral triangles
            95: 5,  # Amicable chains
            96: 4,  # Su Doku
            97: 2,  # Large non-Mersenne prime
            98: 5,  # Anagramic squares
            99: 3,  # Largest exponential
            100: 5  # Arranged probability
        }

        # Default Project Euler difficulty percentages
        self.default_difficulty_percentages = {
            1: 5,   2: 10,  3: 15,  4: 20,  5: 25,  6: 20,  7: 25,  8: 25,  9: 30,  10: 30,
            11: 30, 12: 35, 13: 20, 14: 40, 15: 25, 16: 25, 17: 30, 18: 20, 19: 35, 20: 30,
            21: 35, 22: 20, 23: 40, 24: 35, 25: 25, 26: 45, 27: 40, 28: 35, 29: 30, 30: 35,
            31: 30, 32: 40, 33: 40, 34: 35, 35: 40, 36: 35, 37: 45, 38: 35, 39: 40, 40: 40,
            41: 40, 42: 25, 43: 40, 44: 45, 45: 35, 46: 45, 47: 45, 48: 30, 49: 40, 50: 50,
            51: 50, 52: 45, 53: 30, 54: 35, 55: 45, 56: 35, 57: 50, 58: 50, 59: 40, 60: 60,
            61: 50, 62: 50, 63: 40, 64: 50, 65: 40, 66: 60, 67: 20, 68: 50, 69: 50, 70: 55,
            71: 40, 72: 55, 73: 50, 74: 50, 75: 55, 76: 50, 77: 55, 78: 60, 79: 35, 80: 50,
            81: 40, 82: 50, 83: 50, 84: 50, 85: 45, 86: 60, 87: 50, 88: 65, 89: 25, 90: 55,
            91: 50, 92: 45, 93: 60, 94: 60, 95: 65, 96: 45, 97: 30, 98: 60, 99: 40, 100: 70
        }

        # Create directories if they don't exist
        os.makedirs(self.problems_dir, exist_ok=True)
        os.makedirs(self.solutions_dir, exist_ok=True)
        os.makedirs(self.helpers_dir, exist_ok=True)

        # Load or create difficulty data
        self.difficulty_data = self._load_difficulty_data()

        # Load or create problem assignments
        self.problem_assignments = self._load_problem_assignments()

        self._ensure_directories()
        self._load_progress()
        self.load_problem_files()
        self.load_solution_files()
        self.load_data_files()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        if not os.path.exists(self.progress_file):
            self._save_progress()

    def _load_progress(self):
        """Load user progress from JSON file."""
        try:
            with open(self.progress_file, 'r') as f:
                self.progress = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.progress = {
                "solved_problems": [],
                "attempted_problems": [],
                "last_attempted": None,
                "execution_times": {},
                "verified_problems": []  # Add verified problems list
            }
            self._save_progress()

    def _save_progress(self):
        """Save user progress to JSON file."""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=4)

    def get_problem(self, problem_number: int) -> str:
        """Load problem description and hints."""
        try:
            with open(f"{self.problems_dir}/problem_{problem_number}.txt", 'r') as f:
                content = f.read()
            return content
        except FileNotFoundError:
            return f"Problem {problem_number} not found."

    def save_solution(self, problem_number: int, code: str, execution_time=None) -> bool:
        """Save a solution for a problem."""
        try:
            filename = f"solution_{problem_number}.py"
            file_path = os.path.join(self.solutions_dir, filename)

            # Add execution time as a comment at the top of the file
            if execution_time is not None:
                code = f"# Execution time: {execution_time:.6f} seconds\n\n{code}"
                # Update progress with execution time
                self.progress["execution_times"][str(problem_number)] = execution_time
                self._save_progress()

            with open(file_path, 'w') as f:
                f.write(code)

            # Update progress
            self.progress["last_attempted"] = problem_number
            # Also ensure the problem is in the attempted_problems list
            if problem_number not in self.progress["attempted_problems"]:
                self.progress["attempted_problems"].append(problem_number)
            self._save_progress()

            return True
        except Exception as e:
            print(f"Error saving solution: {e}")
            return False

    def load_solution(self, problem_number: int) -> str:
        """Load a solution for a problem."""
        try:
            filename = f"solution_{problem_number}.py"
            file_path = os.path.join(self.solutions_dir, filename)

            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return f.read()
            return None
        except Exception as e:
            print(f"Error loading solution: {e}")
            return None

    def get_execution_time(self, problem_number: int) -> Optional[float]:
        """Get the execution time of a solution if it exists."""
        try:
            solution = self.load_solution(problem_number)
            if solution:
                # Extract execution time from the comment
                match = re.search(r"# Execution time: ([\d.]+) seconds", solution)
                if match:
                    return float(match.group(1))
            return None
        except Exception as e:
            print(f"Error getting execution time: {e}")
            return None

    def save_helper_file(self, filename, content):
        """Save a helper file."""
        try:
            file_path = os.path.join(self.helpers_dir, filename)
            with open(file_path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error saving helper file: {e}")
            return False

    def load_helper_files(self, problem_number):
        """Load helper files assigned to a problem."""
        helper_files = {}

        # Add recursion protection
        if hasattr(self, '_loading_helpers') and self._loading_helpers:
            return helper_files
            
        # Track that we're in the process of loading helpers
        try:
            self._loading_helpers = True
            
            # Get list of helper files assigned to this problem
            assigned_files = self.problem_assignments.get(str(problem_number), [])

            # Load each assigned file
            for filename in assigned_files:
                # Use explicit string concatenation instead of os.path.join to avoid recursion
                file_path = self.helpers_dir + os.sep + filename
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        helper_files[filename] = f.read()
        finally:
            # Reset the loading flag when done or if an exception occurs
            self._loading_helpers = False

        return helper_files

    def delete_helper_file(self, problem_number: int, filename: str) -> bool:
        """Delete a helper file."""
        try:
            file_path = os.path.join(self.helpers_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            print(f"Error deleting helper file: {e}")
        return False

    def test_helper_function(self, problem_number: int, function_name: str, *args, **kwargs) -> Dict:
        """Test a helper function with given arguments."""
        try:
            # Load all helper files
            helper_files = self.load_helper_files(problem_number)

            # Get any debug function from kwargs
            debug_function = kwargs.pop('debug_function', None)

            # Create a new namespace
            namespace = {}

            # Add debug function if provided
            if debug_function:
                namespace['debug'] = debug_function

            # Add problem manager
            namespace['problem_manager'] = self

            # Execute all helper files
            for filename, code in helper_files.items():
                exec(code, namespace)

            # Check if the function exists
            if function_name not in namespace:
                return {
                    "success": False,
                    "error": f"Function '{function_name}' not found in helper files"
                }

            # Test the function
            start_time = time.time()
            result = namespace[function_name](*args, **kwargs)
            execution_time = time.time() - start_time

            return {
                "success": True,
                "result": result,
                "execution_time": execution_time
            }
        except Exception as e:
            # Try to extract line number from traceback
            tb = traceback.extract_tb(e.__traceback__)
            if tb:
                line_number = tb[-1].lineno
            else:
                line_number = None

            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "line_number": line_number
            }

    def run_solution(self, problem_number: int, code: str, namespace=None) -> Dict:
        """Execute the user's code and return the result."""
        try:
            # Create a new namespace if one was not provided
            if namespace is None:
                namespace = {}

            # Add problem_manager to the namespace
            namespace['problem_manager'] = self

            # Load and execute all helper files
            helper_files = self.load_helper_files(problem_number)
            for filename, helper_code in helper_files.items():
                exec(helper_code, namespace)

            # Execute the main solution code
            exec(code, namespace)

            # The solution should define a function called 'solve'
            if 'solve' in namespace:
                start_time = time.time()
                result = namespace['solve']()
                execution_time = time.time() - start_time

                # Update progress
                if problem_number not in self.progress["attempted_problems"]:
                    self.progress["attempted_problems"].append(problem_number)
                self.progress["last_attempted"] = problem_number
                self._save_progress()

                return {
                    "success": True,
                    "result": result,
                    "execution_time": f"{execution_time:.4f} seconds"
                }
            else:
                return {
                    "success": False,
                    "error": "No 'solve' function found in the code."
                }
        except SyntaxError as e:
            # Extract line number from syntax error
            line_number = e.lineno
            return {
                "success": False,
                "error": str(e),
                "line_number": line_number,
                "traceback": traceback.format_exc()
            }
        except Exception as e:
            # Try to extract line number from traceback
            tb = traceback.extract_tb(e.__traceback__)
            if tb:
                line_number = tb[-1].lineno
            else:
                line_number = None
            return {
                "success": False,
                "error": str(e),
                "line_number": line_number,
                "traceback": traceback.format_exc()
            }

    def mark_problem_solved(self, problem_number: int):
        """Mark a problem as solved."""
        if problem_number not in self.progress["solved_problems"]:
            self.progress["solved_problems"].append(problem_number)
            self._save_progress()
            
    def mark_problem_verified(self, problem_number: int, execution_time: float = 0):
        """
        Mark a problem as verified with the correct answer.
        
        Args:
            problem_number: The problem number to mark as verified
            execution_time: The execution time of the solution
        """
        # Initialize verified_problems list if it doesn't exist (backward compatibility)
        if "verified_problems" not in self.progress:
            self.progress["verified_problems"] = []
            
        # Add to verified problems if not already verified
        if problem_number not in self.progress["verified_problems"]:
            self.progress["verified_problems"].append(problem_number)
            
        # Also mark it as solved if it's not already
        if problem_number not in self.progress["solved_problems"]:
            self.progress["solved_problems"].append(problem_number)
            
        # Update execution time
        if execution_time > 0:
            self.progress["execution_times"][str(problem_number)] = execution_time
            
        # Save the updated progress
        self._save_progress()
        
    def is_problem_verified(self, problem_number: int) -> bool:
        """Check if a problem has been verified with the correct answer."""
        # Ensure verified_problems list exists (backward compatibility)
        if "verified_problems" not in self.progress:
            self.progress["verified_problems"] = []
            self._save_progress()
            
        return problem_number in self.progress["verified_problems"]

    def get_progress(self) -> Dict:
        """Get the user's progress."""
        return {
            "solved_problems": self.progress["solved_problems"],
            "attempted_problems": self.progress["attempted_problems"],
            "verified_problems": self.progress.get("verified_problems", []),  # Add verified problems
            "last_attempted": self.progress["last_attempted"],
            "execution_times": self.progress["execution_times"]
        }

    def is_problem_solved(self, problem_number: int) -> bool:
        """Check if a problem has been solved."""
        return problem_number in self.progress["solved_problems"]

    def load_problem_files(self):
        """Load all problem files from the problems directory based on current mode."""
        self.problem_files = {}
        
        # Always scan all problem group directories
        for dirname in os.listdir(self.problems_dir):
            if re.match(r'\d+-\d+', dirname):
                subdir_path = os.path.join(self.problems_dir, dirname)
                if os.path.isdir(subdir_path):
                    # Check if this group is within our mode's problem limit
                    group_match = re.match(r'(\d+)-\d+', dirname)
                    if group_match:
                        group_start = int(group_match.group(1))
                        if self.current_mode == "basic" and group_start > 100:
                            # Skip groups beyond basic limit
                            continue
                            
                    # Load problem files from this directory
                    for filename in os.listdir(subdir_path):
                        if filename.endswith('.txt') and filename.startswith('problem_'):
                            file_path = os.path.join(subdir_path, filename)
                            self.problem_files[filename] = file_path
        
        # Also load from the root for backward compatibility (problems 1-100)
        for filename in os.listdir(self.problems_dir):
            if filename.endswith('.txt') and filename.startswith('problem_'):
                # Extract problem number
                match = re.match(r'problem_(\d+)\.txt', filename)
                if match:
                    problem_number = int(match.group(1))
                    # Only include if it's within the current mode's limit
                    if self.current_mode == "basic" and problem_number > 100:
                        continue
                        
                    # Add to problem files if not already loaded from subdirectory
                    if filename not in self.problem_files:
                        file_path = os.path.join(self.problems_dir, filename)
                        self.problem_files[filename] = file_path

    def load_solution_files(self):
        """Load all solution files from the solutions directory."""
        for filename in os.listdir(self.solutions_dir):
            if filename.endswith('.py'):
                file_path = os.path.join(self.solutions_dir, filename)
                self.solution_files[filename] = file_path

    def load_data_files(self):
        """Load all data files from the data directory."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"Created data directory at {self.data_dir}")
            return

        for filename in os.listdir(self.data_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.data_dir, filename)
                self.data_files[filename] = file_path

    def get_data_file(self, filename):
        """Get the path to a specific data file."""
        if filename in self.data_files:
            return self.data_files[filename]
        return None

    def check_data_file(self, filename):
        """Check if a data file exists and return its status."""
        file_path = self.get_data_file(filename)
        if not file_path:
            return {
                'exists': False,
                'message': f"Required data file '{filename}' is missing.",
                'download_url': f"https://projecteuler.net/problem={self._get_problem_for_file(filename)}"
            }

        if not os.path.exists(file_path):
            return {
                'exists': False,
                'message': f"Required data file '{filename}' was not found at {file_path}.",
                'download_url': f"https://projecteuler.net/problem={self._get_problem_for_file(filename)}"
            }

        return {'exists': True, 'file_path': file_path}

    def _get_problem_for_file(self, filename):
        """Get the problem number that uses a specific data file."""
        for problem, info in self.problem_data_files.items():
            if info['file'] == filename:
                return problem
        return None

    def load_triangle_data(self, filename='triangle.txt'):
        """Load triangle data for Problem 67."""
        status = self.check_data_file(filename)
        if not status['exists']:
            raise FileNotFoundError(status['message'])

        try:
            with open(status['file_path'], 'r') as f:
                return [[int(num) for num in line.strip().split()]
                       for line in f.readlines()]
        except Exception as e:
            raise Exception(f"Error loading triangle data: {str(e)}")

    def load_sudoku_data(self, filename='sudoku.txt'):
        """Load Sudoku puzzles for Problem 96."""
        status = self.check_data_file(filename)
        if not status['exists']:
            raise FileNotFoundError(status['message'])

        try:
            with open(status['file_path'], 'r') as f:
                puzzles = []
                current_puzzle = []
                for line in f:
                    if line.startswith('Grid'):
                        if current_puzzle:
                            puzzles.append(current_puzzle)
                        current_puzzle = []
                    else:
                        current_puzzle.append([int(c) for c in line.strip()])
                if current_puzzle:
                    puzzles.append(current_puzzle)
            return puzzles
        except Exception as e:
            raise Exception(f"Error loading Sudoku data: {str(e)}")

    def load_words_data(self, filename='words.txt'):
        """Load words data for Problems 42 and 98."""
        status = self.check_data_file(filename)
        if not status['exists']:
            raise FileNotFoundError(status['message'])

        try:
            with open(status['file_path'], 'r') as f:
                return [word.strip('"') for word in f.read().split(',')]
        except Exception as e:
            raise Exception(f"Error loading words data: {str(e)}")

    def load_base_exp_data(self, filename='base_exp.txt'):
        """Load base/exponent pairs data for Problem 99."""
        status = self.check_data_file(filename)
        if not status['exists']:
            raise FileNotFoundError(status['message'])

        try:
            with open(status['file_path'], 'r') as f:
                return [tuple(map(int, line.strip().split(',')))
                       for line in f.readlines()]
        except Exception as e:
            raise Exception(f"Error loading base/exponent data: {str(e)}")

    def load_names_data(self, filename='names.txt'):
        """Load names data for Problem 22."""
        status = self.check_data_file(filename)
        if not status['exists']:
            raise FileNotFoundError(status['message'])

        try:
            with open(status['file_path'], 'r') as f:
                return [name.strip('"') for name in f.read().split(',')]
        except Exception as e:
            raise Exception(f"Error loading names data: {str(e)}")

    def load_poker_data(self, filename='poker.txt'):
        """Load poker hands data for Problem 54."""
        status = self.check_data_file(filename)
        if not status['exists']:
            raise FileNotFoundError(status['message'])

        try:
            with open(status['file_path'], 'r') as f:
                return [tuple(line.strip().split()[:5]) for line in f.readlines()]
        except Exception as e:
            raise Exception(f"Error loading poker data: {str(e)}")

    def load_cipher_data(self, filename='cipher.txt'):
        """Load cipher data for Problem 59."""
        status = self.check_data_file(filename)
        if not status['exists']:
            raise FileNotFoundError(status['message'])

        try:
            with open(status['file_path'], 'r') as f:
                return [int(num) for num in f.read().split(',')]
        except Exception as e:
            raise Exception(f"Error loading cipher data: {str(e)}")

    def load_keylog_data(self, filename='keylog.txt'):
        """Load keylog data for Problem 79."""
        status = self.check_data_file(filename)
        if not status['exists']:
            raise FileNotFoundError(status['message'])

        try:
            with open(status['file_path'], 'r') as f:
                return [line.strip() for line in f.readlines()]
        except Exception as e:
            raise Exception(f"Error loading keylog data: {str(e)}")

    def load_matrix_data(self, filename='matrix.txt'):
        """Load matrix data for Problems 81, 82, and 83."""
        status = self.check_data_file(filename)
        if not status['exists']:
            raise FileNotFoundError(status['message'])

        try:
            with open(status['file_path'], 'r') as f:
                return [[int(num) for num in line.strip().split(',')]
                       for line in f.readlines()]
        except Exception as e:
            raise Exception(f"Error loading matrix data: {str(e)}")

    def load_roman_data(self, filename='roman.txt'):
        """Load Roman numerals data for Problem 89."""
        status = self.check_data_file(filename)
        if not status['exists']:
            raise FileNotFoundError(status['message'])

        try:
            with open(status['file_path'], 'r') as f:
                return [line.strip() for line in f.readlines()]
        except Exception as e:
            raise Exception(f"Error loading Roman numerals data: {str(e)}")

    def load_problem(self, problem_number):
        """Load problem text from file."""
        try:
            # Enforce problem limits based on mode
            if self.current_mode == "basic" and problem_number > self.basic_problem_limit:
                return {
                    "text": f"Problem {problem_number} not available in Basic mode. Switch to Max mode to access all problems.",
                    "hints": ""
                }
                
            # Determine file path based on problem number
            file_path = None
            found = False
            
            # All problems should be in subdirectories by group
            group_start = ((problem_number - 1) // 100) * 100 + 1
            group_end = group_start + 99
            group_dir = f"{self.problems_dir}/{group_start}-{group_end}"
            
            # First try to load from the appropriate subdirectory
            subdir_path = f"{group_dir}/problem_{problem_number}.txt"
            if os.path.exists(subdir_path):
                file_path = subdir_path
                found = True
            
            # For problems 1-100, try the root directory as fallback (backward compatibility)
            if not found and problem_number <= 100:
                root_path = f"{self.problems_dir}/problem_{problem_number}.txt"
                if os.path.exists(root_path):
                    file_path = root_path
                    found = True
            
            if not found:
                return {
                    "text": f"Problem {problem_number} not found.",
                    "hints": ""
                }
            
            with open(file_path, "r") as f:
                content = f.read()

                # Split content into problem text and hints
                parts = content.split("\nHints:")
                problem_text = parts[0].strip()
                hints = parts[1].strip() if len(parts) > 1 else ""

                return {
                    "text": problem_text,
                    "hints": hints
                }
        except FileNotFoundError:
            return {
                "text": f"Problem {problem_number} not found.",
                "hints": ""
            }

    def get_problem_data_info(self, problem_number):
        """Get information about data files required for a problem."""
        if problem_number in self.problem_data_files:
            info = self.problem_data_files[problem_number]
            return {
                'has_data': True,
                'file': info['file'],
                'method': info['method'],
                'description': info['description'],
                'example': self._get_data_example(problem_number)
            }
        return {'has_data': False}

    def _get_data_example(self, problem_number):
        """Get example code for loading and using the data file."""
        if problem_number not in self.problem_data_files:
            return None

        info = self.problem_data_files[problem_number]
        method = info['method']

        examples = {
            'load_triangle_data': """
# Load the triangle data
triangle = problem_manager.load_triangle_data()

# The data is returned as a list of lists
# Each inner list represents a row of the triangle
# Example: [[3], [7, 4], [2, 4, 6], ...]
""",
            'load_names_data': """
# Load the names data
names = problem_manager.load_names_data()

# The data is returned as a list of strings
# Example: ['MARY', 'PATRICIA', 'LINDA', ...]
""",
            'load_words_data': """
# Load the words data
words = problem_manager.load_words_data()

# The data is returned as a list of strings
# Example: ['A', 'ABILITY', 'ABLE', ...]
""",
            'load_poker_data': """
# Load the poker hands data
hands = problem_manager.load_poker_data()

# The data is returned as a list of tuples
# Each tuple contains two lists of cards
# Example: [('8C TS KC 9H 4S', '7D 2S 5D 3S AC'), ...]
""",
            'load_cipher_data': """
# Load the cipher data
cipher = problem_manager.load_cipher_data()

# The data is returned as a list of integers
# Each integer represents an ASCII code
# Example: [79, 59, 12, ...]
""",
            'load_keylog_data': """
# Load the keylog data
attempts = problem_manager.load_keylog_data()

# The data is returned as a list of strings
# Each string represents a login attempt
# Example: ['319', '680', '180', ...]
""",
            'load_matrix_data': """
# Load the matrix data
matrix = problem_manager.load_matrix_data()

# The data is returned as a 2D list of integers
# Example: [[131, 673, 234, 103, 18], ...]
""",
            'load_roman_data': """
# Load the Roman numerals data
romans = problem_manager.load_roman_data()

# The data is returned as a list of strings
# Each string is a valid Roman numeral
# Example: ['I', 'II', 'III', ...]
""",
            'load_sudoku_data': """
# Load the Sudoku puzzles data
puzzles = problem_manager.load_sudoku_data()

# The data is returned as a list of 9x9 grids
# Each grid is a list of lists of integers
# Example: [[[0, 0, 3, 0, 2, 0, 6, 0, 0], ...], ...]
""",
            'load_base_exp_data': """
# Load the base/exponent pairs data
pairs = problem_manager.load_base_exp_data()

# The data is returned as a list of tuples
# Each tuple contains (base, exponent)
# Example: [(519432, 525806), (632382, 518061), ...]
"""
        }

        return examples.get(method)

    def _load_problem_assignments(self):
        """Load helper file assignments for problems."""
        assignments_file = os.path.join(self.helpers_dir, self.problem_assignments_file)
        if os.path.exists(assignments_file):
            with open(assignments_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_problem_assignments(self):
        """Save helper file assignments for problems."""
        assignments_file = os.path.join(self.helpers_dir, self.problem_assignments_file)
        with open(assignments_file, 'w') as f:
            json.dump(self.problem_assignments, f)

    def get_available_helper_files(self):
        """Get list of all available helper files."""
        if not os.path.exists(self.helpers_dir):
            return []
        return [f for f in os.listdir(self.helpers_dir) if f.endswith('.py') and f != self.problem_assignments_file]

    def assign_helper_to_problem(self, problem_number, filename):
        """Assign a helper file to a problem."""
        try:
            # Check if file exists
            file_path = os.path.join(self.helpers_dir, filename)
            if not os.path.exists(file_path):
                return False

            # Update assignments
            if str(problem_number) not in self.problem_assignments:
                self.problem_assignments[str(problem_number)] = []
            if filename not in self.problem_assignments[str(problem_number)]:
                self.problem_assignments[str(problem_number)].append(filename)
                self._save_problem_assignments()

            return True
        except Exception as e:
            print(f"Error assigning helper file: {e}")
            return False

    def unassign_helper_from_problem(self, problem_number, filename):
        """Remove a helper file assignment from a problem."""
        try:
            # Update assignments
            if str(problem_number) in self.problem_assignments:
                if filename in self.problem_assignments[str(problem_number)]:
                    self.problem_assignments[str(problem_number)].remove(filename)
                    self._save_problem_assignments()

            return True
        except Exception as e:
            print(f"Error unassigning helper file: {e}")
            return False

    def has_info_file(self, problem_number):
        """
        Check if a problem has an additional info file.

        Args:
            problem_number: The problem number to check

        Returns:
            True if an info file exists, False otherwise
        """
        info_path = os.path.join("info", f"{problem_number:03d}_overview.pdf")
        return os.path.exists(info_path)

    def get_problem_description(self, problem_number):
        """
        Get the description for a problem.

        Args:
            problem_number: The problem number to get the description for

        Returns:
            The problem description with info file notification if available
        """
        description = self.problems.get(problem_number, {}).get('description', '')

        # Check for info file
        if self.has_info_file(problem_number):
            description += "\n\n[Additional information available in the Info tab]"

        return description

    def load_data_file_preview(self, filename, max_lines=20):
        """Load a preview of the data file contents."""
        status = self.check_data_file(filename)
        if not status['exists']:
            return f"Error: {status['message']}"

        try:
            with open(status['file_path'], 'r') as f:
                lines = f.readlines()
                if len(lines) > max_lines:
                    preview = ''.join(lines[:max_lines])
                    preview += f"\n... (showing first {max_lines} lines of {len(lines)} total)"
                else:
                    preview = ''.join(lines)
                return preview
        except Exception as e:
            return f"Error loading data preview: {str(e)}"

    def get_problem_difficulty(self, problem_number):
        """Get the difficulty rating for a problem."""
        # First check the difficulty data
        if str(problem_number) in self.difficulty_data["ratings"]:
            return self.difficulty_data["ratings"][str(problem_number)]

        # Then check the default ratings
        if problem_number in self.default_difficulty_ratings:
            return self.default_difficulty_ratings[problem_number]

        # If no rating is found, return 3 as a default
        return 3

    def get_problem_difficulty_percentage(self, problem_number):
        """Get the Project Euler difficulty percentage for a problem."""
        # First check the difficulty data
        if str(problem_number) in self.difficulty_data["percentages"]:
            return self.difficulty_data["percentages"][str(problem_number)]

        # If no percentage is found, return the default percentage
        return self.default_difficulty_percentages.get(problem_number, 15)

    def update_problem_difficulty(self, problem_number, rating, percentage):
        """Update the difficulty rating and percentage for a problem."""
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if not (0 <= percentage <= 100):
            raise ValueError("Percentage must be between 0 and 100")

        self.difficulty_data["ratings"][problem_number] = rating
        self.difficulty_data["percentages"][problem_number] = percentage
        self.difficulty_data["last_updated"] = datetime.now().isoformat()
        self._save_difficulty_data(self.difficulty_data)

    def get_all_difficulties(self):
        """Get all difficulty ratings."""
        return self.difficulty_data["ratings"]

    def _load_difficulty_data(self):
        """Load difficulty data from JSON file or create default data."""
        try:
            if os.path.exists(self.difficulty_file):
                with open(self.difficulty_file, 'r') as f:
                    data = json.load(f)
                    # Ensure the data has the required structure
                    if "ratings" not in data:
                        data["ratings"] = {}
                    if "percentages" not in data:
                        data["percentages"] = {}
                    return data
        except Exception as e:
            print(f"Error loading difficulty data: {e}")

        # Create default data structure
        return {
            "ratings": self.default_difficulty_ratings.copy(),
            "percentages": self.default_difficulty_percentages.copy()
        }

    def _save_difficulty_data(self, data):
        """Save difficulty data to JSON file."""
        try:
            with open(self.difficulty_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving difficulty data: {e}")

    def set_problem_mode(self, mode):
        """
        Set the problem mode (basic or max) and reload problem files.
        
        Args:
            mode: The mode to set ('basic' or 'max')
        """
        if mode not in ['basic', 'max']:
            return
            
        self.current_mode = mode
        
        # Reload problem files
        self.load_problem_files()
        
        # Update metadata
        print(f"Problem mode set to {mode.upper()}: " + 
              f"Problems 1-{self.basic_problem_limit if mode == 'basic' else self.max_problem_limit} available")