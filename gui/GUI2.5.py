import tkinter as tk
from tkinter import Frame, ttk, filedialog, messagebox
import pandas as pd

class mainApp(tk.Tk):
    '''Class definition for the UI core and frame sizes'''

    def __init__(self, *args, **kwargs):
        '''Initialize the main UI class to serve as container for all pages.'''

        #Initialization call to the Tk class
        tk.Tk.__init__(self, *args, **kwargs)

        #Configure the main container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand=True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        #Initialize frames variable to an empty array
        self.frames = {}

        #Define a tuple of unique page classes and iteratively configure each page
        for F in (main_page, manual_entry):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        #Display the main page first
        self.show_frame(main_page)

    def show_frame(self, cont):
        '''Display additional pages when passed page titles as parameters'''
        frame = self.frames[cont]
        frame.tkraise()

class main_page(tk.Frame):
    '''Class definition for main UI page and associated buttons'''
    def __init__(self, parent, controller):
        '''Initializes the main page'''

        #Initialization call to the Tk frame
        tk.Frame.__init__(self, parent)

        #Frame labeling
        label = ttk.Label(self, text="Main")

        #Configure frame grid
        label.grid(row = 0, column = 4, padx = 10, pady = 10)

        '''Configure buttons'''

        #Configure load button
        self.load_button = ttk.Button(self, text="Load CSV File", command=self.open_command)
        self.load_button.grid(column=1, row=1, padx=10, pady=10)

        #Configure manual entry button
        self.manual_button = ttk.Button(self, text="Manual data entry",
                                command=lambda: controller.show_frame(manual_entry))
        self.manual_button.grid(column=2, row=1, padx = 10, pady = 10)

        # Submit button
        self.submit_button = ttk.Button(self, text="Check Eligibility")
        self.submit_button.grid(row=3, column= 1, padx = 10, pady = 10)

    #Configure button commands
    def open_command(self):
        '''Generates tkinter file dialog and loads a selected .CSV file
        to a pandas data frame'''

        try:
            path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if not path:  # If user cancels file selection
                return  
            input_data = pd.read_csv(path)
            messagebox.showinfo("Success", "CSV file loaded successfully!")
    
            print(input_data.head())

        except ValueError as ex:
            print("Error:", ex)
            messagebox.showinfo(message=f"Error: {ex}")

        except FileNotFoundError:
            messagebox.showerror("Error", "File not found!")
    
        except pd.errors.ParserError:
            messagebox.showerror("Error", "Invalid CSV file format!")
    
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

