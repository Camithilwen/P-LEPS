import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from ..prediction.prediction import predict_loan_status

# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class mainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        '''Initialize the main UI class to serve as container for all pages.'''

        super().__init__(*args, **kwargs)
        self.title("Loan Eligibility Application")
        self.geometry("380x600")

        # Configure the main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Initialize frames vairable to an empty array
        self.frames = {}

        #Define a tuple of unique page classes and iteratively configure each page
        for F in (main_page, manual_entry):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #Display the main page first
        self.show_frame(main_page)

    def show_frame(self, cont):
        '''Display additional pages when passed page titles as parameters'''

        frame = self.frames[cont]
        frame.tkraise()


class main_page(ctk.CTkFrame):
    '''Class definition for main UI page and associated buttons'''

    def __init__(self, parent, controller):
        '''Initializes the main page'''

        #Frame initialization call
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Define widgets
        label = ctk.CTkLabel(self, text="Loan Eligibility Checker",
                           font=("Arial", 20, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=20)

        self.load_button = ctk.CTkButton(self, text="Load CSV File", command=self.open_command)
        self.load_button.grid(row=1, column=0, padx=10, pady=10)

        self.manual_button = ctk.CTkButton(self, text="Manual Data Entry",
                                         command=lambda: controller.show_frame(manual_entry))
        self.manual_button.grid(row=1, column=1, padx=10, pady=10)

        self.submit_button = ctk.CTkButton(self, text="Check Eligibility", command=self.check_eligible)
        self.submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

        # Initialize data storage
        self.input_data = pd.DataFrame()
        self.manual_entry_data = pd.DataFrame()

    def open_command(self):
        '''Generates tkinter file dialog and loads a selected .CSV file to a pandas DataFrame'''

        try:
            path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if not path:  # If user cancels file selection
                return
            data = pd.read_csv(path)
            #Print the columns and first few rows of the data
            print("\n\nActual CSV Columns:\n", data.columns.tolist())
            
            #Dropping the loan_Id column if it exists
            if "Loan_ID" in data.columns:
                data.drop(columns=["Loan_ID"], inplace=True)

            data.columns = data.columns.str.strip().str.replace(" ", "_").str.title()

            required_columns = ["Gender", "Married", "Dependents", "Education",
                                "Self_Employed", "Applicantincome", "Coapplicantincome", "Loanamount", "Loan_Amount_Term", "Credit_History", "Property_Area"]
            
            print("\n \nModified CSV Columns:\n", data.columns.tolist())
            missing_cols = [col for col in required_columns if col not in data.columns]

            #Check for missing columns
            if missing_cols:
                messagebox.showerror("Error", f"Missing columns in CSV: {', '.join(missing_cols)}")
                return

            #Select only relevant columns
            self.input_data = data[required_columns]

            messagebox.showinfo("Success", "CSV file loaded successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the file: {e}")

    def check_eligible(self):
        '''Pass data to preprocessing.py and display results'''
        try:

            if not self.input_data.empty:
                print("\n Sending CSV Data to check_eligible()...")
                input_data = self.input_data.copy()  # Process CSV data
            elif not self.manual_entry_data.empty:
                print("\n Sending Manual Entry Data to check_eligible()...")
                input_data = self.manual_entry_data.copy()  # Process manual data
            else:
                messagebox.showerror("Error", "No data available to check eligibility!")
                print("No data available to process.")
                return

            #Get predictions
            results = predict_loan_status(input_data)

            # Display results
            result_text = results["Eligibility"].to_string(index=false)
            self.display_result(result_text)

        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")

    def display_result(self, eligibility_result):
        '''Displays model output and confidence score.'''

        ResultDialog(self.controller, eligibility_result)


class manual_entry(ctk.CTkFrame):
    '''Class definition for manual data entry page and associated fields and buttons'''

    def __init__(self, parent, controller):
        '''Initializes the page'''

        
        #Frame initialization call
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        #Define labels
        label = ctk.CTkLabel(self, text="Manual Entry Page",
                           font=("Arial", 20, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=20)

        #Define entry fields
        self.entries = {}
        fields = [
            ("Gender", "gender"),
            ("Married", "option"),
            ("Dependents", "number"),
            ("Education", "education"),
            ("Self Employed", "option" ),
            ("Applicant Income", "number"),
            ("Co-applicant Income", "number"),
            ("Loan Amount", "number"),
            ("Loan Term", "number"),
            ("Credit History", "number"),
            ("Property Area Type", "area")
        ]

        for row, (label_text, field_type) in enumerate(fields, 1):
            ctk.CTkLabel(self, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="w")
            var = ctk.StringVar()

            if field_type == "gender":
                entry = ctk.CTkOptionMenu(self, variable=var, values=["X", "Female", "Male"])
            elif field_type == "option":
                entry = ctk.CTkOptionMenu(self, variable=var, values=["Yes", "No"])
            elif field_type == "education":
                entry = ctk.CTkOptionMenu(self, variable=var, values=["Graduate", "Not Graduate"])
            elif field_type == "area":
                entry = ctk.CTkOptionMenu(self, variable=var, values=["Urban", "Semiurban", "Rural"])
            else:
                entry = ctk.CTkEntry(self, textvariable=var)

            entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            self.entries[label_text] = var

        #Define buttons
        ctk.CTkButton(self, text="Back to Main",
                     command=lambda: controller.show_frame(main_page)
                     ).grid(row=12, column=0, padx=10, pady=20)
        ctk.CTkButton(self, text="Submit Entry",
                     command=self.save_entry).grid(row=12, column=1, padx=10, pady=20)

    def save_entry(self):
        '''Collects user input and saves it into pandas DataFrame'''

        data = {
            "Gender": self.entries["Gender"].get(),
            "Married": self.entries["Married"].get(),
            "Dependents": self.entries["Dependents"].get(),
            "Education": self.entries["Education"].get(),
            "Self_Employed": self.entries["Self Employed"].get(),
            "ApplicantIncome": self.entries["Applicant Income"].get(),
            "CoapplicantIncome": self.entries["Co-applicant Income"].get(),
            "LoanAmount": self.entries["Loan Amount"].get(),
            "Loan_Amount_Term": self.entries["Loan Term"].get(),
            "Credit_History": self.entries["Credit History"].get(),
            "Property_Area": self.entries["Property Area Type"].get()
        }

        #Convert input to DataFrame
        manual_entry_data = pd.DataFrame([data])
        self.manual_entry_data = manual_entry_data

        #Ask user to save as new or append to existing
        append = messagebox.askyesno("Save Options", "Append to existing CSV file?\n(Click 'No' to save as a new file)")

        if append:
            path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if not path: #User cancellation
                return
            try:
                existing_data = pd.read_csv(path)
                combined_data = pd.concat([existing_data, manual_entry_data], ignore_index=True)
                combined_data.to_csv(path, index=False) #overwrite selected file
                messagebox.showinfo("Success", "Data appended to existing file!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to append:\n{e}")
        else:
            #Let user specify new file path
            path = filedialog.asksaveasfilename(
                defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save as new CSV"
            )
            if not path: #User cancellation
                return
            try:
                manual_entry_data.to_csv(path, index=False)
                messagebox.showinfo("Success", "Data saved to a new file!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save:\n{e}")

        #Combine with existing CSV data if required
        #try:
            #existing_data = pd.read_csv("loan_entries.csv")
            #combined_data = pd.concat([existing_data, manual_entry_data], ignore_index=True)
            #combined_data.to_csv("loan_entries.csv", index=False) #Save combined data
        #except FileNotFoundError:
            #manual_entry_data.to_csv("loan_entries.csv", index=False) #Save new data if no existing file

        #messagebox.showinfo("Success", "Your data has been saved!")

class ResultDialog(ctk.CTkToplevel):
    """Custom resizable dialog for displaying eligibility results."""
    def __init__(self, parent, result_text):
        super().__init__(parent)
        self.title("Eligibility Result")
        self.geometry("600x400")  # Set default size (width x height)

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Add scrollable text box
        self.textbox = ctk.CTkTextbox(self, wrap="none")
        self.textbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.textbox.insert("1.0", result_text)  # Insert eligibility results
        self.textbox.configure(state="disabled")  # Make it read-only

        # Close button
        self.button = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.button.grid(row=1, column=0, pady=10)

if __name__ == '__main__':
    app = mainApp()
    app.mainloop()
