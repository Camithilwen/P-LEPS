# GUI

## 1
![[./error_screenshots/'input_data error.png']]
### Problem statement:
"Cannot access local variable 'input_data' where it is not associated with a value."
If the user did not select a file, a variable was still initialized from a csv read of a null path.

### Solution:
Added a condition for no path above the variable initialization with an empty return statement.

