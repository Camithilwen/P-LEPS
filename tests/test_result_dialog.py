from unittest.mock import MagicMock, patch
import pytest
from src.gui.gui_5_0 import ResultDialog  

@patch('customtkinter.CTkButton')
@patch('customtkinter.CTkTextbox')
@patch('customtkinter.CTkToplevel')
def test_result_dialog(mock_toplevel, mock_textbox, mock_button):
    parent = MagicMock()
    
    # Mocking the ResultDialog instantiation
    mock_dialog_instance = MagicMock()
    mock_toplevel.return_value = mock_dialog_instance
    
    dialog = ResultDialog(parent, "Eligible")
    
    # Check that the dialog is created with the correct message
    mock_dialog_instance.show.assert_called_once_with("Eligible")
