import pandas as pd
import numpy as np


class BaseStrategy():

    def run(self):
        print(f"Running")
        pass


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