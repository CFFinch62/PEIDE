# Variable Inspector Guide

## Overview
The Variable Inspector is a powerful debugging tool in the Project Euler Editor that automatically tracks variables during code execution. Unlike traditional debugging that requires breakpoints or manual print statements, the Variable Inspector automatically captures and displays variable values from debug messages.

## Key Features
- **Automatic variable tracking**: Detects variables from debug output without code modifications
- **Real-time updates**: Shows current values as they change during execution
- **Color-coded display**: Different debug levels are displayed in different colors
- **Timestamp tracking**: Records when each variable was last updated
- **Context menu**: Easy access to copy and clear functions
- **Persistence**: Variables remain tracked between runs for easy comparison

## How It Works

### Variable Detection
The Variable Inspector automatically recognizes variables in debug messages using pattern matching:

1. **Assignment patterns**: Detects both `variable = value` and `variable: value` formats
2. **Selective tracking**: Only tracks variables from debug, info, and important levels
3. **Metadata collection**: Stores not just values but also timestamps and debug levels

### The Variable Inspector Panel
Located below the main debug output, the Variable Inspector shows:

- A table of all tracked variables
- Each variable's current value
- Timestamp of the last update
- Color-coding based on the debug level

## Using the Variable Inspector

### Adding Variables to Track
Include variable assignments in your debug messages:

```python
# These patterns will be automatically tracked
debug("counter = 5")
debug("result = 42", "info")
debug("total_sum: 1275", "important")

# These won't be tracked (error level not tracked)
debug("error_code = 404", "error") 
```

### Interacting with the Variable Inspector

**Context Menu** (right-click anywhere in the Variable Inspector):
- **Copy**: Copy selected variable details to clipboard
- **Select All**: Select all variables in the inspector
- **Clear Variables**: Remove all currently tracked variables

**Keyboard Shortcuts**:
- **Ctrl+C**: Copy selected variable details when focused on the Variable Inspector

### Practical Examples

#### Example 1: Tracking Loop Variables
```python
def solve():
    total = 0
    for i in range(1, 1001):
        if i % 3 == 0 or i % 5 == 0:
            total += i
            debug(f"i = {i}")
            debug(f"total = {total}")
    return total
```

The Variable Inspector will automatically track `i` and `total`, showing their evolution through the loop.

#### Example 2: Monitoring Algorithm State
```python
def solve():
    n = 600851475143
    largest_factor = 1
    i = 2
    
    while i * i <= n:
        debug(f"i = {i}")
        if n % i:
            i += 1
        else:
            n //= i
            debug(f"n = {n}")
            largest_factor = i
            debug(f"largest_factor = {largest_factor}")
    
    if n > 1:
        largest_factor = n
        debug(f"final largest_factor = {largest_factor}")
    
    return largest_factor
```

This will track the state of your algorithm, showing how `n`, `i`, and `largest_factor` change throughout execution.

## Tips for Effective Use

1. **Use consistent variable formats**: Stick to either `var = value` or `var: value` patterns for clarity.

2. **Track intermediate calculations**: Show the steps of complex formulas to identify where issues occur.
   ```python
   partial_result = (n * (n-1)) / 2
   debug(f"partial_result = {partial_result}")
   ```

3. **Group related variables**: Use the same debug level for related variables to make them visually grouped.
   ```python
   debug(f"x = {x}", "important")
   debug(f"y = {y}", "important")
   ```

4. **Clear variables when switching problems**: The system automatically clears variables when changing problems, but you can manually clear them at any time.

5. **Use timestamps to identify bottlenecks**: Look at timestamp differences to see which operations take the most time.

## Troubleshooting

**Variables not appearing?**
- Ensure the debug level is enabled (debug, info, or important)
- Check that the debug output is not filtered out
- Verify variable assignment uses `=` or `:` format
- Make sure master debug toggle is enabled

**Variable display issues?**
- Very long values will be truncated in the display
- Complex objects might not display optimally
- If a variable updates too rapidly, you might only see the final value

## Technical Details

The Variable Inspector uses regular expression matching to detect variables:
```python
variable_patterns = [
    r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([^=]+)$',  # var = value
    r'([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*([^:]+)$',  # var: value
]
```

It stores variables in a dictionary structure:
```python
{
    'variable_name': {
        'value': 'current_value',
        'timestamp': datetime_object,
        'level': 'debug_level'
    }
}
```

## Integration with Debug Workflow

The Variable Inspector is integrated with the rest of the debugging system:

1. Variables are cleared when you:
   - Switch to a different problem
   - Manually clear the variable tracking
   - Restart the application

2. The variable inspector panel size can be adjusted by dragging the splitter between debug output and variable inspector.

3. Search functionality in the debug panel also searches variable values, making it easy to find specific data.

---

This comprehensive tracking system eliminates the need for instrumenting code with print statements, allowing you to focus on solving Project Euler problems while still having full visibility into your code's behavior. 