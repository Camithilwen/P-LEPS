import pytest
from src.gui.gui_5_0 import mainApp, manual_entry, ResultDialog
from unittest.mock import patch, Mock
import pandas as pd
import numpy as np

@pytest.fixture
def app():
    """Fixture to create and destroy the main application"""
    application = mainApp()
    yield application
    application.destroy()

@pytest.fixture
def manual_entry_page(app):
    """Fixture to create and destroy the manual entry page"""
    manual_entry_page = app.frames['manual_entry']
    yield manual_entry_page
    manual_entry_page.destroy()

def test_main_window(app):
    """Test if main window initializes properly"""
    assert app.winfo_exists()

def test_csv_loading(app):
    """Test CSV loading functionality"""
    with patch('pandas.read_csv') as mock_read, \
         patch('src.gui.gui_5_0.messagebox') as mock_msg:

        # Setup mock return value
        mock_read.return_value = pd.DataFrame({
            'Applicant_Income': [30000],
            'Coapplicant_Income': [0],
            'Loan_Amount': [300],
            'Loan_Amount_Term': [360],
            'Credit_History': [1],
            'Gender_Male': [1],
            'Married_Yes': [0],
            'Education_Graduate': [1],
            'Self_Employed_Yes': [0],
            'Property_Area': [1]
        })

        # Execute the load command
        app.frames['main_page'].open_command()

        # Verify results
        mock_read.assert_called_once()
        mock_msg.showinfo.assert_called_with("Success", "CSV file loaded successfully!")
        assert not app.frames['main_page'].input_data.empty

def test_prediction_flow(app):
    """Test complete prediction workflow"""
    with patch('pandas.read_csv') as mock_read, \
         patch('src.prediction.predict_loan_status') as mock_pred:

        # Setup mock data
        mock_read.return_value = pd.DataFrame({
            'Applicant_Income': [30000],
            'Coapplicant_Income': [0],
            'Loan_Amount': [300],
            'Loan_Amount_Term': [360],
            'Credit_History': [1],
            'Gender_Male': [1],
            'Married_Yes': [0],
            'Education_Graduate': [1],
            'Self_Employed_Yes': [0],
            'Property_Area': [1]
        })
        mock_pred.return_value = pd.DataFrame({'Eligibility': ['Eligible']})

        # Execute workflow
        main_page = app.frames['main_page']
        main_page.open_command()
        main_page.check_eligible()

        # Verify predictions
        mock_pred.assert_called_once()
        result_text = main_page.controller.children['!resultdialog'].textbox.get("1.0", "end")
        assert 'Eligible' in result_text

def test_manual_entry_page_loads(manual_entry_page):
    """Test if the manual entry page initializes properly"""
    assert manual_entry_page.winfo_exists()

def test_manual_entry_validation(manual_entry_page):
    """Test the validation of numeric fields in the manual entry page"""
    # Set invalid data
    manual_entry_page.entries["Applicant Income"].set("not a number")
    manual_entry_page.entries["Loan Term"].set("1000")

    # Trigger validation
    manual_entry_page.validate_numeric("Applicant Income")
    manual_entry_page.validate_numeric("Loan Term")

    # Assert that the submit button is disabled due to invalid data
    assert manual_entry_page.submit_button['state'] == 'disabled'

    # Set valid data
    manual_entry_page.entries["Applicant Income"].set("30000")
    manual_entry_page.entries["Loan Term"].set("360")

    # Trigger validation
    manual_entry_page.validate_numeric("Applicant Income")
    manual_entry_page.validate_numeric("Loan Term")

    # Assert that the submit button is enabled due to valid data
    assert manual_entry_page.submit_button['state'] == 'normal'

def test_manual_entry_submission(manual_entry_page):
    """Test the manual entry data submission"""
    # Set valid manual data
    manual_entry_page.entries["Applicant Income"].set("30000")
    manual_entry_page.entries["Co-applicant Income"].set("0")
    manual_entry_page.entries["Loan Amount"].set("300")
    manual_entry_page.entries["Loan Term"].set("360")
    manual_entry_page.entries["Credit History"].set("Good")
    manual_entry_page.entries["Gender"].set("Male")
    manual_entry_page.entries["Married"].set("No")
    manual_entry_page.entries["Education"].set("Graduate")
    manual_entry_page.entries["Self Employed"].set("No")
    manual_entry_page.entries["Property Area Type"].set("Urban")

    # Execute save_entry method (submission)
    with patch('src.gui.gui_5_0.messagebox') as mock_msg, \
         patch('src.gui.gui_5_0.filedialog.asksaveasfilename') as mock_save:

        # Mock save file dialog response
        mock_save.return_value = "test_manual_entry.csv"

        # Save entry
        manual_entry_page.save_entry()

        # Verify the success message
        mock_msg.showinfo.assert_called_with("Success", "Data saved to a new file!")

def test_result_dialog_display(app):
    """Test if the result dialog displays correctly after prediction"""
    with patch('src.prediction.predict_loan_status') as mock_pred:
        mock_pred.return_value = pd.DataFrame({'Eligibility': ['Eligible']})

        # Trigger the prediction flow
        main_page = app.frames['main_page']
        main_page.open_command()
        main_page.check_eligible()

        # Get the result dialog and verify the displayed text
        result_dialog = app.children['!resultdialog']
        result_text = result_dialog.textbox.get("1.0", "end")
        assert 'Eligible' in result_text
