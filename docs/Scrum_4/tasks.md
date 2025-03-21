# GUI
Jamie:
- Rearrange buttons and window size on manual entry screen (in progress)
- Finish Scrum 3 Issue documentation
- add code for batch import from large csv

## Model connection

Gyanu & Sulav:
- drop loanID column during CSV loading
- pass data from csv import or manual entry to preprocessing file (filename preprocessing.py) (a check_eligible() method exist)
- create preprocessing file
- Connect the check_eligible() method to the correct button

Ahriel:
- Edit the display_result() function in the main page to accept an display an array of multiple values (a yes/no answer as a boolean, a confidence score a float percentage, and (on a "no" answer) one or more failure reasons as individual column names (code will have to be able to adjust output dynamically).

Will:
- Create prediction file
- Add feedback on failure for individual features
-------------------------------------------------------------------------------
#Step breakdown
### Create preprocessing python file
Process data from GUI collection as done in model file:
- Drop loanID (if present) (can be done during CSV import step)
- Scale using standard scalar in Sklearn to fit new data to the same shape as the training data. (Use scaler = StandardScaler())

### Create prediction python file
- Loads the .h5 file (the saved model)
- Use the model.evaluate(data) (or similarly named function) to evaluate new data from the preprocessing file and receive a yes or no answer
- Pass yes/no answer and confidence score (times by 100 for percentage) back to the GUI for display.

-------------------------------------------------------------------------------
