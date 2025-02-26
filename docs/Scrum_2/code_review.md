# Scrum 2 Code Review
-------------------------------------------------------------------------------

## GUI

### Impressions
- Smooth screen transitions
- Data entry fields accept and preserve text
- CSV import accepts file, but did not see anything in the debug output
- Excellent self explanatory code


-------------------------------------------------------------------------------

## Model

### Impressions
- Excellent comments
- Readable code

-------------------------------------------------------------------------------

## Model intake data specification

### Relevant fields
- Loan_ID: string
- Gender: string, 'Male' OR 'Female' 
- Married: string, 'Yes' OR 'No'
- ApplicantIncome: integer value
- LoanAmount: float value in thousands
- Yes/No should be omitted from intake because this is what we are evaluating for.

-------------------------------------------------------------------------------

## TO DO

Jamie:
- Complete code review, review model training tutorial for fields used, specify fields to be used in review
- Implement code review recommendations re. any commenting and formatting concerns
- Add result display function to GUI

Ahriel:
- Take specifications from code review and create standard CSV file as example of correct formatting for the model intake
- Comment out unneeded manual entry fields

Gyanu & Sulav:
- Update GUI based on code review and standard CSV to dynamically parse uploaded CSVs for relevant data only
- Continue UI aesthetics work

Will:
- Connect GUI information intake to model
- Connect model output back to GUI

## Deadline:
I would say Monday, loosely. We probably have more than enough progress to share Friday, if needed.

-------------------------------------------------------------------------------
