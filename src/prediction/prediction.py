from keras.api.models import load_model
import pandas as pd
from ..preprocessing.preprocessing import preprocess_input as pp


def predict_loan_status(input_data):
    '''Predict application outcome using preprocessed data and model file'''
    #Preprocess data
    processed_data, valid_indices = pp(input_data)

    #Load model
    model = load_model("src/model/lenn1.3.keras")

    #Prediction
    predictions = model.predict(processed_data)
    predictions_binary = (predictions > 0.5).astype(int).flatten()
    confidence_scores = predictions.flatten() * 100

    # Add failure reasoning
    failure_reasons = []
    for idx, row in input_data.iterrows():
        reasons = []
        if row["Applicant_Income"] < 3000: reasons.append("Low Income")
        if row["Credit_History"] == 0: reasons.append("Poor Credit History")
        failure_reasons.append("; ".join(reasons) if reasons else "N/A")

    results = pd.DataFrame({
        "Eligibility": ["Eligible" if p > 0.5 else "Not Eligible" for p in predictions],
        "Confidence": [f"{score:.1f}%" for score in confidence_scores],
        "Reasons": failure_reasons
    }, index=valid_indices)
    return results
