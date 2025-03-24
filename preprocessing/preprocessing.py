import pandas as pd

def check_eligible(data):
    """ Processes loan application data and checks eligibility. """

    print("\n ***Received Data in check_eligible()***")
    print(data.head())  # Print first few rows to confirm data

    required_columns = ["Gender", "Married", "Dependents", "Education",
                        "Self_Employed", "Applicantincome", "Coapplicantincome",
                        "Loanamount", "Loan_Amount_Term", "Credit_History", "Property_Area"]

    missing_cols = [col for col in required_columns if col not in data.columns]
    if missing_cols:
        print(f"***Missing columns in input data:*** {', '.join(missing_cols)}")
        raise ValueError(f"Missing columns in input data: {', '.join(missing_cols)}")

        #Example Logic. Will be replaced by the model we are making I suppose?
    def eligibility(x):
        if x == 1:
            return "Eligible"
        else:
            return "Not Eligible"

    data["Eligibility"] = data["Credit_History"].apply(eligibility)

    print("\n *** Processed Data with Eligibility:***")
    print(data[["Eligibility"]].head())  # Show eligibility results

    return data
