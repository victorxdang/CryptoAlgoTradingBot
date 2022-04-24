from matplotlib.pyplot import plot
import pandas as pd
import numpy as np

from Source.Kraken import Kraken

class BaseStrategy():

    def __init__(self):
        self.kraken = Kraken()

    def run(self, pair: str, timeframe: int, plot_results: bool):

        # get data from Kraken
        self.dataframe = self.kraken.get_ohlcv_data(pair, timeframe)

        # initialize default values
        self.dataframe["signal"] = 0.0
        self.dataframe["stoploss"] = 0.0

        # call creation of indicator and signals functions
        self.dataframe = self.create_indicators(self.dataframe, pair)
        self.dataframe, self.predictions_dataframe = self.set_signals(self.dataframe, pair)

        # plot results if user decided to do so
        if plot_results:
            self.plot_results(self.dataframe, pair)


    """
    Below functions are to be overwritten by user strategies.
    """

    def create_indicators(self, dataframe: pd.DataFrame, pair: str):
        # to be overwritten by strategy
        return dataframe

    def set_signals(self, dataframe: pd.DataFrame, pair: str):
        # to be overwritten by strategy
        return dataframe

    def plot_results(self, dataframe: pd.DataFrame, pair: str):
        # to be overwritten by strategy
        pass
