import pandas as pd
from pandas import DataFrame
import krakenex
from pykrakenapi import KrakenAPI
import re


class Kraken():
    """
    Description:
        This class will be used to process and parse the data received from server.
    """


    def __init__(self):
        """
        Description:
            Initializes the Kraken class to get info on asset pairs.
        """

        api = krakenex.API()
        self.kraken = KrakenAPI(api, tier = "None", crl_sleep = 1)

    
    def get_tradeable_usd_assets(self) -> DataFrame:
        """
        Description:
            Gets all of the tradeable USD asset pairs.

        Return:
            A dataframe of all USD asset pairs.
        """
        
        pairs = self.kraken.get_tradable_asset_pairs()
        return pairs[pairs["quote"] == "ZUSD"]


    def get_tradeable_usd_asset_names(self) -> list:
        """
        Description:
            Gets only the names (altname column) of the tradeable asset pairs.

        Return:
            A list of the tradeable USD asset pair names.
        """

        return list(self.get_tradeable_usd_assets()["altname"].index)


    def get_ohlcv_data(self, timeframe: int) -> dict:
        """
        Description:
            Gets the OHLCV data from server and parse it into a dataframe.

        Return:
            Returns a dictionary of dataframes of ohlcv data for all pairs.
        """

        dict_df = {}

        for pair in self.get_tradeable_usd_asset_names():
            print(pair)
            ohlc, _ = self.kraken.get_ohlc_data(pair, interval = timeframe, ascending = True)
            dict_df[pair] = ohlc

        return dict_df

    def get_ohlcv_data(self, pair: str, timeframe: int) -> pd.DataFrame:
        """
        Description:
            Gets the OHLCV data from server and parse it into a dataframe.

        Return:
            Returns the dataframe of the given pair.
        """
        
        ohlc, _ = self.kraken.get_ohlc_data(pair, interval = timeframe, ascending = True)
        return ohlc
