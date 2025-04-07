
import pytest
from src.gui.gui_5_0 import mainApp, manual_entry, main_page, ResultDialog
from unittest.mock import patch, Mock, MagicMock, call
import pandas as pd
import numpy as np
import tkinter as tk
import customtkinter as ctk
from src.prediction.prediction import predict_loan_status
import importlib

@pytest.fixture
def app():
    """Fixture to create and destroy the main application"""
    with patch('src.gui.gui_5_0.pd.read_csv') as mock_read_csv:
        mock_read_csv.return_value = pd.DataFrame({
            0: [
                'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount', 'Loan_Amount_Term',
                'Credit_History', 'Gender_Male', 'Married_Yes', 'Education_Graduate',
                'Self_Employed_Yes', 'Property_Area'
            ]
        })
        application = mainApp()
        yield application
        application.destroy()

@pytest.fixture
def populated_manual_entry(app):
    """Fixture to populate manual entry form with valid test data"""
    manual_entry_instance = app.frames[manual_entry]

    # Set form values
    manual_entry_instance.entries["Applicant Income"].set("5000")
    manual_entry_instance.entries["Co-applicant Income"].set("2000")
    manual_entry_instance.entries["Loan Amount"].set("300")
    manual_entry_instance.entries["Loan Term"].set("360")
    manual_entry_instance.entries["Gender"].set("Male")
    manual_entry_instance.entries["Married"].set("Yes")
    manual_entry_instance.entries["Education"].set("Graduate")
    manual_entry_instance.entries["Credit History"].set("Good")
    manual_entry_instance.entries["Self Employed"].set("Yes")
    manual_entry_instance.entries["Property Area Type"].set("Urban")

    # Update validation status
    for field in manual_entry_instance.numeric_fields:
        manual_entry_instance.valid_inputs[field] = True

    return manual_entry_instance

