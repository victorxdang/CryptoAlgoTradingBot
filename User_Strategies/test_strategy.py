import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from finta import TA

from Source.BaseStrategy import BaseStrategy


class test_strategy(BaseStrategy):
    
    def __init__(self):
        BaseStrategy.__init__(self)

    def create_indicators(self, dataframe: pd.DataFrame, pair: str) -> pd.DataFrame:

        dataframe["SMA_Fast"] = TA.SMA(dataframe, 20)
        dataframe["SMA_Slow"] = TA.SMA(dataframe, 50)

        return dataframe

    def set_buy_signals(self, dataframe: pd.DataFrame, pair: str) -> pd.DataFrame:
        
        buy_signal = (dataframe["SMA_Fast"] > dataframe["SMA_Slow"])
        dataframe.loc[buy_signal, "buy"] = 1

        return dataframe

    def set_sell_signals(self, dataframe: pd.DataFrame, pair: str) -> pd.DataFrame:
        
        sell_signal = (dataframe["SMA_Fast"] < dataframe["SMA_Slow"])
        dataframe.loc[sell_signal, "sell"] = 1

        return dataframe

    def plot_results(self, dataframe: pd.DataFrame, pair: str):
        fig = plt.figure(figsize = (25, 10))
        ax1 = fig.add_subplot()
        dataframe["close"].plot(ax = ax1, color = "r", lw = 2)
        dataframe[["SMA_Fast", "SMA_Slow"]].plot(ax = ax1, lw = 2)

        #df_buy = dataframe[dataframe["buy"] == 1]
        #df_sell = dataframe[dataframe["sell"] == 1]
        #ax1.plot(df_buy.index, df_buy, "^", color = "m")
        #ax1.plot(df_sell.index, df_sell, "v", color = "k")

        plt.xlabel("Date")
        plt.ylabel("Price in USD")
        plt.title(f"Backtest Results for {pair}")
        plt.show()
