import json
from pathlib import Path
import shutil
import os

class TutorialManager:
    def __init__(self):
        self.tutorial_dir = Path("tutorials")
        self.tutorial_dir.mkdir(exist_ok=True)

    def save_tutorial(self, name, tutorial_data):
        """Save a tutorial to an individual JSON file."""
        tutorial_path = self.tutorial_dir / f"{name}.json"
        with open(tutorial_path, 'w') as f:
            json.dump(tutorial_data, f, indent=4)

    def load_tutorials(self):
        """Load all tutorials from individual JSON files."""
        tutorials = {}
        # Get all JSON files in the tutorial directory
        for tutorial_file in self.tutorial_dir.glob("*.json"):
            try:
                name = tutorial_file.stem  # Filename without extension
                tutorial_data = self.get_tutorial(name)
                if tutorial_data:
                    tutorials[name] = tutorial_data
            except json.JSONDecodeError:
                print(f"Error loading tutorial file: {tutorial_file}")
                continue
        return tutorials

    def get_tutorial(self, tutorial_name):
        """Get a specific tutorial by name by loading its file."""
        tutorial_path = self.tutorial_dir / f"{tutorial_name}.json"
        if tutorial_path.exists():
            try:
                with open(tutorial_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error loading tutorial file: {tutorial_path}")
                return None
        return None

    def add_tutorial(self, name, title, steps):
        """Add a new tutorial as an individual file."""
        tutorial_data = {
            "title": title,
            "steps": steps
        }
        self.save_tutorial(name, tutorial_data)

    def delete_tutorial(self, tutorial_name):
        """Delete a tutorial by removing its file."""
        tutorial_path = self.tutorial_dir / f"{tutorial_name}.json"
        if tutorial_path.exists():
            tutorial_path.unlink()
            return True
        return False
        
    def export_tutorial(self, tutorial_name, export_path):
        """Export a tutorial to a specified location.
        
        Args:
            tutorial_name: Name of the tutorial to export
            export_path: Path where the tutorial will be exported
            
        Returns:
            bool: True if export was successful, False otherwise
        """
        tutorial_path = self.tutorial_dir / f"{tutorial_name}.json"
        if not tutorial_path.exists():
            return False
            
        try:
            shutil.copy(tutorial_path, export_path)
            return True
        except Exception as e:
            print(f"Error exporting tutorial: {str(e)}")
            return False
            
    def import_tutorial(self, import_path):
        """Import a tutorial from a specified location.
        
        Args:
            import_path: Path to the tutorial JSON file to import
            
        Returns:
            bool: True if import was successful, False otherwise
        """
        if not os.path.exists(import_path):
            return False
            
        try:
            # Validate that it's a proper tutorial file by loading it
            with open(import_path, 'r') as f:
                tutorial_data = json.load(f)
                
            # Check if it has the required fields
            if not all(key in tutorial_data for key in ['title', 'steps']):
                return False
                
            # Get the tutorial name from the file name
            tutorial_name = Path(import_path).stem
            
            # Copy the file to the tutorials directory
            destination = self.tutorial_dir / f"{tutorial_name}.json"
            shutil.copy(import_path, destination)
            return True
        except Exception as e:
            print(f"Error importing tutorial: {str(e)}")
            return False 