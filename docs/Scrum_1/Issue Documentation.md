
# GUI

## 1:
![[Screenshot_20250222_013348 1.png]]
### Problem statement:
- "Positional argument follows keyword argument."
- frame grid definition flagged by linter

### Solution:
* column value assignment mistyped
* swapped "-" for "="

## 2:
![[unknown_option_menu.png]]

![[Pasted image 20250223214512.png]]
### Problem statement:
* Iterative frame initialization failed with internal tkinter error
* Tkinter responding as though an illegal "-menu" option was passed when no such argument was made

## Solution:

#### Before:
![[Pasted image 20250223221040.png]]
#### After:
![[Pasted image 20250223221608.png]]

* The "manual_entry" class had not been defined yet, and contained only a pass statement
* Without an init() method, the "controller" parameter was being interpreted as an erroneous menu configuration option.
* Defined "manual_entry".

## 3:
 ![[Pasted image 20250223215102.png]]
![[Pasted image 20250223215209.png]]
### Problem statement:
* "NameError: 'self' is not defined"

### Solution:
* resolved by nesting button configuration beneath "main_page.\_\_init\_\_()" and adding "self." as a pre fix to each button definition.