from sys import displayhook
from tkinter.tix import DisplayStyle
from sklearn.naive_bayes import ComplementNB
import requests
import urllib.parse
import hashlib
import json
import pandas as pd
import numpy as np
from pandas.tseries.offsets import DateOffset
from sklearn import svm
from sklearn import naive_bayes
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import krakenex
from pykrakenapi import KrakenAPI

api = krakenex.API()
k = KrakenAPI(api, tier="None", crl_sleep=.5)

pairs1 = input("Which crypto?")

ohlc = k.get_ohlc_data(pairs1, interval=1440, ascending=True)
ohlc[0].head()


# SMA Windows
short_window = int(input("Fast SMA:"))
long_window = int(input("Slow SMA"))


ohlc[0]['Fast SMA'] = ohlc[0]['close'].rolling(short_window).mean()
displayhook(ohlc[0].tail())

ohlc[0]['Slow SMA'] = ohlc[0]['close'].rolling(long_window).mean()
# DisplayStyle(ohlc[0].tail())


# Data Training and Testing DataSets

# Calculate the daily returns using the closing prices and the pct_change function
ohlc[0]["Actual Returns"] = ohlc[0]["close"].pct_change()

# Dropping the NaN value from the DataFrame
ohlc = ohlc[0].dropna()


# Initialize the new signal
ohlc["Signal"] = 0.0

# When Actual Returns are greater than 0, generate signal to buy crypto
ohlc.loc[(ohlc["Actual Returns"] >= 0), "Signal"] = 1.0
ohlc.loc[(ohlc["Actual Returns"] < 0), "Signal"] = -1.0

# Disaplying the data
# display(ohlc)


# Scaling the Features using StandardScaler

# Creating a X dataframe with the fast and slow columns
X = ohlc[["Fast SMA", "Slow SMA"]].shift().dropna()

# Creating tha target set by selecting the Signal column
y = ohlc["Signal"]

# Selecting the training start date
training_start = X.index.min()

# Selecting the end of the training and setting the offset to 12 months
training_end = X.index.min() + DateOffset(months=12)


# Genereating the X_train and y_train DataFrames
X_train, y_train = X.loc[training_start:training_end], y.loc[training_start:training_end]

# Generating the X_test and y_test DataFrames
X_test, y_test = X.loc[training_end +
                       DateOffset(hours=1):], y.loc[training_end+DateOffset(hours=1):]


# Scaling and fitting the model
X_scaler = StandardScaler().fit(X_train)

# Transforming tge X_train Aand X_test DataFrame using the X_scaler
X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)


# Using the SVC classifier model
model = svm.SVC().fit(X_train_scaled, y_train)

# Predicting the test set
predictions = model.predict(X_train_scaled)


# Classification Report
SVM_report = classification_report(y_train, predictions)

print(SVM_report)


# Another strategy would be the Naive Bayes Classifier

model = naive_bayes.ComplementNB().fit(X_train, y_train)

predictions = model.predict(X_train)

naive_bayes_report = classification_report(y_train, predictions)

print(naive_bayes_report)
