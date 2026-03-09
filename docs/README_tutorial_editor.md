# Project Euler Tutorial Editor

This standalone application allows you to create and edit tutorials for the Project Euler Editor without needing to run the main application. It provides a user-friendly interface for authoring tutorials that can be displayed in the main Project Euler Editor application.

## Features

- Create new tutorials with multiple steps
- Edit existing tutorials
- Organize tutorial content in a step-by-step format
- Add special actions to enhance tutorial interactivity
- Preview tutorial descriptions

## Setup

1. Ensure you have Python 3.6+ installed
2. Install required packages: `pip install PyQt6`
3. Place this application in the same project directory as your Project Euler Editor

## Usage

### Starting the Application

```bash
python tutorial_editor_app.py
```

### Creating a New Tutorial

1. Click the "New Tutorial" button or select File > New Tutorial
2. Enter a unique name for your tutorial (e.g., "data_files")
3. Enter a title that will be displayed to users (e.g., "Working with Data Files")
4. Add steps by clicking the "Add Step" button
5. For each step:
   - Enter a step title
   - Write the content (supports basic formatting)
   - Add actions and parameters if needed
6. Click "Save Tutorial" when finished

### Editing Existing Tutorials

1. Select a tutorial from the list
2. Click the "Edit Tutorial" button
3. Modify the tutorial content as needed
4. Click "Save Tutorial" to save your changes

### Tutorial Actions

The editor supports several actions that can enhance the tutorial experience:

1. `none` - No special action (default)
2. `highlight_areas` - Highlights specific areas of the interface
3. `highlight_button` - Highlights a specific button
4. `select_problem` - Automatically selects a problem
5. `show_dialog` - Shows a specific dialog
6. `run_code` - Runs the current code

## File Format

Tutorials are stored as JSON files in the `tutorials` directory. They share the same format as the main Project Euler Editor application, ensuring compatibility between both applications.

Example tutorial JSON structure:

```json
{
    "title": "Welcome to Project Euler Editor",
    "steps": [
        {
            "title": "Welcome",
            "content": "Welcome to the Project Euler Editor!",
            "action": "none"
        },
        {
            "title": "Interface Overview",
            "content": "The interface is divided into three main areas...",
            "action": "highlight_areas",
            "params": {
                "areas": ["problem_description", "code_editor"]
            }
        }
    ]
}
```

## Integration with Project Euler Editor

The tutorials created with this editor can be immediately accessed in the main Project Euler Editor application. Both applications use the same `tutorials` directory, so any changes made with the editor will be reflected in the main application.

## For More Information

See the Tutorial Authoring Guide (Help > Tutorial Authoring Guide) for detailed instructions on creating effective tutorials. 