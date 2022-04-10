import pandas as pd
from pandas import DataFrame
import re


class Kraken():
    """
    Description:
        This class will be used to process and parse the data received from server.
    """


    def __init__(self, pairlist: list, timeframe: str, api_key: str = None, api_secret: str = None):
        """
        Description:
            Initializes the Kraken class to get info and make orders on Kraken
        
        Paramters:
            pairlist: (required) the list of list of tradeable pairs where [0] = pair whitelist and [1] = pair blacklist.
            timeframe: (required) the timeframe to use, can be a single timeframe (str), or multiple timeframes (list).
            api_key: (optional) the account holder's API key, please only allow trades/view permissions only! Since this paramter is optional, then no API requiring authentication can be used if no key is provided!
            api_secret: (optional) the account holder's API secret, KEEP THIS SECRET SAFE! Since this paramter is optional, then no API requiring authentication can be used if no secret is provided!

        Note(s):
            API key and secret are not needed if no account info is going to be accessed.
        """

        self.pairlist = pairlist
        self.timeframe = timeframe
        self.api_key = api_key
        self.api_secret = api_secret

    
    def get_ohlcv_data(self) -> DataFrame:
        """
        Description:
            Gets the OHLCV data from server and parse it into a dataframe.

        Return:
            Returns either a list of dataframes of ohlcv data for all pairs or a single dataframe if only one pair is specified.
        """

        

        # [0] = pair whitelist
        for pair in self.pairlist[0]:



