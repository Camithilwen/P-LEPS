import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# basic data preprocessing, can be better oop and put into a differnt file if needed
data = pd.read_csv("model/dataset.csv")
data = data.drop(columns=["Loan_ID"])  # drop the Loan_ID column, not needed for training
data = pd.get_dummies(data, drop_first=True) # one-hot encode categorical variables, drop_first=True to avoid dummy variable trap

print(data.head())
print(data.shape)   

y = data["Loan_Status_Y"].astype(int) 
X = data.drop(columns=["Loan_Status_Y"])

scaler = StandardScaler() # standardize the data, mean = 0, std = 1, might use MinMaxScaler() instead
# scaler = MinMaxScaler() # scale the data to a range, might use StandardScaler() instead
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # 80% training, 20% testing can be changed

# deep neural network
model = Sequential([
    # input layer
    Dense(256, activation='relu', input_shape=(X_train.shape[1],)), # 256 is the number of neurons, can be changed
    # hidden layers
    BatchNormalization(), # normalizes the input layer
    Dropout(0.5), # dropout rate, can be changed

    Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    BatchNormalization(),
    Dropout(0.3),

    Dense(64, activation='relu'),
    BatchNormalization(),
    Dropout(0.3),

    Dense(32, activation='relu'),
    BatchNormalization(),
    Dropout(0.2),

    Dense(1, activation='sigmoid')  # binary classification
])

# compile
model.compile(optimizer=Adam(learning_rate=0.001), # learning rate is .001, can be changed
              loss='binary_crossentropy',
              metrics=['accuracy'])

# train
model.summary()
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=1) # hyperparameters, epochs = 50, batch_size = 32, can be changed

# evalutate
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

model.save("lenn1.0.h5")

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