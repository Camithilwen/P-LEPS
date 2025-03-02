import tkinter as tk
from tkinter import Frame, ttk, filedialog, messagebox
import pandas as pd

class mainApp(tk.Tk):
    '''Class definition for the UI core and frame sizes'''

    def __init__(self, *args, **kwargs):
        '''Initialize the main UI class to serve as container for all pages.'''

        # Initialization call to the Tk class
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Loan Eligibility Application")
        self.configure(bg="#8B8989")  # Set root window background to gray

        # Configure the main container
        container = tk.Frame(self, bg="#8B8989")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initialize frames variable to an empty array
        self.frames = {}

        # Define a tuple of unique page classes and iteratively configure each page
        for F in (main_page, manual_entry):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Display the main page first
        self.show_frame(main_page)

    def show_frame(self, cont):
        '''Display additional pages when passed page titles as parameters'''
        frame = self.frames[cont]
        frame.tkraise()


class main_page(tk.Frame):
    '''Class definition for main UI page and associated buttons'''
    def __init__(self, parent, controller):
        '''Initializes the main page'''

        # Initialization call to the Tk frame
        tk.Frame.__init__(self, parent, bg="#8B8989")
        self.controller = controller

        # Frame labeling
        label = tk.Label(self, text="Loan Eligibility Checker", font=("Arial", 16, "bold"), bg="#8B8989", fg="#27408B")
        label.grid(row=0, column=0, columnspan=3, pady=20)

        # Configure buttons
        self.load_button = tk.Button(self, text="Load CSV File", command=self.open_command,
                                    bg="#27408B", fg="black", font=("Arial", 12), relief="flat")
        self.load_button.grid(row=1, column=0, padx=10, pady=10)

        self.manual_button = tk.Button(self, text="Manual Data Entry", bg="#27408B", fg="black",
                                       font=("Arial", 12), relief="flat",
                                       command=lambda: controller.show_frame(manual_entry))
        self.manual_button.grid(row=1, column=1, padx=10, pady=10)

        self.submit_button = tk.Button(self, text="Check Eligibility", bg="#27408B", fg="black",
                                      font=("Arial", 12), relief="flat")
        self.submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Configure button commands
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

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


class manual_entry(tk.Frame):
    '''Class definition for manual data entry page and associated fields and buttons'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#8B8989")
        self.controller = controller

        # Frame labeling
        label = tk.Label(self, text="Manual Entry Page", font=("Arial", 16, "bold"), bg="#8B8989", fg="#27408B")
        label.grid(row=0, column=0, columnspan=2, pady=20)

        # Personal Contact Information
        fields = [
            ("Gender", "name_var"),
            ("Married", "marital_status_var"),
            ("Applicant Income", "salary_var"),
            ("Loan Amount", "loan_amount_var"),
        ]
        for i, (text, var_name) in enumerate(fields):
            tk.Label(self, text=text, bg="#8B8989", fg="black", font=("Arial", 12)).grid(row=i+1, column=0, sticky="w", padx=10, pady=5)
            setattr(self, var_name, tk.StringVar())
            if text == "Married":
                dropdown = ttk.Combobox(self, textvariable=getattr(self, var_name), values=["Yes", "No"], state="readonly")
                dropdown.grid(row=i+1, column=1, padx=10, pady=5)
            else:
                tk.Entry(self, textvariable=getattr(self, var_name), font=("Arial", 12)).grid(row=i+1, column=1, padx=10, pady=5)

        # Configure buttons
        self.submit_button = tk.Button(self, text="Submit Entry", command=self.save_entry,
                                       bg="#27408B", fg="black", font=("Arial", 12), relief="flat")
        self.submit_button.grid(row=len(fields)+2, column=1, padx=10, pady=10)

        # Back button
        back_button = tk.Button(self, text="Back to Main", bg="#27408B", fg="black",
                               font=("Arial", 12), relief="flat",
                               command=lambda: controller.show_frame(main_page))
        back_button.grid(row=len(fields)+2, column=0, padx=10, pady=10)

    def save_entry(self):
        '''Collects user input and saves it into pandas DataFrame'''
        data = {
            "Gender": self.name_var.get(),
            "Married": self.marital_status_var.get(),
            "Applicant Income": self.salary_var.get(),
            "Loan Amount": self.loan_amount_var.get(),
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