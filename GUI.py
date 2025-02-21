import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Loan Eligibility Predictor")
root.geometry("350x250")


# Submit button
tk.Button(root, text="Check Eligibility") .grid(row=1, column= 0, columnspan=4, pady=32)

# Run the GUI
root.mainloop()
