import pandas as pd
import numpy as np

from Source.Kraken import Kraken

class BaseStrategy():

    def __init__(self):
        self.kraken = Kraken()

    def set_data(self, pair: str, timeframe: int) -> pd.DataFrame:
        self.dataframe = self.kraken.get_ohlcv_data(pair, timeframe)


    """
    Below functions are to be overwritten by user strategies.
    """

    def create_indicators(self, dataframe: pd.DataFrame, pair: str) -> pd.DataFrame:
        # to be overwritten by strategy
        return dataframe

    def set_buy_signals(self, dataframe: pd.DataFrame, pair: str) -> pd.DataFrame:
        # to be overwritten by strategy
        return dataframe

    def set_sell_signals(self, dataframe: pd.DataFrame, pair: str) -> pd.DataFrame:
        # to be overwritten by strategy
        return dataframe
