import pytest
from src.gui.gui_5_0 import mainApp
from unittest.mock import patch, Mock
import pandas as pd
import numpy as np

@pytest.fixture
def app():
    """Fixture to create and destroy the main application"""
    application = mainApp()
    yield application
    application.destroy()

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
