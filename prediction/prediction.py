from tensorflow.keras.models import load_model
import pandas as pd
from preprocessing import preprocessing as pp

model = load_model("model/lem_dnn1.1.h5")

# preprocess...
# pp.check_eligible(gui_data.csv)
# pp.prepprocess(gui_data.csv)

new_data = pd.DataFrame({}) # replace with actual data from preprocessing.py
predictions = model.predict(new_data)
predictions_binary = (predictions > 0.5).astype(int)

new_data["Predicted_Loan_Status"] = predictions_binary

new_data.to_csv("predictions.csv", index=False)

print("Predictions saved to predictions.csv")