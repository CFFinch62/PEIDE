"""
Run Manager module for Project Euler Editor.
Handles execution of solutions and helper functions.
"""
import os
import sys
import io
import time
import tempfile
import traceback
from contextlib import redirect_stdout, redirect_stderr
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
import subprocess
import re
import hashlib
import pickle
import hmac


class RunManager:
    """
    Manages code execution for solutions and helper functions.
    Handles setup of execution environment, output capture, and error handling.
    """

    def __init__(self, problem_manager, debug_panel, ui_components):
        """
        Initialize the Run Manager.

        Args:
            problem_manager: The problem manager instance
            debug_panel: The debug panel for logging output
            ui_components: Dictionary containing UI components needed for execution:
                - status_bar: Status bar for showing execution status
                - progress_bar: Progress bar for showing execution progress
                - execution_time_label: Label for showing execution time
                - code_editor: Code editor for highlighting errors in solution code
                - helpers_editor: Editor for helper files (for highlighting errors)
                - tab_widget: Tab widget for switching to debug tab
        """
        self.problem_manager = problem_manager
        self.debug_panel = debug_panel
        self.ui = ui_components
        # Key used for answer verification (could be loaded from a separate config)
        self._verification_key = b'ProjectEulerVerificationKey'
        # Path to the answers file
        self._answers_file = os.path.join('answers', 'pe_answers.bin')

    def run_solution(self, problem_number, code):
        """Run the solution and return the result."""
        # Prepare UI for execution (including clearing debug output)
        self._prepare_ui_for_execution()

        # Create a result dictionary
        result = {
            "success": False,
            "result": None,
            "execution_time": 0,
            "error": None,
            "line_number": None
        }

        # Check if code is empty
        if not code or not code.strip():
            result["error"] = "No code to run"
            return result

        # Check for solve function
        if "def solve(" not in code:
            result["error"] = "No solve() function found"
            return result

        # Temporary file path for the Python script
        temp_file_path = None

        try:
            # Create a temporary file for execution
            with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w', encoding='utf-8') as temp_file:
                temp_file_path = temp_file.name

                # Write problem manager import and debug function
                output_file_path = os.path.join('/tmp', f'pe_output_{os.getpid()}.txt')
                preamble_code = f"""
import sys
import os
import time
from pathlib import Path
sys.path.append('{os.getcwd().replace("'", "\\'")}')
from problem_manager import ProblemManager

# Create an instance of ProblemManager
problem_manager = ProblemManager()

# Store the problem number for reference
problem_number = {problem_number}

_debug_output = []

def debug(message, level="debug"):
    # Print debug message with the specified level
    _debug_output.append({{"message": str(message), "level": level}})
    print(f"DEBUG[{{level}}]: {{message}}", flush=True)  # Also print to stdout for diagnostic

"""
                temp_file.write(preamble_code)

                # Calculate the line offset for error reporting
                # Count the number of lines in the preamble (including the leading newline)
                preamble_lines = len(preamble_code.split('\n')) - 1  # -1 because split creates an extra empty element

                # Write the user's code
                temp_file.write(code)

                # Add code to call solve() and time it
                temp_file.write(f"""

if __name__ == "__main__":
    # Ensure output is not buffered
    import sys
    import os

    # Force unbuffered output
    sys.stdout.reconfigure(write_through=True) if hasattr(sys.stdout, 'reconfigure') else None

    # Also write to a file for backup
    output_file = "{output_file_path}"
    try:
        with open(output_file, 'w') as f:
            f.write("Starting execution\\n")
    except Exception as e:
        print(f"Failed to create output file: {{e}}", flush=True)

    # Try to solve the problem
    try:
        # Print a marker to verify script is running
        print("EXECUTION_STARTED", flush=True)
        try:
            with open(output_file, 'a') as f:
                f.write("EXECUTION_STARTED\\n")
        except Exception as e:
            print(f"Failed to write to output file: {{e}}", flush=True)

        # Make sure solve function exists
        if 'solve' not in globals():
            print("Error: No solve() function defined in the code.", flush=True)
            sys.exit(1)

        print("Calling solve() function...", flush=True)
        start_time = time.time()

        # Call solve
        answer = solve()

        # Measure execution time
        execution_time = time.time() - start_time

        # Print the result
        print(f"Result: {{answer}}", flush=True)
        print(f"Execution time: {{execution_time:.6f}} seconds", flush=True)
        print("DEBUG_OUTPUT_START", flush=True)
        for item in _debug_output:
            print(f"{{item['level']}}:{{item['message']}}", flush=True)
        print("DEBUG_OUTPUT_END", flush=True)
        print("EXECUTION_COMPLETED", flush=True)

        # Also write to file
        try:
            with open(output_file, 'a') as f:
                f.write(f"Result: {{answer}}\\n")
                f.write(f"Execution time: {{execution_time:.6f}} seconds\\n")
                f.write("EXECUTION_COMPLETED\\n")
        except Exception as e:
            print(f"Failed to write results to output file: {{e}}", flush=True)

        # Exit with success code
        sys.exit(0)
    except Exception as e:
        import traceback
        tb = traceback.extract_tb(sys.exc_info()[2])
        print(f"Error: {{str(e)}}", flush=True)
        # Adjust line number to account for preamble code
        actual_line = tb[-1].lineno - {preamble_lines}
        # Ensure line number is valid (positive)
        if actual_line < 1:
            actual_line = 1
        print(f"Line: {{actual_line}}", flush=True)
        print(f"Traceback: {{traceback.format_exc()}}", flush=True)

        # Also write to file
        try:
            with open(output_file, 'a') as f:
                f.write(f"Error: {{str(e)}}\\n")
                f.write(f"Line: {{actual_line}}\\n")
                f.write(f"Traceback: {{traceback.format_exc()}}\\n")
        except Exception as ex:
            print(f"Failed to write error to output file: {{ex}}", flush=True)

        sys.exit(1)
""")

                # Add an additional check for data files
                temp_file.write(f"""
    # Check if this problem requires any data files
    problem_data_info = problem_manager.get_problem_data_info(problem_number)
    if problem_data_info and problem_data_info.get('has_data', False):
        data_file = problem_data_info.get('file')
        data_check = problem_manager.check_data_file(data_file)
        if not data_check['exists']:
            print(f"WARNING: This problem requires a data file: {{data_file}}")
            print(f"You can download it from: https://projecteuler.net/problem={{problem_number}}")

    """)

            # Run the solution using direct subprocess call
            python_path = "python3"  # Use system Python instead of sys.executable
            cmd = f"{python_path} -u {temp_file_path} > {output_file_path}.out 2> {output_file_path}.err"
            exit_code = os.system(cmd)

            # Read the output from files
            stdout = ""
            stderr = ""

            # Check if output files exist
            out_file = f"{output_file_path}.out"
            err_file = f"{output_file_path}.err"

            try:
                if os.path.exists(out_file):
                    with open(out_file, "r") as f:
                        stdout = f.read()

                if os.path.exists(err_file):
                    with open(err_file, "r") as f:
                        stderr = f.read()

                    # If there's stderr output but no stdout, something is wrong
                    if len(stderr) > 0 and len(stdout) == 0:
                        # Extract any error message if possible
                        error_match = re.search(r"Error: (.*?)$", stderr, re.MULTILINE)
                        if error_match:
                            result["error"] = f"Script error: {error_match.group(1).strip()}"
                        else:
                            result["error"] = f"Script failed with error: {stderr.strip()}"
                        return result
            except Exception as e:
                result["error"] = f"Error reading output files: {str(e)}"
                return result

            # Check if execution started marker is present
            if "EXECUTION_STARTED" not in stdout:
                # Check if there's a backup output file we can read
                output_file = os.path.join('/tmp', f'pe_output_{os.getpid()}.txt')

                if os.path.exists(output_file):
                    try:
                        with open(output_file, 'r') as f:
                            backup_output = f.read()

                        # If we found output in the backup file, use that instead
                        if "EXECUTION_STARTED" in backup_output:
                            stdout = backup_output
                        else:
                            result["error"] = "Script did not execute correctly"
                            return result
                    except Exception as e:
                        result["error"] = "Script did not execute correctly"
                        return result
                else:
                    result["error"] = "Script did not execute correctly"
                    return result

            # Check if the solution ran successfully
            if exit_code == 0:
                # Extract result and execution time using more flexible patterns
                result_match = re.search(r"Result: (.*?)$", stdout, re.MULTILINE)
                time_match = re.search(r"Execution time: ([\d.]+) seconds", stdout, re.MULTILINE)

                if result_match and time_match:
                    # Extract result
                    result_str = result_match.group(1).strip()
                    result["result"] = result_str

                    # Extract execution time
                    execution_time = float(time_match.group(1))
                    result["execution_time"] = execution_time

                    # Check if execution time is too long (> 60 seconds)
                    if execution_time > 60:
                        result["warning"] = "Long execution time"

                    # Extract debug output
                    self._extract_debug_output(stdout)

                    # Mark success
                    result["success"] = True
                else:
                    result["error"] = "Failed to extract result or execution time"
            else:
                # Extract error message
                error_match = re.search(r"Error: (.*?)$", stdout, re.MULTILINE)
                line_match = re.search(r"Line: (\d+)", stdout, re.MULTILINE)

                if error_match:
                    error_message = error_match.group(1).strip()

                    # Check if this is a missing data file error
                    if "No such file or directory" in error_message and "data/" in error_message:
                        data_file_match = re.search(r"'(data/.*?)'", error_message)
                        if data_file_match:
                            data_file = data_file_match.group(1)
                            result["error"] = f"Missing data file: {data_file}"
                            result["is_missing_data"] = True

                            # Get the Project Euler problem URL
                            result["download_url"] = f"https://projecteuler.net/problem={problem_number}"
                    else:
                        result["error"] = error_message
                else:
                    result["error"] = stderr or stdout or "Unknown error"

                # Extract line number if available
                if line_match:
                    line_number = int(line_match.group(1))
                    # The line number is already adjusted in the temp file output
                    # so we can use it directly, but ensure it's valid
                    if line_number > 0:
                        result["line_number"] = line_number

        except Exception as e:
            result["error"] = f"Error setting up execution: {str(e)}"
        finally:
            # Clean up temporary file and output files
            try:
                if temp_file_path and os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

                # Clean up any output files
                for suffix in ['.out', '.err']:
                    try:
                        if os.path.exists(f"{output_file_path}{suffix}"):
                            os.unlink(f"{output_file_path}{suffix}")
                    except:
                        pass
            except Exception:
                pass

            # Reset UI after execution
            self._reset_ui_after_execution()

        return result

    def test_helper_function(self, problem_number, function_name, args, kwargs):
        """
        Test a helper function with the given arguments.

        Args:
            problem_number: The problem number
            function_name: The name of the function to test
            args: Positional arguments for the function
            kwargs: Keyword arguments for the function

        Returns:
            dict: Result information with success/failure details
        """
        # Clear any previous error highlights
        self.ui['helpers_editor'].clear_error_highlights()

        # Clear debug output if debug is enabled
        if self.debug_panel.is_debug_enabled():
            self.debug_panel.clear_debug_output()
            self._log_debug("Starting helper function test...", "info")
            # Switch to debug tab
            self.ui['tab_widget'].setCurrentIndex(4)  # Index of debug tab

        # Create capture buffers for stdout/stderr
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()

        # Get debug function
        debug_function = self.debug_panel.get_debug_function()

        # Add debug function to kwargs if debug is enabled
        if self.debug_panel.is_debug_enabled() and 'debug_function' not in kwargs:
            kwargs['debug_function'] = debug_function

        # Test the function with output capture
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            result = self.problem_manager.test_helper_function(
                problem_number, function_name, *args, **kwargs)

        # Process output
        self._process_execution_output(stdout_buffer.getvalue(), stderr_buffer.getvalue())

        # Process result
        if result["success"]:
            execution_time = result["execution_time"]
            self._log_debug(f"Function executed successfully in {execution_time:.6f} seconds", "info")
            self._log_debug(f"Result: {result['result']}", "important")

            return {
                "success": True,
                "result": result['result'],
                "execution_time": execution_time
            }
        else:
            self._log_debug(f"Error: {result['error']}", "error")

            if 'traceback' in result:
                self._log_debug("Traceback:", "error")
                for line in result['traceback'].splitlines():
                    self._log_debug(f"    {line}", "error")

            # If we have line number information, highlight the error line
            if 'line_number' in result and result['line_number'] is not None:
                self.ui['helpers_editor'].highlight_error_line(
                    result['line_number'], result['error'])
                self._log_debug(f"Error at line {result['line_number']}", "error")

            return {
                "success": False,
                "error": result['error'],
                "traceback": result.get('traceback', ''),
                "line_number": result.get('line_number')
            }

    def _prepare_ui_for_execution(self):
        """Prepare UI components for code execution."""
        # Show progress indicators
        self.ui['progress_bar'].setVisible(True)
        self.ui['progress_bar'].setRange(0, 0)  # Indeterminate progress
        self.ui['execution_time_label'].setVisible(True)

        # Check if the main window has a styled status message method
        if hasattr(self.ui['status_bar'].parent(), 'show_status_message'):
            self.ui['status_bar'].parent().show_status_message("Initializing execution...")
        else:
            self.ui['status_bar'].showMessage("Initializing execution...")

        # Clear debug output if debug is enabled
        if self.debug_panel.is_debug_enabled():
            self.debug_panel.clear_debug_output()
            self._log_debug("Starting code execution...", "info")
            # Switch to debug tab
            self.ui['tab_widget'].setCurrentIndex(4)  # Index of debug tab

    def _reset_ui_after_execution(self):
        """Reset UI components after code execution."""
        self.ui['progress_bar'].setVisible(False)
        self.ui['execution_time_label'].setVisible(False)

        # Check if the main window has a styled status message method
        if hasattr(self.ui['status_bar'].parent(), 'show_status_message'):
            self.ui['status_bar'].parent().show_status_message("Ready")
        else:
            self.ui['status_bar'].showMessage("Ready")

    def _process_execution_output(self, stdout_output, stderr_output):
        """
        Process captured stdout and stderr output.

        Args:
            stdout_output: Captured standard output
            stderr_output: Captured standard error
        """
        # Display stdout if there is any
        if stdout_output and self.debug_panel.is_debug_enabled():
            self._log_debug("Standard output:", "info")
            for line in stdout_output.splitlines():
                self._log_debug(f"    {line}")

        # Display stderr if there is any
        if stderr_output and self.debug_panel.is_debug_enabled():
            self._log_debug("Standard error:", "error")
            for line in stderr_output.splitlines():
                self._log_debug(f"    {line}", "error")

    def _log_debug(self, message, level="debug"):
        """
        Log a debug message if debug panel is available.

        Args:
            message: The message to log
            level: Debug level ("debug", "info", "error", "important", etc.)
        """
        if self.debug_panel:
            self.debug_panel.add_debug_message(message, level)

    def _extract_debug_output(self, stdout):
        """Extract debug output from the solution's stdout."""
        # Find debug output section
        start_marker = "DEBUG_OUTPUT_START"
        end_marker = "DEBUG_OUTPUT_END"

        start_idx = stdout.find(start_marker)
        end_idx = stdout.find(end_marker)

        if start_idx != -1 and end_idx != -1:
            # Extract debug lines
            debug_section = stdout[start_idx + len(start_marker):end_idx].strip()
            debug_lines = debug_section.split('\n')

            # Process each debug line
            for line in debug_lines:
                if not line.strip():
                    continue

                # Parse level and message
                parts = line.split(':', 1)
                if len(parts) == 2:
                    level, message = parts
                    # Add to debug panel
                    self._log_debug(message.strip(), level.strip())
                else:
                    # No level specified, use default
                    self._log_debug(line.strip(), "debug")

        # Also look for direct DEBUG output from print statements
        debug_pattern = r"DEBUG\[(.*?)\]:(.*?)$"
        for match in re.finditer(debug_pattern, stdout, re.MULTILINE):
            if match:
                level = match.group(1).strip()
                message = match.group(2).strip()
                self._log_debug(message, level)

    def verify_solution(self, problem_number, result):
        """
        Verify if the solution result matches the correct answer.

        Args:
            problem_number: The problem number to verify
            result: The result from running the solution

        Returns:
            dict: Verification result with keys:
                - verified: Boolean indicating if the solution is correct
                - message: A message describing the verification result
        """
        verification_result = {
            "verified": False,
            "message": "Unable to verify solution."
        }

        # Log the attempt
        self._log_debug(f"Verifying solution for problem {problem_number}...", "info")

        # Check if result was successful
        if not result.get("success", False) or result.get("error"):
            verification_result["message"] = "Solution execution failed. Cannot verify."
            return verification_result

        try:
            # Check if answers file exists
            if not os.path.exists(self._answers_file):
                verification_result["message"] = "Answers database not found."
                return verification_result

            # Read the answers file
            with open(self._answers_file, 'rb') as f:
                encrypted_data = f.read()

            # Extract the hmac signature and the encrypted data
            signature = encrypted_data[:32]  # First 32 bytes are the HMAC-SHA256
            data = encrypted_data[32:]

            # Verify the signature
            expected_signature = hmac.new(self._verification_key, data, hashlib.sha256).digest()
            if not hmac.compare_digest(signature, expected_signature):
                verification_result["message"] = "Answers database integrity check failed."
                return verification_result

            # Decode the answers
            try:
                # Simple XOR decryption with the key
                decrypted_data = bytearray()
                key_bytes = bytearray(self._verification_key)
                for i, byte in enumerate(data):
                    decrypted_data.append(byte ^ key_bytes[i % len(key_bytes)])

                # Unpickle the answers
                answers = pickle.loads(bytes(decrypted_data))

                # Check if the problem number exists in the answers
                if str(problem_number) not in answers:
                    verification_result["message"] = f"No answer available for Problem {problem_number}."
                    return verification_result

                # Get the correct answer for this problem
                correct_answer = answers[str(problem_number)]

                # Convert result to string for comparison (if not already)
                user_answer = str(result.get("result", "")).strip()

                # Compare the answers
                if user_answer == str(correct_answer).strip():
                    verification_result["verified"] = True
                    verification_result["message"] = "Correct answer! Solution verified."

                    # Update progress through the problem manager
                    self.problem_manager.mark_problem_verified(problem_number,
                                                             result.get("execution_time", 0))
                else:
                    verification_result["message"] = "Incorrect answer. Try again."
            except (pickle.PickleError, Exception) as e:
                verification_result["message"] = f"Error decoding answers: {str(e)}"
        except Exception as e:
            verification_result["message"] = f"Verification error: {str(e)}"
            self._log_debug(f"Verification error: {traceback.format_exc()}", "error")

        return verification_result