# Answer Checking Feature - Implementation Refactor Documentation

## Overview

This document details the implementation of the answer checking feature for the Project Euler IDE. The feature allows users to securely verify their solutions against correct answers without exposing all answers to them. Verified solutions are visually indicated in the UI, providing a more rewarding experience.

## Files Modified

1. `run_manager.py` - Added verification functionality
2. `problem_manager.py` - Added verification tracking
3. `progress_grid.py` - Added visual indicators for verified problems
4. `pe_editor.py` - Added UI components and logic for verification
5. `README.md` - Updated documentation

## Files Added

1. `create_answers_file.py` - Script for generating encrypted answers file
2. Created `answers/` directory - Stores the encrypted answers file

## Implementation Details

### 1. Secure Answer Storage (create_answers_file.py)

Created a script to generate and maintain an encrypted answers file:

```python
def create_encrypted_answers_file(answers, key, output_file):
    """
    Create an encrypted answers file.
    
    Args:
        answers: Dictionary of problem numbers to answers
        key: Encryption key
        output_file: Path to output file
    """
    # Pickle the answers dictionary
    pickled_data = pickle.dumps(answers)
    
    # Encrypt with XOR and sign with HMAC-SHA256
    encrypted_data = bytearray()
    key_bytes = bytearray(key)
    for i, byte in enumerate(pickled_data):
        encrypted_data.append(byte ^ key_bytes[i % len(key_bytes)])
    
    # Create a signature to prevent tampering
    signature = hmac.new(key, encrypted_data, hashlib.sha256).digest()
    
    # Write the signature followed by the encrypted data
    with open(output_file, 'wb') as f:
        f.write(signature)
        f.write(encrypted_data)
```

The encryption approach uses:
- Pickling to serialize the answers dictionary
- XOR encryption with a key for basic obfuscation
- HMAC-SHA256 signature to prevent tampering
- Binary file format to prevent casual viewing

### 2. Answer Verification Logic (run_manager.py)

Added a `verify_solution` method to the `RunManager` class:

```python
def verify_solution(self, problem_number, result):
    """
    Verify if the solution result matches the correct answer.
    """
    # Check if result was successful
    if not result.get("success", False):
        return {"verified": False, "message": "Solution execution failed."}
    
    # Read and verify the encrypted answers file
    with open(self._answers_file, 'rb') as f:
        encrypted_data = f.read()
    
    # Verify signature to prevent tampering
    signature = encrypted_data[:32]
    data = encrypted_data[32:]
    expected_signature = hmac.new(self._verification_key, data, hashlib.sha256).digest()
    if not hmac.compare_digest(signature, expected_signature):
        return {"verified": False, "message": "Answers database integrity check failed."}
    
    # Decrypt and deserialize the answers
    decrypted_data = bytearray()
    key_bytes = bytearray(self._verification_key)
    for i, byte in enumerate(data):
        decrypted_data.append(byte ^ key_bytes[i % len(key_bytes)])
    
    answers = pickle.loads(bytes(decrypted_data))
    
    # Compare user's answer with correct answer
    user_answer = str(result.get("result", "")).strip()
    correct_answer = answers.get(str(problem_number))
    
    if user_answer == str(correct_answer).strip():
        # Mark as verified and update progress
        self.problem_manager.mark_problem_verified(problem_number, result.get("execution_time", 0))
        return {"verified": True, "message": "Correct answer! Solution verified."}
    else:
        return {"verified": False, "message": "Incorrect answer. Try again."}
```

Also added class attributes to store verification configuration:
```python
self._verification_key = b'ProjectEulerVerificationKey'
self._answers_file = os.path.join('answers', 'pe_answers.bin')
```

### 3. Progress Tracking (problem_manager.py)

Extended the `ProblemManager` class to track verified problems:

```python
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
            "verified_problems": []  # Added verified problems list
        }
        self._save_progress()
```

Added methods to manage verified problems:

```python
def mark_problem_verified(self, problem_number: int, execution_time: float = 0):
    """Mark a problem as verified with the correct answer."""
    # Initialize verified_problems list if it doesn't exist
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
    # Ensure verified_problems list exists
    if "verified_problems" not in self.progress:
        self.progress["verified_problems"] = []
        self._save_progress()
        
    return problem_number in self.progress["verified_problems"]
```

Updated the `get_progress` method to include verified problems:

```python
def get_progress(self) -> Dict:
    """Get the user's progress."""
    return {
        "solved_problems": self.progress["solved_problems"],
        "attempted_problems": self.progress["attempted_problems"],
        "verified_problems": self.progress.get("verified_problems", []),
        "last_attempted": self.progress["last_attempted"],
        "execution_times": self.progress["execution_times"]
    }
```

### 4. Visual Indicators (progress_grid.py)

Updated the `ProblemGrid` class to visually distinguish verified problems:

```python
def setup_ui(self):
    # Added tracking for verified problems
    self.verified_problems = set()
    
    # For each problem square
    for i in range(10):
        for j in range(10):
            # ... existing code ...
            
            # Add checkmark icon for verified problems (hidden by default)
            checkmark_label = QLabel("✓")
            checkmark_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkmark_label.setStyleSheet("""
                QLabel {
                    color: #FFFFFF;
                    font-size: 10px;
                    padding: 0px;
                    margin: 0px;
                    background: transparent;
                }
            """)
            checkmark_label.setVisible(False)  # Hide by default
            square_layout.addWidget(checkmark_label)
            
            # Store references
            square.checkmark_label = checkmark_label
```

Updated the `update_progress` method to handle verified problems:

