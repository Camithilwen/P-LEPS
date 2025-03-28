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

    #Format results
    results = pd.DataFrame({
        "Predicted_Status": predictions_binary,
        "Eligibility": ["Eligible" if p ==1 else "Not Eligible" for p in predictions_binary]
    }, index=valid_indices)

    return results
