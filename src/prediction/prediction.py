import numpy as np
import tensorflow as tf
import pandas as pd
import os
import sys

# Get the base path for accessing resources
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

try:
    # For frozen executable
    from src.preprocessing.preprocessing import preprocess_input as pp
except ImportError:
    # For development environment
    from preprocessing.preprocessing import preprocess_input as pp
def predict_loan_status(input_data):
    '''Predict application outcome using preprocessed data and model file'''
    #Preprocess data
    processed_data, valid_indices = pp(input_data)

    #Load model
    model_path = resource_path('lenn1.3.keras')
    model = tf.keras.models.load_model(model_path)

    #Prediction
    predictions = model.predict(processed_data)
    predictions_binary = (predictions > 0.5).astype(int).flatten()
    confidence_scores = predictions.flatten() * 100

    # Add failure reasoning
    failure_reasons = []
    for idx, row in input_data.iterrows():
        reasons = []
        if row["Applicant_Income"] < 3000 and row["Coapplicant_Income"] < 3000: reasons.append("Low Income")
        if row["Credit_History"] == 0: reasons.append("Poor Credit History")
        if row["Applicant_Income"] < 6000 and row["Property_Area"] == 2: reasons.append("Income too low for area")
        failure_reasons.append("; ".join(reasons) if reasons else "N/A")

    results = pd.DataFrame({
        "Eligibility": ["Eligible" if p > 0.5 else "Not Eligible" for p in predictions_binary],
        "Confidence": [f"{score:.1f}%" for score in confidence_scores],
        "Reasons": failure_reasons
    }, index=valid_indices)
    return results
