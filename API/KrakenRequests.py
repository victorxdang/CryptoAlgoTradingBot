import requests
import urllib.parse
import hashlib
import hmac
import base64

from API.Endpoints import KrakenEndpoints
from Helper import Utilities as util


class KrakenRequests():
    """
    Description:
        A custom wrapper class for the Kraken API which uses the RESTful API and all known
        functions/methods are implemented in this script. This does not support Kraken Futures
        or WebSockets API, it only supports the Spot Exchange API.

        For each method, there will be some methods with the 'Public' or 'Private' tag 
        added at the start of each description. For 'Public' methods, they do not require the
        user's API or Private key, while 'Private' will require a signature that can be
        obtained by the get_kraken_signature() function.

        Some methods will have the 'Internal' tag on it, those are to be only used within this
        class alone. DO NOT USE THOSE FUNCTIONS EXTERNALLY.
        
        More info about the Kraken API can be found using the following link:
        https://docs.kraken.com/rest/
    """


    def __init__(self):
        self._endpoints = KrakenEndpoints()


#==================================================================================================#
#
# The below functions will be internal functions that the public and private request functions can
# use to simplify its' code.
#
#==================================================================================================#

    def get_request(self, endpoint: str, payload: dict = None):
        """
        Description:
            (Internal) A function used to send a GET request out and parse the data received
            from the server. Depending on the status_code returned, it will either return 
            the message body or the error message. This method should only be used internally
            by this class and should not be used anywhere else.

        Parameters:
            endpoint : (required) the endpoint to use.
            payload : (optional) the extra parameters needed as part of the request.
            get_full_response : (optional) returns the entire response object received from
            server.

        Return:
            Returns whether or not if the request was successful or not and also the 
            result of the request or an error message.
        """

        response = requests.get(self._endpoints.get_public_endpoint(endpoint), params = payload)

        status_code = response.status_code
        response_json = response.json()
        request_success = status_code == 200 and len(response_json['error']) == 0

        if request_success:
            return (request_success, response_json['result'])
        else:
            return (request_success, response_json['error'])

        
    def post_request(self, endpoint: str, payload: dict, api_key: str, api_secret: str,
                     file_save: bool = False, file_name = None):
        """
        Description:
            (Internal) A function used to send a POST request out and parse the data received
            from the server. Depending on the status_code returned, it will either return 
            the message body or the error message. This method should only be used internally
            by this class and should not be used anywhere else. The following request to this
            function will require user authentication, so the api_key and api_secret are
            required to send any POST requests.

        Parameters:
            endpoint : (required) the endpoint to use.
            payload : (required) the extra parameters needed as part of the request.
            api_key : (required) the key of the user.
            api_secret : (required) the secret of the user.
            file_save : (optional) set to True if the request is to save a file instead of json.
            file_name : (optional) the name of the file (required if file_save is set to True).
            get_full_response : (optional) returns the entire response object received from
            server.

        Return:
            Returns whether or not if the request was successful or not and also the 
            result of the request or an error message.
        """

        headers = {}
        headers['API-Key'] = api_key
        headers['API-Sign'] = self.get_kraken_signature(self._endpoints.PRIVATE + endpoint, payload, api_secret)

        response = requests.post(self._endpoints.get_private_endpoint(endpoint),
                                headers = headers, data = payload)
        

        if file_save:
            if file_name is None:
                raise Exception("Filename doesn't exist!")

            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size = 512):
                    # filter out keep-alive new chunks
                    if chunk:
                        f.write(chunk)

            return (True, 'File Saved')

        else:
            status_code = response.status_code
            response_json = response.json()
            request_success = status_code == 200 and len(response_json['error']) == 0

            if request_success:
                return (request_success, response_json['result'])
            else:
                return (request_success, response_json['error'])


    def get_pair_from_result(self, result):
        """
        Description: 
            (Internal) For whatever reason, the Kraken API doesn't like it when 'BTC/USD' is used
            (also occurs for a few other pair names). HOWEVER, IF YOU LOOK AT THE RETURN DATA FROM
            THE API, THAT IS THE EXACT KEY IT RETURNS FOR US TO ACCESS THE DICTIONARY. So we have
            to do this janky method (not really janky, more like an extra step) to get this function
            working... The return value is always a dictionary with 2 keys (the (exact) pair name
            passed to this function and 'last'). STILL THOUGH, WHAT THE FUCK. Also, grabbing the keys
            is done through a for loop because the dictionary may not be ordered. I believe the API
            will always return the data with the pair name first then the 'last' key, but this way is
            less prone to errors.

        Parameters:
            result : (required) the result received from server.

        Return:
            Returns the (proper) pair name.
        """

        pair = None
        for p in result.keys():
            if p != 'last': pair = p

        return pair


    def get_kraken_signature(self, url_path: str, payload: dict, api_secret: str):
        """
        Description:
            (Internal) A function used to create the signature required to authenticate
            certain POST requests. To generate a signature, the private (secret) key,
            nonce, payload and URI are all required by this function. The endcoding and
            signature generation will be done automatically.

        Parameters:
            url_path : (required) the url for the request (not the domain!).
            payload : (required) the data to be sent with the request.
            api_secret : (required) the private (secret) key of the user.

        Return:
            Returns the encoded signature required for the POST request. 
        """

        post_data = urllib.parse.urlencode(payload)
        encoded = (str(payload['nonce']) + post_data).encode()
        message = url_path.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(base64.b64decode(api_secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())

        return sigdigest.decode()



#==================================================================================================#
#
# The below functions will be for public endpoint requests.
#
#==================================================================================================#

    def test_public_method(self):
        """
        Description:
            (Internal) THIS IS AN INTERNAL TEST METHOD, DO NOT CALL OR TOUCH OR VERY BAD
            THINGS WILL HAPPEN... 
            
            or not, who knows :)
        """

        #resp = requests.get('https://api.kraken.com/0/public/AssetPairs?pair=BTC/USD,ETH/USD')
        #print(resp.json())
        
        # uncomment this line if the method is empty! 
        pass


    def get_server_time(self, use_unix_time: bool = True):
        """
        Description
            (Public) Retrives the time from the server.

        Parameters:
            use_unix_time : (optional) set to True to return unix time, otherwise will return
            a datetime (defaults to True).

        Return:
            See Kraken API for more info.
        """

        success, result = self.get_request(self._endpoints.TIME)

        if success:
            return result['unixtime'] if use_unix_time else result['rfc1123']
        else:
            return result


    def get_system_status(self):
        """
        Description:
            (Public) Gets the current system status or trading mode.

        Parameters:
            None required.

        Return:
            See Kraken API for more info.
        """

        success, result = self.get_request(self._endpoints.STATUS)
        return result['status'] if success else result


    def get_asset_info(self, assets: list, aclass: str = 'currency'):
        """
        Description:
            (Public) Gets information about the assets that are available for deposit,
            withdrawl, trading and staking.

        Parameters:
            assets : (required) a string list of pairs to get the info of (ex. ['ETH', 'BTC', 'USD'])
            aclass : (optional) the asset class (defaults to 'currency')

        Return:
            See Kraken API for more info.
        """

        payload = {
            'asset' : util.list_to_string(assets),
            'aclass' : aclass
        }

        _, result = self.get_request(self._endpoints.ASSETS, payload)
        return result
    

    def get_asset_pairs(self, asset_pairs: list, info: str = 'info'):
        """
        Description:
            (Public) Gets all tradeable asset pairs.

        Parameters:
            pair : (required) a string list of pairs to get data for (ex. ['ETH/USD', 'BTC/USD']).
            info : (required) the info to retrieve for the pairs (defaults to 'info').

            For the 'info' parameter, the following options can be used:
            'info', 'leverage', 'fees', 'margin'
            
            See the Kraken API link in the class description for more info

        Return:
            See Kraken API for more info.
        """

        payload = {
            'pair' : util.list_to_string(asset_pairs),
            'info' : info
        }

        _, result = self.get_request(self._endpoints.ASSET_PAIRS, payload)
        return result


    def get_ticker_info(self, pair: str):
        """
        Description:
            Gets the ticker information for the specified pair.

        Parameters:
            pair : (required) the name of the pair (ex. 'BTC/USD').

        Return:
            See Kraken API for more info.
        """

        payload = {
            'pair' : pair
        }

        success, result = self.get_request(self._endpoints.TICKER, payload)
        return result[self.get_pair_from_result(result)] if success else result


    def get_ohlcv_data(self, pair: str, timeframe: str):
        """
        Description:
            (Public)  Gets the Open, High, Low, Close, Volume of the specified pair for given
            timeframe. Due to how the API is written, this method will only return the last 720
            candles of the specified timeframe (ex. for 1 hour candles, the last month's worth
            of data will be retrieved (720 1-hour candles / 24 hours in a day = 30 days)).

        Parameters:
            pair : (required) the pair to get the OHLCV data for (ex. 'BTC/USD').
            timeframe : (required) the time frame interval in string format.

            Use the following supported timeframes:
            '1m', '5m', '15m', '30m', '1h', '4h', '1D', '7D' or '1W', '15D'

        Return:
            See Kraken API for more info.
        """

        payload = {
            'pair' : pair,
            'interval' : util.convert_time_from_str(timeframe)
        }

        success, result = self.get_request(self._endpoints.OHLC, payload)
        return result[self.get_pair_from_result(result)] if success else result


    def get_order_book(self, pair: str, count: int = 100):
        """
        Description:
            (Public) Gets the order book data for the specified asset.

        Parameters:
            pair : (required) the pair to get the data for.
            count : (required) the maximum number of asks/bids, this value can be from 1 to 500,
            default is 100. The count will be automatically adjusted if outside the range.

        Return:
            See Kraken API for more info.
        """

        if count < 1: count = 1
        elif count > 500: count = 500

        payload = {
            'pair' : pair,
            'count' : count
        }

        success, result = self.get_request(self._endpoints.DEPTH, payload)
        return result[self.get_pair_from_result(result)] if success else result
        

    def get_recent_trades(self, pair: str, since: str):
        """
        Description:
            (Public) Gets the most recent trades for the specified pair and 'since' timestamp. 
            Note that this will only return the last 1000 trades starting from 'since'. 

        Paramters:
            pair : (required) the pair to get the data for.
            since: (required) the strating timestamp in unix to retrieve the data for.

        Return:
            See Kraken API for more info.
        """

        payload = {
            'pair' : pair,
            'since' : since
        }

        success, result = self.get_request(self._endpoints.TRADES, payload)
        return result[self.get_pair_from_result(result)] if success else result

    def get_recent_spreads(self, pair: str, since: str):
        """
        Description:
            (Public) Gets the recent spread of the specified pair starting from the time specified
            by 'since'.

        Paramters:
            pair : (required) the pair to get the data for.
            since : (required) the strating timestamp in unix to retrieve the data for.

        Return:
            See Kraken API for more info.
        """

        payload = {
            'pair' : pair,
            'since' : since
        }

        success, result = self.get_request(self._endpoints.SPREAD, payload)
        return result[self.get_pair_from_result(result)] if success else result



#==================================================================================================#
#
# The below functions will be for private user data endpoint requests.
#
#==================================================================================================#

    def test_private_method(self):
        """
        Description:
            (Internal) THIS IS AN INTERNAL TEST METHOD, DO NOT CALL OR TOUCH OR VERY BAD
            THINGS WILL HAPPEN... 
            
            or not, who knows :)
        """

        #resp = requests.get('https://api.kraken.com/0/public/AssetPairs?pair=BTC/USD,ETH/USD')
        #print(resp.json())
        
        # uncomment this line if the method is empty! 
        pass


    def get_account_balance(self, api_key: str, api_secret: str):
        """
        Description:
            (Private) Retrieves all cash balances minus all pending withdrawls.

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.

        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce()
        }

        _, result = self.post_request(self._endpoints.BALANCE, payload, api_key, api_secret)
        return result
    

    def get_trade_balance(self, api_key: str, api_secret: str, asset: str):
        """
        Description:
            (Private) Retrieves a summary of collateral balances, margin positions
            valuations, equity and margin level.

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            asset : (required) the asset to determine the balance for (ex. 'USD').

        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce(),
            'asset' : asset
        }

        _, result = self.post_request(self._endpoints.TRADE_BALANCE, payload, api_key, api_secret)
        return result

    
    def get_open_orders(self, api_key: str, api_secret: str, include_trades: bool = False, userref: int = None):
        """
        Description:
            (Private) Retreives info about currently open orders.

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            include_trades : (optional) whether or not to include trades related to position in output.
            userref : (optional) restrict result to given user reference ID.

        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce(),
            'trades' : include_trades
        }

        if userref is not None: payload['userref'] = userref

        success, result = self.post_request(self._endpoints.OPEN_ORDERS, payload, api_key, api_secret)
        return result['open'] if success else result


    def get_closed_orders(self, api_key: str, api_secret: str, include_trades: bool = False, userref: int = None,
                            start: int = None, end: int = None, offset: int = None, closetime: str = 'both'):

        """
        Description:
            (Private) Retrieve information about orders that have been closed (filled or cancelled). The 
            50 most recent results are returned at a time. This is the max amount of trades it can return.

            Note: if an order's transaction ID is given for 'start' or 'end', then the order's opening time
            is used.

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            include_trades : (optional) whether or not to include trades related to position in output.
            userref : (optional) restrict result to given user reference ID.
            start : (optional) starting unix timestamp or order transaction ID of results (exclusive).
            end : (optional) ending unix timestamp or order transaction ID of results (inclusive).
            offset : (optional) result offset for pagination.
            closetime : (optional) which time to use to search ('both', 'open', 'close').

        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce(),
            'trades' : include_trades,
            'closetime' : closetime
        }

        if userref is not None: payload['userref'] = userref
        if start is not None: payload['start'] = start
        if end is not None: payload['end'] = end
        if offset is not None: payload['ofs'] = offset

        success, result = self.post_request(self._endpoints.CLOSED_ORDERS, payload, api_key, api_secret)
        return result['closed'] if success else result

    
    def query_order_info(self, api_key: str, api_secret: str, transactionID, 
                        include_trades: bool = False, userref: int = None):

        """
        Description:
            (Private) Retrieve information about specific orders.

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            transactionID : (required) comma delimited list of transaction IDs to query info about (20 max).
            include_trades : (optional) whether or not to include trades related to position in output.
            userref : (optional) restrict result to given user reference ID.

        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce(),
            'trades' : include_trades
        }

        if userref is not None: payload['userref'] = userref
        if transactionID is not None: payload['txid'] = util.list_to_string(transactionID)

        _, result = self.post_request(self._endpoints.QUERY_ORDERS, payload, api_key, api_secret)
        return result

    
    def get_trades_history(self, api_key: str, api_secret: str, type: str = 'all', include_trades: bool = False,
                           start: int = None, end: int = None, offset: int = None):
        
        """
        Description:
            (Private) Retrieves information about trades/fills. The 50 most recent results are returned at 
            a time.

            Note: Unless otherwise stated, costs, fees, prices and volumes are specified with the precision
            for the asset pair ('pair_decimal' and 'lot_decimal'), not the individual assets' precision
            ('decimals').

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            type : (optional) the type of trade:
            ('all', 'any position', 'closed position', 'closing position', 'no position').
            include_trades : (optional) whether or not to include trades related to position in output.
            start : (optional) starting unix timestamp or trade transcation ID of results (exclusive).
            end : (optional) ending unix timestamp or trade transaction ID of results (inclusive).
            offset : (optional) result offest for pagination.

        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce(),
            'type' : type,
            'trades' : include_trades
        }

        if start is not None: payload['start'] = start
        if end is not None: payload['end'] = end
        if offset is not None: payload['ofs'] = offset

        _, result = self.post_request(self._endpoints.TRADES_HISTORY, payload, api_key, api_secret)
        return result

    
    def query_trades_info(self, api_key: str, api_secret: str, transactionID, include_trades = False):

        """
        Description:
            (Private) Retrieves information about specific trades/fills.

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            transactionID : (required) comma delimited list of transaction IDs to query info about (20 max).
            include_trades : (optional) whether or not to include trades related to position in output.

        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce(),
            'txid' : util.list_to_string(transactionID),
            'trades' : include_trades
        }

        _, result = self.post_request(self._endpoints.QUERY_TRADES, payload, api_key, api_secret)
        return result

    
    def get_open_positions(self, api_key: str, api_secret: str, transactionID, docalcs: bool = False,
                           consolidation: str = 'market'):

        """
        Description:
            (Private) Get information about open margins positions.

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            transactionID : (required) comma delimited list of transaction IDs to query info about (20 max).
            docalcs : (optional) whether to include P&L calculations.
            consolidation : (optional) consolidates positions by 'market' or 'pair'.
            
        Return:
            See Kraken API for more info.
        """
        
        payload = {
            'nonce' : util.generate_nonce(),
            'txid' : util.list_to_string(transactionID),
            'docalcs' : docalcs,
            'consolidation' : consolidation
        }

        _, result = self.post_request(self._endpoints.OPEN_POSITIONS, payload, api_key, api_secret)
        return result

    
    def get_ledgers_info(self, api_key: str, api_secret: str, asset: str = 'all', aclass: str = 'currency', 
                         type: str = 'all', start: int = None, end: int = None, offset: int = None):

        """
        Description:
            (Private) Retrieves information about ledger entries. By default, the 50 most recent results
            are returned.

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            asset : (optional) comma delimited list of assets to restrict output to (defaults to 'all').
            aclass : (optional) the asset class (defaults to currency).
            type : (optional) type of ledger to retrieve ('all', 'deposit', 'withdrawl', 'trade', 'margin')
            start : (optional) starting unix timestamp or ledger ID of results (exclusive).
            end : (optional) ending unix timestamp or ledger ID of results (inclusive).
            offset : (optional) result offset for pagination.
            
        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce(),
            'asset' : asset,
            'aclass': aclass,
            'type'  : type
        }

        if start is not None: payload['start'] = start
        if end is not None: payload['end'] = end
        if offset is not None: payload['ofs'] = offset
        
        _, result = self.post_request(self._endpoints.LEDGERS, payload, api_key, api_secret)
        return result
        
    
    def query_ledgers(self, api_key: str, api_secret: str, id, include_trades: bool = False):

        """
        Description:
            (Private) Retrieves information about ledger entries. By default, the 50 most recent
            results are returned.

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            id : (required) comma delimited list of ledger IDs to query info about (20 max).
            include_trades : (optional) whether or not to include trades related to position in output.
            
        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce(),
            'id'    : util.list_to_string(id),
            'trades' : include_trades
        }

        _, result = self.post_request(self._endpoints.QUERY_LEDGERS, payload, api_key, api_secret)
        return result
        

    def get_trade_volume(self, api_key: str, api_secret: str, pair: str, fee_info: bool = False):

        """
        Description:
            (Private) If an asset pair is on a maker/taker fee schedule, the taker side is given
            in 'fees' and maker side in 'fee_maker'. For pairs not on maker/taker, they will only
            be given in 'fees'.

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            pair : (optional) asset pair to get data for.
            fee_info : (optional) whether or not to include fee info in results
            
        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce(),
            'pair'  : pair,
            'fee-info'  : fee_info
        }

        _, result = self.post_request(self._endpoints.TRADE_VOLUME, payload, api_key, api_secret)
        return result


    def request_export_report(self, api_key: str, api_secret: str, report: str, descr: str, format: str = 'CSV',
                              fields: str = 'all', starttm: int = None, endtm: int = None):

        """
        Description:
            (Private) Request export of trades or ledgers.

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            report : (required) type of data to export ('trades', 'ledgers').
            descr : (required) description for the export.
            format : (optional) file format to export ('CSV', 'TSV').
            fields : (optional) comma-delimited list of fields to include.
                * trades: ordertxid, time, ordertype, price, cost, fee, vol, margin, misc, ledgers
                * ledgers: refid, time, type, aclass, asset, amount, fee, balance
            starttm : (optional) unix timestamp for report start time (default 1st of the current month).
            endtm : (optional) unix timestamp for report end time (default now).
            
        Return:
            See Kraken API for more info.
        """
        
        payload = {
            'nonce' : util.generate_nonce(),
            'report': report,
            'format': format,
            'description': descr,
            'fields': fields
        }
        
        if starttm is not None: payload['starttm'] = starttm
        if endtm is not None: payload['endtm'] = endtm
            
        success, result = self.post_request(self._endpoints.ADD_EXPORT, payload, api_key, api_secret)
        return result['id'] if success else result

    
    def get_export_report_status(self, api_key: str, api_secret: str, report: str):

        """
        Description:
            (Private) Get status of requested data exports.

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            report :  (required) type of reports to inquire about ('trades', 'ledgers').
            
        Return:
            See Kraken API for more info.
        """
        
        payload = {
            'nonce' : util.generate_nonce(),
            'report': report
        }
        
        _, result = self.post_request(self._endpoints.EXPORT_STATUS, payload, api_key, api_secret)
        return result


    def retrieve_data_export(self, api_key: str, api_secret: str, id: str, file_name: str):
        
        """
        Description:
            (Private) Get status of requested data exports.

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            id : (required) report ID to retrieve.
            file_name : (required) the name of the file to use when saving the report (without extension).
            
        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce(),
            'id'    : id
        }
        
        _, result = self.post_request(self._endpoints.RETRIEVE_EXPORT, payload, api_key, api_secret, True, file_name + '.zip')
        return result


    def delete_export_report(self, api_key: str, api_secret: str, id: str, type: str):
        
        """
        Description:
            (Private) Delete exported trades/ledgers report

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            id : (required) ID of report to delete or cancel
            type : (required) 'cancel', 'delete'.
                * 'delete' can only be used for reports that have already been processed. Use 
                  'cancel' for queued or processing reports.
            
        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce(),
            'id' : id,
            'type' : type
        }

        success, result = self.post_request(self._endpoints.REMOVE_EXPORT, payload, api_key, api_secret)
        return result[type] if success else result