def test_csv_loading(app):
    """Test CSV loading functionality"""

    with patch('src.gui.gui_5_0.filedialog.askopenfilename') as mock_askopen, \
         patch('pandas.read_csv', side_effect=lambda path, **kwargs:
               mock_data if path != "src/preprocessing/training_columns.csv"
               else pd.DataFrame({0: mock_data.columns.tolist()})) as mock_read, \
        patch('src.gui.gui_5_0.messagebox') as mock_msg:
        # Setup mock DataFrame
        mock_data = pd.DataFrame({
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

        # Configure mocks
        mock_askopen.return_value = "/dummy/path.csv"
        mock_read.return_value = mock_data

        # Get main page instance
        main_page_instance = app.frames[main_page]

        # Execute CSV loading command
        main_page_instance.open_command()

        # Verify results
        assert not main_page_instance.input_data.empty
        mock_msg.showinfo.assert_called_once_with("Success", "CSV file loaded successfully!")
        pd.testing.assert_frame_equal(main_page_instance.input_data, mock_data)

def test_prediction_flow(app):
    """Test complete prediction workflow"""
    # Get main page instance and execute flow
    main_page_instance = app.frames[main_page]
    with patch('src.gui.gui_5_0.filedialog.askopenfilename') as mock_askopen, \
        patch('pandas.read_csv') as mock_read, \
        patch('src.prediction.prediction.predict_loan_status') as mock_pred, \
        patch('src.preprocessing.preprocessing.load') as mock_load, \
        patch('src.preprocessing.preprocessing.pd.read_csv') as mock_train_cols, \
        patch('src.gui.gui_5_0.ResultDialog') as mock_dialog, \
        patch.object(main_page_instance, 'check_eligible', wraps=main_page_instance.check_eligible) as wrapped_check:

        # Mock training columns to match test data
        mock_train_cols.return_value = pd.DataFrame({
            0: [
                'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount',
                'Loan_Amount_Term', 'Credit_History', 'Gender_Male',
                'Married_Yes', 'Education_Graduate', 'Self_Employed_Yes',
                'Property_Area'
            ]
        })

        # Create mock DataFrame with correct structure
        mock_data = pd.DataFrame({
            'Applicant_Income': [30000.0],
            'Coapplicant_Income': [0.0],
            'Loan_Amount': [300.0],
            'Loan_Amount_Term': [360.0],
            'Credit_History': [1.0],
            'Gender_Male': [1.0],
            'Married_Yes': [0.0],
            'Education_Graduate': [1.0],
            'Self_Employed_Yes': [0.0],
            'Property_Area': [1.0]
        })

        # Configure mocks
        mock_askopen.return_value = "/dummy/path.csv"
        mock_read.return_value = mock_data
        mock_pred.return_value = pd.DataFrame({'Eligibility': ['Eligible']})
        mock_load.return_value = Mock(transform=lambda x: x)  # Mock scaler


        # 1. Load CSV data
        main_page_instance.open_command()
        main_page_instance.input_data = mock_data

        # 2. Trigger prediction
        main_page_instance.check_eligible()

        # Verify prediction call with expected columns
        expected_columns = mock_train_cols.return_value[0].tolist()
        pd.testing.assert_frame_equal(
            mock_pred.call_args[0][0][expected_columns],
            mock_data[expected_columns]
        )
        mock_pred.assert_called_once()
        mock_dialog.assert_called_once()
def test_check_eligibility_with_manual_data(app):
    """Test check eligibility with manual data"""
    # Get the main page instance
    main_page_instance = app.frames[main_page]

    # Create the test data first
    manual_data = pd.DataFrame({
        'Applicant_Income': [30000],
        'Coapplicant_Income': [0],
        'Loan_Amount': [200],
        'Loan_Amount_Term': [240],
        'Credit_History': [0],
        'Gender_Male': [0],
        'Married_Yes': [0],
        'Education_Graduate': [0],
        'Self_Employed_Yes': [1],
        'Property_Area': [0]
    })

    # Set up the test data on the main page
    main_page_instance.input_data = pd.DataFrame()
    main_page_instance.manual_entry_data = manual_data

    # Now patch at more specific locations - try all of these approaches
    with patch('src.gui.gui_5_0.predict_loan_status') as mock_pred, \
         patch('src.gui.gui_5_0.ResultDialog') as mock_dialog:

        # Configure the mock to return our test result
        mock_pred.return_value = pd.DataFrame({'Eligibility': ['Not Eligible']})

        # Call the method under test
        main_page_instance.check_eligible()

        # Assert that the mock was called
        mock_pred.assert_called_once()
        mock_dialog.assert_called_once()

def test_manual_entry_navigation(app):
    """Test navigation to manual entry page and back"""
    main_page_instance = app.frames[main_page]
    manual_entry_instance = app.frames[manual_entry]

    with patch.object(app, 'show_frame') as mock_show:
        main_page_instance.manual_button.invoke()
        mock_show.assert_called_once_with(manual_entry)

    with patch.object(app, 'show_frame') as mock_show:
        manual_entry_instance.back_button.invoke()
        mock_show.assert_called_once_with(main_page)

def test_manual_entry_initial_state(app):
    """Test initial state of manual entry form"""
    manual_entry_instance = app.frames[manual_entry]
    assert manual_entry_instance.submit_button.cget("state") == "disabled"
    for field in manual_entry_instance.numeric_fields:
        assert not manual_entry_instance.valid_inputs[field]

def test_numeric_field_validation(app):
    """Test validation of numeric fields"""
    manual_entry_instance = app.frames[manual_entry]
    test_cases = [
        ("Applicant Income", "abc", False),
        ("Applicant Income", "", False),
        ("Applicant Income", "123.45", True),
        ("Co-applicant Income", "0", True),
        ("Co-applicant Income", "-100", True),
        ("Loan Amount", "abc123", False),
        ("Loan Amount", "500", True),
        ("Loan Term", "5", False),
        ("Loan Term", "400", False),
        ("Loan Term", "360", True),
    ]

    for field, value, expected_valid in test_cases:
        manual_entry_instance.entries[field].set(value)
        manual_entry_instance.validate_numeric(field)
        assert manual_entry_instance.valid_inputs[field] == expected_valid

@patch('tkinter.filedialog.asksaveasfilename')
@patch('tkinter.messagebox.askyesno')
@patch('pandas.read_csv')
def test_save_entry_new_file(mock_read_csv, mock_askyesno, mock_asksaveasfilename, populated_manual_entry):
    """Test saving manual entry data to a new file"""

    #Populate test fields
    manual_entry_instance = populated_manual_entry

    mock_askyesno.return_value = False
    mock_asksaveasfilename.return_value = "new_file.csv"
    mock_read_csv.return_value = pd.DataFrame({
        0: [
            'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount', 'Loan_Amount_Term',
            'Credit_History', 'Gender_Male', 'Married_Yes', 'Education_Graduate',
            'Self_Employed_Yes', 'Property_Area'
        ]
    })

    manual_entry_instance.save_entry()
    mock_read_csv.assert_called_once()

@patch('tkinter.filedialog.askopenfilename')
@patch('tkinter.messagebox.askyesno')
@patch('pandas.read_csv')
def test_save_entry_append(mock_read_csv, mock_askyesno, mock_askopenfilename, populated_manual_entry):
    """Test appending manual entry data to an existing file"""

    #Populate test fields
    manual_entry_instance = populated_manual_entry

    mock_askyesno.return_value = True
    mock_askopenfilename.return_value = "existing_file.csv"
    mock_read_csv.side_effect = [
        pd.DataFrame({0: [
            'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount', 'Loan_Amount_Term',
            'Credit_History', 'Gender_Male', 'Married_Yes', 'Education_Graduate',
            'Self_Employed_Yes', 'Property_Area'
        ]}),
        pd.DataFrame({
            'Applicant_Income': [40000],
            'Coapplicant_Income': [20000],
            'Loan_Amount': [400],
            'Loan_Amount_Term': [360],
            'Credit_History': [1],
            'Gender_Male': [1],
            'Married_Yes': [1],
            'Education_Graduate': [1],
            'Self_Employed_Yes': [0],
            'Property_Area': [1]
        })
    ]

    manual_entry_instance.save_entry()
    assert mock_read_csv.call_count == 2

def test_user_cancels_file_operations(populated_manual_entry):
    """Test handling when user cancels file operations"""

    manual_entry_instance = populated_manual_entry

    with patch('tkinter.messagebox.askyesno', return_value=True), \
         patch('tkinter.filedialog.askopenfilename', return_value=""), \
         patch('pandas.read_csv') as mock_read_csv:

        mock_read_csv.return_value = pd.DataFrame({
            0: [
                'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount', 'Loan_Amount_Term',
                'Credit_History', 'Gender_Male', 'Married_Yes', 'Education_Graduate',
                'Self_Employed_Yes', 'Property_Area'
            ]
        })
        manual_entry_instance.save_entry()

@patch('src.gui.gui_5_0.ResultDialog')
@patch('customtkinter.CTkButton')
@patch('customtkinter.CTkTextbox')
@patch('customtkinter.CTkToplevel')
def test_result_dialog(mock_toplevel, mock_textbox, mock_button, mock_dialog):
    """Test result dialog without GUI window creation"""
    # Fix decorator order and parameter names

    # Mock dialog methods
    mock_instance = MagicMock()
    mock_dialog.return_value = mock_instance

    # Create a mock parent window
    parent = MagicMock(spec=ctk.CTk)
    parent.tk = MagicMock()

    # Simulate creating the dialog
    dialog = ResultDialog(parent, "Eligible")

    # Verify dialog initialization
    mock_dialog.assert_called_once_with(parent, "Eligible")

    # Verify textbox configuration
    mock_instance.textbox.insert.assert_called_once_with("1.0", "Eligible")
    mock_instance.textbox.configure.assert_called_once_with(state="disabled")

    # Simulate closing the dialog
    dialog.destroy()

def test_csv_loading_missing_columns(app):
    """Test CSV loading with missing required columns"""
    with patch('src.gui.gui_5_0.filedialog.askopenfilename') as mock_askopen, \
         patch('pandas.read_csv') as mock_read, \
         patch('src.gui.gui_5_0.messagebox') as mock_msg:

        # Mock data with missing columns
        mock_data = pd.DataFrame({'Wrong_Column': [1]})
        mock_askopen.return_value = "/dummy/path.csv"
        mock_read.return_value = mock_data

        main_page_instance = app.frames[main_page]
        main_page_instance.open_command()

        # Verify error message for missing columns
        mock_msg.showerror.assert_called_once()
        assert main_page_instance.input_data.empty

def test_csv_loading_exception(app):
    """Test error handling during CSV loading"""
    with patch('src.gui.gui_5_0.filedialog.askopenfilename') as mock_askopen, \
         patch('pandas.read_csv', side_effect=Exception("File error")), \
         patch('src.gui.gui_5_0.messagebox') as mock_msg:

        mock_askopen.return_value = "/dummy/path.csv"
        main_page_instance = app.frames[main_page]
        main_page_instance.open_command()

        mock_msg.showerror.assert_called_once_with("Error", "An error occurred while loading the file: File error")


@patch('pandas.read_csv', side_effect=FileNotFoundError)
def test_save_entry_invalid_training_columns(mock_read, populated_manual_entry):
    """Test handling missing training_columns.csv"""
    manual_entry_instance = populated_manual_entry
    with patch('src.gui.gui_5_0.messagebox.showerror') as mock_error:
        manual_entry_instance.save_entry()
        mock_error.assert_called_once_with("Error", "Required training columns file not found")

@patch('tkinter.filedialog.askopenfilename')
@patch('pandas.read_csv', side_effect=Exception("Read error"))
def test_save_entry_append_failure(mock_read, mock_ask, populated_manual_entry):
    """Test append failure during save"""
    mock_ask.return_value = "existing.csv"
    manual_entry_instance = populated_manual_entry
    with patch('src.gui.gui_5_0.messagebox.showerror') as mock_error:
        manual_entry_instance.save_entry()
        mock_error.assert_called_once_with("Error", "Failed to append:\nRead error")

def test_loan_term_validation(app):
    """Test loan term validation with invalid input"""
    manual_entry_instance = app.frames[manual_entry]
    manual_entry_instance.entries["Loan Term"].set("invalid")
    manual_entry_instance.validate_numeric("Loan Term")
    assert not manual_entry_instance.valid_inputs["Loan Term"]

def test_result_dialog_initialization(app):
    """Test ResultDialog widget configuration"""
    with patch('src.gui.gui_5_0.ctk.CTkToplevel') as mock_toplevel, \
         patch('src.gui.gui_5_0.ctk.CTkTextbox') as mock_textbox, \
         patch('src.gui.gui_5_0.ctk.CTkButton') as mock_button:

        # Configure the mock textbox
        mock_textbox_instance = MagicMock()
        mock_textbox.return_value = mock_textbox_instance

        # Create the dialog
        dialog = ResultDialog(app, "Test Results")

        # Verify the textbox was configured correctly
        mock_textbox_instance.insert.assert_called_once_with("1.0", "Test Results")
        mock_textbox_instance.configure.assert_called_once_with(state="disabled")

def test_main_execution():
    """Test __main__ block execution"""
    with patch('src.gui.gui_5_0.mainApp') as mock_app, \
         patch('src.gui.gui_5_0.__name__', '__main__'):  # Simulate running as __main__

        # Trigger the __main__ block execution
        import src.gui.gui_5_0
        importlib.reload(src.gui.gui_5_0)  # Ensure the module is reloaded

        mock_app.assert_called_once()
        mock_app.return_value.mainloop.assert_called_once()
