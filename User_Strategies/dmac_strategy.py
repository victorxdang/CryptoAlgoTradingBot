import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import questionary

from pandas.tseries.offsets import DateOffset
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from finta import TA
from Source.BaseStrategy import BaseStrategy


class dmac_strategy(BaseStrategy):
    
    def __init__(self):
        BaseStrategy.__init__(self)

    def create_indicators(self, dataframe: pd.DataFrame, pair: str) -> pd.DataFrame:
        """
        Description:
            Create the indicators for the strategy
        """

        # SMA windows
        fast = float(questionary.text("Enter Fast SMA Length:"))
        slow = float(questionary.text("Enter Slow SMA Length:"))

        # instantiate indicators
        dataframe["SMA_Fast"] = TA.SMA(dataframe, fast)
        dataframe["SMA_Slow"] = TA.SMA(dataframe, slow)

        return dataframe

    def set_signals(self, dataframe: pd.DataFrame, pair: str) -> pd.DataFrame:
        """
        Description:
            Setting the buy and sell signals while applying machine learning.
        """

        # calculate daily returns using closing price and pct_change function
        dataframe["actual_returns"] = dataframe["close"].pct_change()

        # dropping NaN values from the DataFrame
        dataframe.dropna()

        # initialize new signal
        dataframe["signal"] = 0.0

        # when actual_returns are greater than 0, generate signal to buy crypto
        dataframe.loc[(dataframe["actual_returns"] >= 0), "signal"] = 1.0
        dataframe.loc[(dataframe["actual_returns"] < 0), "signal"] = -1.0

        # sisaplying the data
        display(dataframe)


        # Scaling the Features using StandardScaler

        # Creating a X dataframe with the fast and slow columns
        X = dataframe[["SMA_Fast", "SMA_Slow"]].shift().dropna()

        # Creating tha target set by selecting the Signal column
        y = dataframe["signal"]

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


        # Classification Report and Confusion Matrix
        SVM_report = classification_report(y_train, predictions)
        confusion_matrix = confusion_matrix(y_train, predictions)

        print("\nSVM Report:")
        print(SVM_report)
        print("\nConfusion Matrix:")
        print(confusion_matrix)

        return dataframe

    def plot_results(self, dataframe: pd.DataFrame, pair: str):
        """
        Description:
            Plotting the closing price and indicators.
        """

        fig = plt.figure(figsize = (25, 10))
        ax1 = fig.add_subplot()
        dataframe["close"].plot(ax = ax1, color = "r", lw = 2)
        dataframe[["SMA_Fast", "SMA_Slow"]].plot(ax = ax1, lw = 2)

        df_buy = dataframe.loc[dataframe["buy"] == 1, "SMA_Fast"]
        df_sell = dataframe.loc[dataframe["sell"] == 1, "SMA_Fast"]
        ax1.plot(df_buy.index, df_buy, "^", color = "m")
        ax1.plot(df_sell.index, df_sell, "v", color = "k")

        plt.xlabel("Date")
        plt.ylabel("Price in USD")
        plt.title(f"Backtest Results for {pair}")
        plt.show()
