# Tutorial Editor Guide

This guide explains how to create and edit tutorials using the Tutorial Editor in the Project Euler Editor.

## Accessing the Tutorial Editor

1. Click on the "Help" menu in the main window
2. Select "Tutorial Editor"

## Creating a New Tutorial

1. In the Tutorial Editor window:
   - Enter a unique name for your tutorial (e.g., "data_files")
   - Enter a title that will be displayed to users (e.g., "Working with Data Files")
   - Click "Add Step" to create tutorial steps

2. For each step:
   - Enter a step title (e.g., "Downloading Data Files")
   - Write the content in markdown format
   - (Optional) Select an action
   - (Optional) Enter parameters in JSON format

3. Click "Save Tutorial" to save your work

## Editing an Existing Tutorial

1. Click the "Load Tutorial" button
2. Select the tutorial you want to edit from the list
3. Make your changes to the title, steps, or content
4. Click "Save Tutorial" to save your changes

## Step Actions and Parameters

The tutorial editor supports several actions that can enhance the tutorial experience by guiding users through the interface and demonstrating features.

### Available Actions

1. `none` - No special action (default)
   - Use when you just want to display information without any interface interaction
   - No parameters required

2. `highlight_areas` - Highlights specific areas of the interface
   - Parameters:
     ```json
     {
         "areas": ["area1", "area2", ...]
     }
     ```
   - Available areas:
     - `problem_description` - The main problem text area
     - `code_editor` - The code editing area
     - `run_button` - The Run Code button
     - `hint_button` - The Get Hint button
     - `save_button` - The Save Solution button
     - `mark_solved_button` - The Mark as Solved button
     - `data_file_indicator` - The data file status indicator
     - `progress_grid` - The problem progress grid
     - `helper_files_list` - The list of helper files
     - `helpers_editor` - The helper files editor
     - `data_preview` - The data file preview area

3. `highlight_button` - Highlights a specific button
   - Parameters:
     ```json
     {
         "button": "button_name"
     }
     ```
   - Available buttons:
     - `run` - Run Code button
     - `hint` - Get Hint button
     - `save` - Save Solution button
     - `mark_solved` - Mark as Solved button
     - `add_helper` - Add Helper File button
     - `delete_helper` - Delete Helper File button
     - `test_helper` - Test Helper Function button
     - `save_helper` - Save Helper File button
     - `load_helper` - Load Helper File button

4. `select_problem` - Selects and loads a specific problem
   - Parameters:
     ```json
     {
         "problem_number": 1
     }
     ```
   - The problem number must be a valid Project Euler problem number

5. `show_dialog` - Opens a specific dialog
   - Parameters:
     ```json
     {
         "dialog": "dialog_name"
     }
     ```
   - Available dialogs:
     - `templates` - Code Templates dialog
     - `settings` - Settings dialog
     - `progress` - Progress dialog
     - `about` - About dialog
     - `info` - Info dialog

6. `insert_template` - Inserts a code template
   - Parameters:
     ```json
     {
         "template": "template_name"
     }
     ```
   - The template name must match an existing template

7. `run_code` - Runs the current code
   - No parameters required
   - Simulates clicking the Run Code button

8. `load_helper` - Loads a helper file
   - Parameters:
     ```json
     {
         "filename": "helper_name.py"
     }
     ```
   - The filename must exist in the helper files list

### Action Combinations

You can combine multiple actions in a single step by separating them with commas:

```json
{
    "action": "highlight_areas,highlight_button",
    "params": {
        "areas": ["code_editor"],
        "button": "run"
    }
}
```

### Action Sequences

For complex tutorials, you can create a sequence of actions that execute in order:

```json
{
    "action": "select_problem,highlight_areas,run_code",
    "params": {
        "problem_number": 1,
        "areas": ["code_editor", "run_button"]
    }
}
```

### Best Practices for Actions

1. **Use Sparingly**: Only use actions when they add value to the tutorial
2. **Be Specific**: Target specific interface elements rather than highlighting large areas
3. **Logical Flow**: Arrange actions in a logical sequence that matches the tutorial flow
4. **Test Thoroughly**: Verify that all actions work as expected in the tutorial
5. **Provide Context**: Always include explanatory text with actions to guide the user

### Example with Multiple Actions

```json
{
    "title": "Solving Your First Problem",
    "steps": [
        {
            "title": "Select Problem",
            "content": "Let's start with Problem 1. The system will load it for you.",
            "action": "select_problem",
            "params": {
                "problem_number": 1
            }
        },
        {
            "title": "Write Your Solution",
            "content": "Type your solution in the code editor. We'll highlight the important areas.",
            "action": "highlight_areas",
            "params": {
                "areas": ["problem_description", "code_editor"]
            }
        },
        {
            "title": "Run Your Code",
            "content": "Click the Run button to test your solution.",
            "action": "highlight_button,run_code",
            "params": {
                "button": "run"
            }
        }
    ]
}
```

## Example Tutorial

Here's an example of a complete tutorial JSON file:

```json
{
    "title": "Working with Data Files",
    "steps": [
        {
            "title": "Introduction",
            "content": "Many Project Euler problems require working with data files. This tutorial will show you how to handle these files effectively.",
            "action": "none",
            "params": {}
        },
        {
            "title": "Downloading Data Files",
            "content": "1. Look for the data file indicator below the problem description\n2. Click the download link if the file is missing\n3. The file will be automatically downloaded to the correct location",
            "action": "highlight_areas",
            "params": {
                "areas": ["data_file_indicator"]
            }
        },
        {
            "title": "Using Data Files",
            "content": "1. The data file will be automatically loaded when you run your code\n2. You can access it using the provided helper functions\n3. Check the problem description for specific usage instructions",
            "action": "highlight_button",
            "params": {
                "button": "run"
            }
        }
    ]
}
```

## Markdown Formatting

You can use markdown in the step content for better formatting:

```markdown
# This is a heading
This is a paragraph with **bold** and *italic* text.

1. This is a numbered list
2. With multiple items

- This is a bullet list
- With multiple items

`This is code`

> This is a blockquote
```

## Best Practices

1. **Naming**: Use descriptive, lowercase names without spaces (e.g., "data_files" instead of "Data Files")

2. **Structure**:
   - Start with an introduction step
   - Break complex topics into multiple steps
   - End with a summary or next steps

3. **Content**:
   - Be clear and concise
   - Use markdown formatting for readability
   - Include examples where helpful
   - Use actions to guide users' attention

4. **Testing**:
   - Test your tutorial after creating it
   - Verify all actions work as expected
   - Check that the content is clear and helpful

## Troubleshooting

If you encounter issues:

1. **File Not Found**: Ensure the tutorial name matches the filename exactly
2. **JSON Errors**: Check that your parameters are valid JSON
3. **Action Not Working**: Verify the action name and parameters are correct
4. **Content Not Displaying**: Check your markdown formatting

## Support

If you need help creating or editing tutorials, please contact the development team. 