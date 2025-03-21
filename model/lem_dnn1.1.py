import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# basic data preprocessing, can be better oop and put into a differnt file if needed
data = pd.read_csv("model/dataset.csv")
data = data.drop(columns=["Loan_ID"])  # drop the Loan_ID column, not needed for training
data = pd.get_dummies(data, drop_first=True) # one-hot encode categorical variables, drop_first=True to avoid dummy variable trap
data = data.dropna() # drop rows with missing values, can be better to fill with mean or median

#print(data.head())
#print(data.shape)   

y = data["Loan_Status_Y"].astype(int) 
X = data.drop(columns=["Loan_Status_Y"])

scaler = StandardScaler() # standardize the data, mean = 0, std = 1, might use MinMaxScaler() instead
# scaler = MinMaxScaler() # scale the data to a range, might use StandardScaler() instead
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # 80% training, 20% testing can be changed

#print(y_train.value_counts())
#print(y_test.value_counts())

# SMOTE to fix data imbalance
smote = SMOTE(sampling_strategy='auto', random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print("New Class Distribution:", np.bincount(y_train_resampled))

# random forest to see if it can do better and for feature importance
rf_model = RandomForestClassifier()
rf_model.fit(X_train_resampled, y_train_resampled)

feature_importances = pd.Series(rf_model.feature_importances_, index=data.drop(columns=["Loan_Status_Y"]).columns)
print(feature_importances.sort_values(ascending=False))

rf_y_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_y_pred)
print(f"Random Forest Test Accuracy: {rf_accuracy * 100:.2f}%")

# deep neural network
model = Sequential([
    # input layer
    Dense(256, activation='relu', input_shape=(X_train.shape[1],)), # 256 is the number of neurons, can be changed
    # hidden layers
    BatchNormalization(), # normalizes the input layer
    Dropout(0.6), # dropout rate, can be changed

    Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    BatchNormalization(),
    Dropout(0.4),

    Dense(64, activation='relu'),
    BatchNormalization(),
    Dropout(0.3),

    Dense(32, activation='relu'),
    BatchNormalization(),
    Dropout(0.2),

    Dense(1, activation='sigmoid')  # binary classification
])

# compile
model.compile(optimizer=Adam(learning_rate=0.01), # learning rate is .001, can be changed
              loss='binary_crossentropy',
              metrics=['accuracy'])

# train
model.summary()
history = model.fit(X_train, y_train, epochs=50, batch_size=32, # hyperparameters, epochs = 50, batch_size = 32, can be changed
                    validation_data=(X_test, y_test), 
                    verbose=2) # hyperparameters, epochs = 50, batch_size = 32, can be changed

# evalutate
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

model.save("lenn1.1.keras")

# notes 1.0
# need data set to work with
# testing flexibility of scrum approach with the delay of the model implementation
# basic implementation of a model
# haven't begun to train or test
# haven't begun to perfect hyper parameters

# notes 1.1
# struggled importing the data set and preprocessing
# used get_dummies to one-hot encode categorical variables
# renamed some of the dataframe columns, had to change the refrence in the y variable
# model is trained and tested
# accuracy is 65%
# need to test with more data, more epochs, and/or more hyperparameters
# the *fun* part is just beginning, tweaking the model to get better results. trial and error.
# save model to h5 file
# import h5 file for predictions
# we will need to create a new file for predictions for predictions and data preprocessing, 
# as the model data set and all incoming data points will need to be preprocessed the same way

# notes 1.2
# val accuracy is stuck at 65%
# checked for data imbalance, found imbalance
# trying to fix data imbalance with Class Weights and SMOTE
# SMOTE worked, but class weights didn't
# val acccuracy jumps to 81.13% with loss still dropping
# Trying to use random forest to see if it can do better and for feature importance