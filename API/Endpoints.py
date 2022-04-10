
class KrakenEndpoints():

    # (general)
    API_DOMAIN = 'https://api.kraken.com'

    # (public) server/market data
    PUBLIC = '/0/public/'
    TIME = 'Time'
    STATUS = 'SystemStatus'
    ASSETS = 'Assets'
    ASSET_PAIRS = 'AssetPairs'
    TICKER = 'Ticker'
    OHLC = 'OHLC'
    DEPTH = 'Depth'
    TRADES = 'Trades'
    SPREAD = 'Spread'

    # (private) user data
    PRIVATE = '/0/private/'
    BALANCE = 'Balance'
    TRADE_BALANCE = 'TradeBalance'
    OPEN_ORDERS = 'OpenOrders'
    CLOSED_ORDERS = 'ClosedOrders'
    QUERY_ORDERS = 'QueryOrders'
    TRADES_HISTORY = 'TradesHistory'
    QUERY_TRADES = 'QueryTrades'
    OPEN_POSITIONS = 'OpenPositions'
    LEDGERS = 'Ledgers'
    QUERY_LEDGERS = 'QueryLedgers'
    TRADE_VOLUME = 'TradeVolume'
    ADD_EXPORT = 'AddExport'
    EXPORT_STATUS = 'ExportStatus'
    RETRIEVE_EXPORT = 'RetrieveExport'
    REMOVE_EXPORT = 'RemoveExport'

    # (private) user trading
    ADD_ORDER = 'AddOrder'
    CANCEL_ORDER = 'CancelOrder'
    CANCEL_ALL_ORDERS = 'CancelAll'
    CANCEL_ALL_ORDERS_AFTER = 'CancelAllOrdersAfter'


    def get_public_endpoint(self, endpoint: str):
        """
        Description:
            Formats the URL based on the endpoint provided to this function. This class
            will contain the avilable endpoints as attributes. Note that this class will
            only return the PUBLIC endpoints. For private endpoints, see:
            get_private_endpoint()

        Parameters:
            endpoint : all endpoints are specified by class attributes.

        Return:
            Returns the fully formatted endpoint URL.
        """

        return f"{self.API_DOMAIN}{self.PUBLIC}{endpoint}"


    def get_private_endpoint(self, endpoint: str):
        """
        Description:
            Formats the URL based on the endpoint provided to this function. This class
            will contain the avilable endpoints as attributes. Note that this class will
            only return the PRIVATE/AUTHENTICATED endpoints. For public endpoints, see:
            get_public_endpoint()

        Parameters:
            endpoint : all endpoints are specified by class attributes.

        Return:
            Returns the fully formatted endpoint URL.
        """

        return f"{self.API_DOMAIN}{self.PRIVATE}{endpoint}"
