import unittest
import pandas as pd
import re
from dotenv import load_dotenv
import os

from API.KrakenRequests import KrakenRequests


class TestKrakenRequests(unittest.TestCase):

    # The following parameters below can be changed
    asset_fiat = "USD"
    asset_crypto = "BTC"
    crypto_method = "Bitcoin"
    pair = "BTC/USD"
    asset_list = ['BTC', 'ETH', 'ADA', 'DOT', 'USD']
    assetpair_list = ['BTC/USD', 'ETH/USD', 'ADA/USD', 'DOT/USD']

    timeframe = "1h"
    oder_book_count = 10
    timestamp = "20211201 00:00:00"


    def setUp(self):
        load_dotenv(dotenv_path = "../.env")

        self.test_key = os.getenv("test_key")
        self.test_secret = os.getenv("test_secret")
        self.kraken = KrakenRequests()

    def assertNoError(self, result):
        """
        Usually, the Kraken API will return a dictionary of values when sending a request to the server.
        But for errors, it will return a list of error messages (string). Each error message will be in
        the format of: ['E<error>:<error_message>']

        This function will assert whether or not the regular expression matches an error message. Note
        that the server could return multiple error messages, but for testing purposes, it will check
        if there is ANY error.
        """

        print(result)

        if type(result) is list and len(result) > 0:
            test_result = result[0]

            if type(test_result) is str:
                match = re.match(r"E.*:.*", test_result)
                self.assertEqual(match, None, f"Error Received From Server:\n{test_result}")

    def get_timestamp(self, time: str):
        return pd.Timestamp(time).timestamp()

#==================================================================================================#
#
# The below functions will be for public endpoint requests.
#
#==================================================================================================#

    def test_get_server_time(self):
        self.assertNoError(self.kraken.get_server_time(False))

    def test_get_system_status(self):
        self.assertNoError(self.kraken.get_system_status())

    def test_get_asset_info(self):
        self.assertNoError(self.kraken.get_asset_info(self.asset_list))

    def test_get_asset_pairs(self):
        self.assertNoError(self.kraken.get_asset_pairs(self.assetpair_list))

    def test_get_ticker_info(self):
        self.assertNoError(self.kraken.get_ticker_info(self.pair))

    def test_get_ohlcv_data(self):
        self.assertNoError(self.kraken.get_ohlcv_data(self.pair, self.timeframe))

    def test_get_order_book(self):
        self.assertNoError(self.kraken.get_order_book(self.pair))

    def test_get_recent_trades(self):
        unix_time = self.get_timestamp(self.timestamp)
        self.assertNoError(self.kraken.get_recent_trades(self.pair, unix_time))

    def test_get_recent_spread(self):
        unix_time = self.get_timestamp(self.timestamp)
        self.assertNoError(self.kraken.get_recent_spreads(self.pair, unix_time))


#==================================================================================================#
#
# The below functions will be for private user data enpoint requests.
#
#==================================================================================================#

    def test_get_account_balance(self):
        self.assertNoError(self.kraken.get_account_balance(self.test_key, self.test_secret))

    def test_get_trade_balance(self):
        self.assertNoError(self.kraken.get_trade_balance(self.test_key, self.test_secret, self.asset_fiat))

    def test_get_open_orders(self):
        self.assertNoError(self.kraken.get_open_orders(self.test_key, self.test_secret))

    def test_get_closed_orders(self):
        self.assertNoError(self.kraken.get_closed_orders(self.test_key, self.test_secret))

    def test_query_order_info(self):
        id = 'OXRZVQ-EGEBV-ZPEU7S'
        self.assertNoError(self.kraken.query_order_info(self.test_key, self.test_secret, id))

    def test_get_trades_history(self):
        self.assertNoError(self.kraken.get_trades_history(self.test_key, self.test_secret))

    def test_query_trades_info(self):
        id = ['T2BRYZ-STOYF-667JE2', 'T4ZTIL-QK5UR-NETXMO']
        #id = 'T2BRYZ-STOYF-667JE2'
        self.assertNoError(self.kraken.query_trades_info(self.test_key, self.test_secret, id))

    def test_get_open_positions(self):
        # currently don't have any open positions in this account, needs testing in the future.
        id = ''
        self.assertNoError(self.kraken.get_open_positions(self.test_key, self.test_secret, id))

    def test_get_ledgers_info(self):
        self.assertNoError(self.kraken.get_ledgers_info(self.test_key, self.test_secret))

    def test_query_ledgers(self):
        #id = ['LAZ3U4-T66NW-BYCTTN', 'LQZ5TN-K7EHZ-565IFG']
        id = 'LAZ3U4-T66NW-BYCTTN'
        self.assertNoError(self.kraken.query_ledgers(self.test_key, self.test_secret, id))

    def test_get_trade_volume(self):
        self.assertNoError(self.kraken.get_trade_volume(self.test_key, self.test_secret, self.pair))

    def test_request_export_report(self):
        report = 'trades'
        descr = 'Test Report'
        self.assertNoError(self.kraken.request_export_report(self.test_key, self.test_secret, report, descr))

    def test_get_export_report_status(self):
        report = 'trades'
        self.assertNoError(self.kraken.get_export_report_status(self.test_key, self.test_secret, report))

    def test_retrieve_data_export(self):
        id = 'KEQY'
        file_name = 'TestFile'
        self.assertNoError(self.kraken.retrieve_data_export(self.test_key, self.test_secret, id, file_name))

    def test_delete_export_report(self):
        id = 'KEQY'
        type = 'delete'
        self.assertNoError(self.kraken.delete_export_report(self.test_key, self.test_secret, id, type))


#==================================================================================================#
#
# The below functions will be for private user trading endpoint requests.
#
#==================================================================================================#

    def test_add_order(self):
        type = 'buy'
        order_type = 'limit'
        price = '10000'
        volume = 0.005
        validate = True # ONLY CHANGE THIS IF YOU KNOW WHAT YOU'RE DOING!
        
        self.assertNoError(self.kraken.add_order(api_key = self.test_key, api_secret = self.test_secret, pair = self.pair, type = type, order_type = order_type, volume = volume, price = price, validate = validate))

    def test_cancel_order(self):
        id = ''
        self.assertNoError(self.kraken.cancel_order(self.test_key, self.test_secret, id))

    def test_cancel_all_orders(self):
        self.assertNoError(self.kraken.cancel_all_orders(self.test_key, self.test_secret))

    def test_cancel_all_orders_after_x(self):
        timeout = 10 # seconds
        self.assertNoError(self.kraken.cancel_all_orders_after_x(self.test_key, self.test_secret, timeout))


if __name__ == '__main__':
    unittest.main()