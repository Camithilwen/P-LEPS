import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class mainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        '''Initialize the main UI class to serve as container for all pages.'''

        super().__init__(*args, **kwargs)
        self.title("Loan Eligibility Application")
        self.geometry("600x400")

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
        '''Generates tkinter file dialog and loads a selected .CSV file
        to a pandas data frame'''

        try:
            path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if not path: #If user cancels file selection
                return
            self.input_data = pd.read_csv(path)
            messagebox.showinfo("Success", "CSV file loaded successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def check_eligible(self):
        '''Provides applicant data to predictive model and triggers result display.
        TO DO:
         - Implement connection to model'''

        if not self.input_data.empty:
            pass  #Send imported csv data to model
        elif not self.manual_entry_data.empty:
            pass  #Send manually entered data to model
        self.display_result()

    def display_result(self):
        '''Displays model output and confidence score.
        To DO:
         - Connect the main_page class to receive feedback from the model.
         - Connect feedback to this display.'''

        messagebox.showinfo("Test", "Testing result output.")


class manual_entry(ctk.CTkFrame):
    '''Class definition for manual data entry page and associated fields and buttons'''

    def __init__(self, parent, controller):
        '''Initializes the page'''
        ttk.Label(self, text="Gender").grid(row=1, column=0, sticky="w")
        self.name_var = ctk.StringVar()
        ttk.Entry(self, textvariable=self.name_var).grid(row=1, column=1)
       
        ttk.Label(self, text="Married").grid(row=2, column=0, sticky="w")
        self.marital_status_var = ctk.StringVar()
        self.marital_status_dropdown = ttk.Combobox(self, textvariable=self.marital_status_var, values=["Yes", "No"], state="readonly")
        self.marital_status_dropdown.grid(row=2, column=1)
        
        ttk.Label(self, text="Dependents").grid(row=3, column=0, sticky="w")
        self.name_var = ctk.StringVar()
        ttk.Entry(self, textvariable=self.name_var).grid(row=3, column=1)
        
        ttk.Label(self, text="Education").grid(row=4, column=0, sticky="w")
        self.name_var = ctk.StringVar()
        ttk.Entry(self, textvariable=self.name_var).grid(row=4, column=1)
        
        ttk.Label(self, text="Self Employeed").grid(row=5, column=0, sticky="w")
        self.marital_status_var = ctk.StringVar()
        self.marital_status_dropdown = ttk.Combobox(self, textvariable=self.marital_status_var, values=["Yes", "No"], state="readonly")
        self.marital_status_dropdown.grid(row=5, column=1)
        
        ttk.Label(self, text="Applicant Income ").grid(row=6, column=0, sticky="w")
        self.name_var = ctk.StringVar()
        ttk.Entry(self, textvariable=self.name_var).grid(row=6, column=1)  
        
        ttk.Label(self, text="CoApplicant Income ").grid(row=7, column=0, sticky="w")
        self.name_var = ctk.StringVar()
        ttk.Entry(self, textvariable=self.name_var).grid(row=7, column=1)  
        
        ttk.Label(self, text="Loan Amount").grid(row=8, column=0, sticky="w")
        self.loan_amount_var = ctk.StringVar()
        ttk.Entry(self, textvariable=self.loan_amount_var).grid(row=8, column=1)
        
        ttk.Label(self, text="Loan Amount Term").grid(row=9, column=0, sticky="w")
        self.term_var = ctk.StringVar()
        ttk.Entry(self, textvariable=self.term_var).grid(row=9, column=1)
        
        ttk.Label(self, text="Credit History").grid(row=10, column=0, sticky="w")
        self.name_var = ctk.StringVar()
        ttk.Entry(self, textvariable=self.name_var).grid(row=10, column=1)  
        
        ttk.Label(self, text="Property Area").grid(row=11, column=0, sticky="w")
        self.name_var = ctk.StringVar()
        ttk.Entry(self, textvariable=self.name_var).grid(row=11, column=1)
        
        ttk.Label(self, text="Loan Status").grid(row=12, column=0, sticky="w")
        self.name_var = ctk.StringVar()
        ttk.Entry(self, textvariable=self.name_var).grid(row=12, column=1)
        
        
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
            ("Gender", "text"),
            ("Married", "option"),
            ("Applicant Income", "number"),
            ("Loan Amount", "number")
        ]

        for row, (label_text, field_type) in enumerate(fields, 1):
            ctk.CTkLabel(self, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="w")
            var = ctk.StringVar()

            if field_type == "option":
                entry = ctk.CTkOptionMenu(self, variable=var, values=["Yes", "No"])
            else:
                entry = ctk.CTkEntry(self, textvariable=var)

            entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            self.entries[label_text] = var

        #Define buttons
        ctk.CTkButton(self, text="Back to Main",
                     command=lambda: controller.show_frame(main_page)
                     ).grid(row=5, column=0, padx=10, pady=20)
        ctk.CTkButton(self, text="Submit Entry",
                     command=self.save_entry).grid(row=5, column=1, padx=10, pady=20)

    def save_entry(self):
        '''Collects user input and saves it into pandas DataFrame'''

        data = {
            "Gender": self.entries["Gender"].get(),
            "Married": self.entries["Married"].get(),
            "Applicant Income": self.entries["Applicant Income"].get(),
            "Loan Amount": self.entries["Loan Amount"].get(),
        }

        #Convert input to DataFrame
        manual_entry_data = pd.DataFrame([data])
        main_page.manual_entry_data = manual_entry_data

        #Combine with existing CSV data if required
        try:
            existing_data = pd.read_csv("loan_entries.csv")
            combined_data = pd.concat([existing_data, manual_entry_data], ignore_index=True)
            combined_data.to_csv("loan_entries.csv", index=False) #Save combined data
        except FileNotFoundError:
            manual_entry_data.to_csv("loan_entries.csv", index=False) #Save new data if no existing file

        messagebox.showinfo("Success", "Your data has been saved!")


if __name__ == '__main__':
    app = mainApp()
    app.mainloop()
