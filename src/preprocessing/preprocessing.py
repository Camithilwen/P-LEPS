import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from joblib import load

def preprocess_input(data):
    """Replicate preprocessing from model training using saved artifacts."""
    # Drop Loan_ID if present
    data = data.drop(columns=["Loan_ID"], errors="ignore")

    # Load training columns and scaler (saved after training)
    training_columns = pd.read_csv("src/preprocessing/training_columns.csv", header=None).squeeze().tolist()
    scaler = load("src/preprocessing/scaler.joblib")  # Saved from training

    if "Property_Area" in data.columns:
        data["Property_Area"] = pd.to_numeric(data["Property_Area"], errors="coerce")
    # Check if data already contains dummy columns and no original categoricals
    # If not, one-hot encode (ensure same as training)
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    if not categorical_cols.empty:
        data = pd.get_dummies(data, drop_first=True)

    print(data.columns)

    # Align columns with training data (add missing, drop extras)
    for col in training_columns:
        if col not in data.columns:
            data[col] = 0
    data = data[training_columns]

    # Impute any missing values
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())

#    categorical_cols = data.select_dtypes(exclude=[np.number]).columns
#    data[categorical_cols] = data[categorical_cols].fillna(data[categorical_cols].mode().iloc[0])

    print("\n--- Post Column Alignment ---")
    print("Columns:", data.columns.tolist())
    print("Data Shape:", data.shape)
    print("Data:\n", data.head())

    #Convert DataFrame to NumPy array before scaling
    data_array = data.values

    #Data presence check
    if data.empty:
        raise ValueError("Data is empty after preprocessing")

    # Scale using the same scaler
    scaled_data = scaler.transform(data_array)
    print("Scaled Data Shape:", scaled_data.shape)
    #Data presence checks
    if len(scaled_data) == 0:
        raise ValueError("No valid data to process after preprocessing.")

    if scaled_data.shape[1] != 10: #Count of training columns
        raise ValueError(f"Expected 10 features, got {scaled_data.shape[1]}")

    return scaled_data, data.index  # Return valid indices
