import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from joblib import load

def preprocess_input(data):
    """Replicate preprocessing from model training using saved artifacts."""
    # Drop Loan_ID if present
    data = data.drop(columns=["Loan_ID"], errors="ignore")

    # Load training columns and scaler (saved after training)
    training_columns = pd.read_csv("src/preprocessing/training_columns.csv")["columns"].tolist()
    scaler = load("scaler.joblib")  # Saved from training

    # One-hot encode (ensure same as training)
    data = pd.get_dummies(data, drop_first=True)

    print(data.columns)
    

    # Align columns with training data (add missing, drop extras)
    for col in training_columns:
        if col not in data.columns:
            data[col] = 0
    data = data[training_columns]

    # Drop rows with NA (mimic training's dropna())
    data = data.dropna()

    # Scale using the same scaler
    scaled_data = scaler.transform(data)

    return scaled_data, data.index  # Return valid indices