class manual_entry(tk.Frame):
    '''Class definition for manual data entry page and associated fields and buttons'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Manual Entry Page")
        label.grid(row=0, column=1, padx=10, pady=10)
        
        # Personal Contact Information
        # ttk.Label(self, text="Full Name").grid(row=1, column=0, sticky="w")
        # self.name_var = tk.StringVar()
        # ttk.Entry(self, textvariable=self.name_var).grid(row=1, column=1)

        ttk.Label(self, text="Gender").grid(row=1, column=0, sticky="w")
        self.name_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.name_var).grid(row=1, column=1)
        
        #ttk.Label(self, text="Date of Birth").grid(row=2, column=0, sticky="w")
        # self.dob_var = tk.StringVar()
        # ttk.Entry(self, textvariable=self.dob_var).grid(row=2, column=1)
        
        # ttk.Label(self, text="Age").grid(row=3, column=0, sticky="w")
        # self.age_var = tk.StringVar()
        # ttk.Entry(self, textvariable=self.age_var).grid(row=3, column=1)
        
        ttk.Label(self, text="Married").grid(row=4, column=0, sticky="w")
        self.marital_status_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.marital_status_var).grid(row=4, column=1)
        
        # ttk.Label(self, text="Email Address").grid(row=5, column=0, sticky="w")
        # self.email_var = tk.StringVar()
        # ttk.Entry(self, textvariable=self.email_var).grid(row=5, column=1)
        
        # ttk.Label(self, text="Primary Telephone Number").grid(row=6, column=0, sticky="w")
        # self.phone_var = tk.StringVar()
        # ttk.Entry(self, textvariable=self.phone_var).grid(row=6, column=1)
        
        # ttk.Label(self, text="Permanent Physical Address").grid(row=7, column=0, sticky="w")
        # self.address_var = tk.StringVar()
        # ttk.Entry(self, textvariable=self.address_var).grid(row=7, column=1)
        
        # Employment and Income Information
        # ttk.Label(self, text="Employment Status").grid(row=8, column=0, sticky="w")
        # self.employment_status_var = tk.StringVar()
        # ttk.Entry(self, textvariable=self.employment_status_var).grid(row=8, column=1)
        
        # ttk.Label(self, text="Work Phone Number").grid(row=9, column=0, sticky="w")
        # self.work_phone_var = tk.StringVar()
        # ttk.Entry(self, textvariable=self.work_phone_var).grid(row=9, column=1)
        
        # ttk.Label(self, text="Employer Name").grid(row=10, column=0, sticky="w")
        # self.employer_name_var = tk.StringVar()
        # ttk.Entry(self, textvariable=self.employer_name_var).grid(row=10, column=1)
        
        # ttk.Label(self, text="Gross Monthly Income").grid(row=11, column=0, sticky="w")
        # self.income_var = tk.StringVar()
        # ttk.Entry(self, textvariable=self.income_var).grid(row=11, column=1)
        
        ttk.Label(self, text="Applicant Income").grid(row=12, column=0, sticky="w")
        self.salary_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.salary_var).grid(row=12, column=1)
        
        # ttk.Label(self, text="Credit Score").grid(row=13, column=0, sticky="w")
        # self.credit_score_var = tk.StringVar()
        # ttk.Entry(self, textvariable=self.credit_score_var).grid(row=13, column=1)
        
        # ttk.Label(self, text="Monthly Mortgage or Rent Payment Amount").grid(row=14, column=0, sticky="w")
        # self.rent_var = tk.StringVar()
        # ttk.Entry(self, textvariable=self.rent_var).grid(row=14, column=1)
        
        # Personal Loan Information
        # ttk.Label(self, text="Loan Purpose").grid(row=15, column=0, sticky="w")
        # self.loan_purpose_var = tk.StringVar()
        # ttk.Entry(self, textvariable=self.loan_purpose_var).grid(row=15, column=1)
        
       #  ttk.Label(self, text="Desired Term").grid(row=16, column=0, sticky="w")
       #  self.term_var = tk.StringVar()
       #  ttk.Entry(self, textvariable=self.term_var).grid(row=16, column=1)
        
        ttk.Label(self, text="Loan Amount").grid(row=17, column=0, sticky="w")
        self.loan_amount_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.loan_amount_var).grid(row=17, column=1)
        
        # ttk.Label(self, text="Preferred Payment Due Date").grid(row=18, column=0, sticky="w")
        # self.payment_due_date_var = tk.StringVar()
        # ttk.Entry(self, textvariable=self.payment_due_date_var).grid(row=18, column=1)
        
        # Configure buttons
        self.submit_button = ttk.Button(self, text="Submit Entry", command=self.save_entry)
        self.submit_button.grid(row=19, column=1, padx=10, pady=10)

        # Back button
        back_button = ttk.Button(
            self,
            text="Back to Main",
            command=lambda: controller.show_frame(main_page)
        )
        back_button.grid(row=19, column=0, padx=10, pady=10)

    def save_entry(self):
        '''Collects user input and saves it into pandas DataFrame'''
        data = {
            "Full Name": self.name_var.get(),
            "Date of Birth": self.dob_var.get(),
            "Age": self.age_var.get(),
            "Marital Status": self.marital_status_var.get(),
            "Email": self.email_var.get(),
            "Phone": self.phone_var.get(),
            "Address": self.address_var.get(),
            "Employment Status": self.employment_status_var.get(),
            "Work Phone": self.work_phone_var.get(),
            "Employer Name": self.employer_name_var.get(),
            "Gross Monthly Income": self.income_var.get(),
            "Annual Salary": self.salary_var.get(),
            "Credit Score": self.credit_score_var.get(),
            "Monthly Rent/Mortgage": self.rent_var.get(),
            "Loan Purpose": self.loan_purpose_var.get(),
            "Desired Term": self.term_var.get(),
            "Loan Request Amount": self.loan_amount_var.get(),
            "Preferred Payment Due Date": self.payment_due_date_var.get(),
        }
        # Convert to DataFrame
        manual_entry_data = pd.DataFrame([data])

        # Combine with any existing CSV data if necessary
        try:
            existing_data = pd.read_csv("loan_entries.csv")
            combined_data = pd.concat([existing_data, manual_entry_data], ignore_index=True)
            combined_data.to_csv("loan_entries.csv", index=False)  # Save the combined data
        except FileNotFoundError:
            manual_entry_data.to_csv("loan_entries.csv", index=False)  # Save the new data if no file exists

        messagebox.showinfo("Success", "Your data has been saved!")


if __name__ == '__main__':

# Run the GUI
    app = mainApp()
    app.mainloop()
