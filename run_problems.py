import sys
from problem_manager import ProblemManager

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_problems.py <problem_number> [problem_number2 ...]")
        print("Example: python run_problems.py 1 2 3")
        return

    problem_manager = ProblemManager()
    
    for problem_number in sys.argv[1:]:
        try:
            problem_number = int(problem_number)
            print(f"\nRunning Problem {problem_number}...")
            
            # Load the solution code
            code = problem_manager.load_solution(problem_number)
            if not code:
                print(f"No solution found for Problem {problem_number}")
                continue
            
            # Run the solution
            result = problem_manager.run_solution(problem_number, code)
            
            if result["success"]:
                print(f"Result: {result['result']}")
                print(f"Execution Time: {result['execution_time']}")
            else:
                print(f"Error: {result['error']}")
                if "traceback" in result:
                    print(f"Traceback:\n{result['traceback']}")
                    
        except ValueError:
            print(f"Invalid problem number: {problem_number}")
        except Exception as e:
            print(f"Error running Problem {problem_number}: {str(e)}")

if __name__ == "__main__":
    main() 