#==================================================================================================#
#
# The below functions will be for private user trading endpoint requests.
#
#==================================================================================================#

    def add_order(self, api_key: str, api_secret: str, pair: str, type: str, order_type: str, volume: int, 
                  price: str = None, price2: str = None, trigger: str = 'last', leverage: str = None, 
                  oflags: str = None, timeinforce: str = 'GTC', starttm: str = None, 
                  expiretm: str = None, close_orderType: str = None, close_price: str = None, 
                  close_price2: str = None, deadline: str = None, userref: int = None, validate: bool = False):

        """
        Description:
            Place a new order. There are many parameters for this request, so please thorougly read this
            docstring and completely understand how this works before calling this function.

            Note 1: See the AssetPairs endpoint for details on the available trading pairs, their price and 
            quanitity precisions, order minimums, available leverage, etc.

            Note 2: Use validate = True to test if the header is correct, otherwise, an actual order will
            be placed if validate = False

        Paramters:
            \napi_key : (required) the API key for the account.
            \napi_secret : (required) the API secret for the account.
            \npair : (required) Asset pair id or altname.
            \ntype : (required) order direction, 'buy', 'sell'.
            \norder_type : (required) 'market', 'limit', 'stop-loss', 'take-profit', 'stop-loss-limit','take-profit-limit', 'settle-position'.
            \nvolume : (required) order quantity in terms of the base asset. Note that volume can be specified as 0 for closing margin orders to automatically fill the requisite quantity.
            \nprice : (optional) optional but required for the following:
                * Limit price for 'limit' orders
                * Trigger price for 'stop-loss', 'stop-loss-limit', 'take-profit' and 'take-profit-limit' orders.
            \nprice2 : (optional) limit price for 'stop-loss-limit' and 'take-profit-limit' orders.
            \ntrigger : (NOT IN USE) price signal used to trigger 'stop-loss', 'stop-loss-limit', 'take-profit' and 'take-profit-limit' orders ('index', 'last', defaults to 'last'). Note that this 'trigger' type will as well be used for associated conditional close orders.
            \nleverage : (optional) amount of leverage desired.
            \noflags : (optional) comma delimited list of order flags
                * post = post-only order (available when order_type = 'limit').
                * fcib = prefer fee in base currency (default if selling).
                * fciq = prefer fee in quote currency (default if buying, mutually exclusive with fcib)/
                * nompp = disable market price protection for market orders.
            \ntimeinforce : (optional) time-in-force of the order to specify how long it should remain in the order book before being cancelled. 'GTC' (Good-'til-cancelled) is default if the parameter is omitted. 'IOC' (immediate-or-cancel) will immediately execute the amount possible and cancel any remaining balance rather than resting in the book. 'GTD' (good-'til-date), if specified, must coincide with a desired expiretm.
            \nstarttm : (optional) scheduled start time. Can be specified as an absolute timestamp or as a number of seconds in the future.
                * 0 = now (default)
                * +<n> = schedule start time seconds from now
                * <n> = unix timestamp of start time
            \nexpiretm : (optional) expiration time
                * 0 = no expiration (default)
                * +<n> = expire seconds from now, minimum 5 seconds
                * <n> = unix timestamp of expiration time
            \nclose[order_type] : (optional) conditional close order type, 'limit', 'stop-loss', 'take-profit', 'stop-loss-limit', 'take-profit-limit'. Note that conditional close orders are triggered by execution of the primary order in the same quantity and opposite direction, but once triggered are independent orders that may reduce or increase net position.
            \nclose[price] : (optional) conditional close order price
            \nclose[price2] : (optional) conditional close order price2
            \ndeadline : (optional) RFC3339 timestamp (e.g. 2021-04-01T00:18:45Z) after which the matching engine should reject the new order request, in presence of latency or order queueing. min now() + 5 seconds, max now() + 60 seconds.
            \nuserref : (optional) userref is an optional user-specified integer id that can be associated with any number of orders. Many clients choose a userref corresponding to a unique integer id generated by their systems (e.g. a timestamp). However, because we don't enforce uniqueness on our side, it can also be used to easily group orders by pair, side, strategy, etc. This allows clients to more readily cancel or query information about orders in a particular group, with fewer API calls by using userref instead of our txid, where supported.
            \nvalidate : (testing) validate inputs only. Does not submit order. Please set this parameter to True when testing!

        \nReturn:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce(),
            'pair' : pair,
            'type' : type,
            'ordertype' : order_type,
            'volume' : volume,
            'timeinforce' : timeinforce,
            'validate' : validate
        }

        # not sure why trigger doesn't work ): but it doesn't seem to make a difference anyways...
        #if order_type != 'market': payload['trigger'] = trigger
        if price is not None: payload['price'] = price
        if price2 is not None: payload['price2'] = price2
        if leverage is not None: payload['leverage'] = leverage
        if oflags is not None: payload['oflags'] = oflags
        if starttm is not None: payload['starttm'] = starttm
        if expiretm is not None: payload['expiretm'] = expiretm
        if close_orderType is not None: payload['close[ordertype]'] = close_orderType
        if close_price is not None: payload['close[price]'] = close_price
        if close_price2 is not None: payload['close[price2]'] = close_price2
        if deadline is not None: payload['deadline'] = deadline
        if userref is not None: payload['userref'] = userref

        _, result = self.post_request(self._endpoints.ADD_ORDER, payload, api_key, api_secret)
        return result


    def cancel_order(self, api_key: str, api_secret: str, transactionID):

        """
        Description:
            Cancel a particular open order (or set of open orders by transactionID or userref).

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            transactionID: (required) open order transaction id or user reference. 

        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce(),
            'txid' : transactionID
        }

        _, result = self.post_request(self._endpoints.CANCEL_ORDER, payload, api_key, api_secret)
        return result

    def cancel_all_orders(self, api_key: str, api_secret: str):

        """
        Description:
            Cancel all open orders.

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.

        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce()
        }

        _, result = self.post_request(self._endpoints.CANCEL_ALL_ORDERS, payload, api_key, api_secret)
        return result

    def cancel_all_orders_after_x(self, api_key: str, api_secret: str, timeout: int):

        """
        Description:
            CancelAllOrdersAfter provides a "Dead Man's Switch" mechanism to protect the client from network malfunction, extreme latency or unexpected matching engine downtime. The client can send a request with a timeout (in seconds), that will start a countdown timer which will cancel all client orders when the timer expires. The client has to keep sending new requests to push back the trigger time, or deactivate the mechanism by specifying a timeout of 0. If the timer expires, all orders are cancelled and then the timer remains disabled until the client provides a new (non-zero) timeout.

            The recommended use is to make a call every 15 to 30 seconds, providing a timeout of 60 seconds. This allows the client to keep the orders in place in case of a brief disconnection or transient delay, while keeping them safe in case of a network breakdown. It is also recommended to disable the timer ahead of regularly scheduled trading engine maintenance (if the timer is enabled, all orders will be cancelled when the trading engine comes back from downtime - planned or otherwise).

        Parameters:
            api_key : (required) the API key for the account.
            api_secret : (required) the API secret for the account.
            timeout : (required) duration (in seconds) to set/extend the timer by.

        Return:
            See Kraken API for more info.
        """

        payload = {
            'nonce' : util.generate_nonce(),
            'timeout' : timeout
        }

        _, result = self.post_request(self._endpoints.CANCEL_ALL_ORDERS_AFTER, payload, api_key, api_secret)
        return result
