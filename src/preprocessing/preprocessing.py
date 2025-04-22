import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from joblib import load
import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource for PyInstaller or development."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Handle both forward and backward slashes
    path = os.path.join(base_path, *relative_path.split('/'))
    
    # Debugging output
    print(f"Looking for {relative_path} at: {path}")
    if not os.path.exists(path):
        print(f"File not found at {path}")
        print(f"Contents of {os.path.dirname(path)}: {os.listdir(os.path.dirname(path))}")
    
    return path

def preprocess_input(data, strict_validation=True):
    """Replicate preprocessing from model training using saved artifacts."""
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    
    # Debugging output
    print("\n--- Starting Preprocessing ---")
    print(f"Current working directory: {os.getcwd()}")
    if getattr(sys, 'frozen', False):
        print(f"Running in PyInstaller bundle, MEIPASS: {sys._MEIPASS}")
    
    # Create copy to prevent modifying original data
    data = data.copy()

    # Drop Loan_ID if present
    data = data.drop(columns=["Loan_ID"], errors="ignore")

    # Load training columns with multiple fallback paths

    try:
        training_columns = pd.read_csv(resource_path('training_columns.csv'), header=None
        ).squeeze().str.strip().str.replace(" ", "_").str.title().tolist()
        print("Successfully loaded training columns")
        print("Training columns:", training_columns)
    except FileNotFoundError:
        pass

    
    if training_columns is None:
        error_msg = f"Could not find training_columns.csv at any of:\n" + "\n".join(training_col_path)
        print(error_msg)
        raise FileNotFoundError(error_msg)

    # Check for conversion errors
    conversion_errors = []
    for col in data.columns:
        try:
            data[col] = pd.to_numeric(data[col], errors='raise')
        except ValueError:
            conversion_errors.append(col)

    if conversion_errors:
        raise ValueError(f"Invalid numeric value in columns: {conversion_errors}")

    # Strict validation (ensure required columns exist)
    if strict_validation:
        missing_cols = set(training_columns) - set(data.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

    # Convert to numeric types safely
    data = data.apply(pd.to_numeric, errors='coerce')

    # One-hot encoding for unexpected object columns (failsafe)
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        data = pd.get_dummies(data, drop_first=True)

    # Align columns with training structure
    missing_cols = set(training_columns) - set(data.columns)
    extra_cols = set(data.columns) - set(training_columns)

    for col in missing_cols:
        data[col] = 0
    data = data[training_columns]

    # Impute missing values
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())

    # Debugging info
    print("\n--- Post Column Alignment ---")
    print("Columns:", data.columns.tolist())
    print("Data Shape:", data.shape)
    print("Data:\n", data.head())

    # Load scaler with improved error handling
    try:
        scaler_path = resource_path('scaler.joblib')
        print(f"Loading scaler from: {scaler_path}")
        scaler = load(scaler_path)
    except FileNotFoundError:
        print("Warning: scaler.joblib not found, using dummy StandardScaler for testing.")
        scaler = StandardScaler()
        scaler.fit(data)

    # Final structure validation
    if data.shape[1] != len(training_columns):
        raise ValueError(f"Expected {len(training_columns)} features, got {data.shape[1]}")

    scaled_data = scaler.transform(data)
    return scaled_data, data.index