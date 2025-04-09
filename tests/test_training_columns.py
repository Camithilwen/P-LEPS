import pytest
import pandas as pd
from src.preprocessing.preprocessing import preprocess_input

def test_preprocess_valid_data():
    """Test preprocessing with valid input"""
    data = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [4, 5, 6]})
    result = preprocess_input(data)
    
    assert result.shape == (3, 2)  
    assert result['feature1'].isnull().sum() == 0  

def test_preprocess_invalid_data():
    """Test preprocessing with invalid data"""
    with pytest.raises(ValueError):
        preprocess_input(None) 
