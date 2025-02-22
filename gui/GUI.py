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

        #Initialize a frames variable to an empty array
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

        #Inihttps://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/tialization call to the Tk frame
        tk.Frame.__init__(self, parent)

        #Frame labeling
        label = ttk.Label(self, text="Main")

        #Configure frame grid
        label.grid(row = 0, column = 4, padx = 10, pady = 10)

    '''Configure buttons'''

    #Configure button commands
    def open_command():
        '''Generates tkinter file dialog and loads a selected .CSV file
        to a pandas data frame'''

        try:
            path = filedialog.askopenfile(filetypes=[("CSV files", "*.csv")])
            input_data = pd.read_csv(path.name)

        except ValueError as ex:
            print("Error:", ex)
            messagebox.showinfo(message=f"Error: {ex}")

    #Configure load button
    load_button = ttk.Button(text="Load CSV File", command=open_command)
    load_button.grid(column=1, row=1, padx=10, pady=10)

    #Configure manual entry button
    manual_button = ttk.Button(text="Manual data entry",
                               command = lambda : controller.show_frame(manual_entry))
    manual_button.grid(column=2, row=1, padx = 10, pady = 10)

    # Submit button
    submit_button = ttk.Button(text="Check Eligibility")
    submit_button.grid(row=3, column= 1, padx = 10, pady = 10)

class manual_entry(tk.Frame):
    '''Class definition for manual data entry page and associated fields and buttons'''
    '''TO DO:
    - Define entry fields for desired values
    - Define a save button
    - Link fields to save button and collect values into a pandas dataframe
    - Define a text display to confirm data has saved
    - Define a button to return to main screen
    '''



if __name__ == '__main__':

# Run the GUI
    app = mainApp()
    app.mainloop()