```python
def update_progress(self, solved_problems, attempted_problems, verified_problems=None):
    """Update the visual state of problem squares based on progress."""
    self.solved_problems = set(solved_problems)
    self.attempted_problems = set(attempted_problems)
    
    # Handle verified problems
    if verified_problems is not None:
        self.verified_problems = set(verified_problems)
    
    for problem_number, square in self.problem_squares.items():
        if problem_number in self.verified_problems:
            color = "#388E3C"  # Darker green for verified
            hover_color = "#2E7D32"
            text_color = "#FFFFFF"
            # Show the checkmark for verified problems
            square.checkmark_label.setVisible(True)
        elif problem_number in solved_problems:
            color = "#4CAF50"  # Green for solved
            hover_color = "#45A049"
            text_color = "#FFFFFF"
            # Hide the checkmark for non-verified problems
            square.checkmark_label.setVisible(False)
        # ... existing code ...
```

Also updated the `square_clicked` method for consistent color handling.

### 5. UI Integration (pe_editor.py)

Added a "Verify Answer" button to the main window:

```python
# Create bottom bar with buttons
bottom_bar = QHBoxLayout()
self.run_button = QPushButton("Run Code")
self.hint_button = QPushButton("Get Hint")
self.save_button = QPushButton("Save Solution")
self.mark_solved_button = QPushButton("Mark as Solved")
self.verify_button = QPushButton("Verify Answer")  # Added verify button
bottom_bar.addWidget(self.run_button)
bottom_bar.addWidget(self.hint_button)
bottom_bar.addWidget(self.save_button)
bottom_bar.addWidget(self.mark_solved_button)
bottom_bar.addWidget(self.verify_button)  # Added to layout
```

Connected the button click signal:

```python
# Connect signals
self.run_button.clicked.connect(self.run_code)
self.hint_button.clicked.connect(self.show_hint)
self.save_button.clicked.connect(self.save_solution)
self.mark_solved_button.clicked.connect(self.mark_problem_solved)
self.verify_button.clicked.connect(self.verify_solution)  # Connected verify button
```

Added the `verify_solution` method to handle verification:

```python
def verify_solution(self):
    """Verify the current solution against the known answer."""
    # Get current problem number
    problem_number = self.problem_display.get_current_problem_number()

    # No problem selected
    if problem_number is None:
        QMessageBox.warning(self, "No Problem Selected", "Please select a problem first.")
        return
        
    # Check if we have a last run result
    if not hasattr(self, 'last_run_result') or self.last_run_result is None:
        QMessageBox.warning(self, "No Solution Run", 
                          "Please run your solution first to get a result to verify.")
        return
        
    # Verify the solution
    verification = self.run_manager.verify_solution(problem_number, self.last_run_result)
    
    # Show the result
    if verification["verified"]:
        QMessageBox.information(self, "Solution Verified", verification["message"])
        # Update the progress display
        self.update_progress()
    else:
        QMessageBox.warning(self, "Verification Failed", verification["message"])
    
    # Update status bar
    self.status_bar.showMessage(verification["message"])
```

Modified the `run_code` method to store the last result for verification:

```python
def run_code(self):
    # ... existing code ...
    
    # Handle results
    if result["success"]:
        # ... existing code ...
        
        # Store the last result for use by verify_solution
        self.last_run_result = result
    else:
        # ... existing code ...
        
        # Clear the last result
        self.last_run_result = None
```

Updated the `update_progress` method to include verified problems:

```python
def update_progress(self):
    """Update the progress grid with current status."""
    progress = self.problem_manager.get_progress()
    solved_problems = progress["solved_problems"]
    attempted_problems = progress["attempted_problems"]
    verified_problems = progress.get("verified_problems", [])
    
    # Update the progress grid with all progress information
    self.progress_grid.update_progress(solved_problems, attempted_problems, verified_problems)
```

### 6. Documentation Updates (README.md)

Added information about the answer verification feature to the README:

- Added **Answer Verification** to the Features list
- Added step 6 to the Getting Started section
- Added a dedicated Verifying Solutions section
- Updated the Tracking Progress section to include verified problems
- Added `/answers/` directory to the Project Structure section

## Security Considerations

1. **Encryption**: The answers are encrypted using a simple XOR cipher with a fixed key. While not cryptographically secure, it's sufficient to prevent casual viewing.

2. **Integrity Checking**: HMAC-SHA256 signature prevents tampering with the answers file.

3. **Binary Format**: The answers are stored in a binary file, making it harder to casually inspect the contents.

4. **No Exposure of Other Answers**: Users can only verify the answer for the problem they are currently solving.

## Usage Flow

1. User writes and runs a solution
2. Solution result is temporarily stored
3. User clicks "Verify Answer"
4. System:
   - Retrieves the saved result
   - Decrypts the answers file
   - Compares the user's result with the correct answer
   - Provides feedback on whether the answer is correct
   - Updates progress and visual indicators for verified problems

## Limitations

1. The verification key is hardcoded in the application code. In a production environment, this should be more securely managed.

2. The XOR encryption is relatively simple and can be broken with dedicated effort. For higher security, stronger encryption could be implemented.

3. The answers file currently contains only example answers for problems 1-10. A complete implementation would require all 100 answers.

## Future Enhancements

1. **Stronger Encryption**: Implement more robust encryption using libraries like cryptography.

2. **Remote Verification**: Verify answers against a server to prevent local tampering.

3. **Progressive Unlocking**: Only allow verification of problems after previous ones are solved.

## Conclusion

The answer checking feature enhances the Project Euler IDE by providing immediate feedback on solution correctness without exposing all answers. The feature is implemented with security in mind while maintaining a simple user experience. 