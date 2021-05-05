from datetime import datetime
from time import mktime
import uuid
import hmac
import requests
import json
from hashlib import sha256
import optparse
import sys
import re

# OPTIONS
ACTIVITY_TYPES = [ "DEPOSIT", "WITHDRAWAL", "HASHPOWER", "MINING", "EXCHANGE", "UNPAID_MINING", "OTHER" ]
ALGORITHMS = [ "SCRYPT", "SHA256", "SCRYPTNF", "X11", "X13", "KECCAK", "X15", "NIST5", "NEOSCRYPT", "LYRA2RE", "WHIRLPOOLX", "QUBIT", "QUARK", "AXIOM", "LYRA2REV2", "SCRYPTJANENF16", "BLAKE256R8", "BLAKE256R14", "BLAKE256R8VNL", "HODL", "DAGGERHASHIMOTO", "DECRED", "CRYPTONIGHT", "LBRY", "EQUIHASH", "PASCAL", "X11GOST", "SIA", "BLAKE2S", "SKUNK", "CRYPTONIGHTV7", "CRYPTONIGHTHEAVY", "LYRA2Z", "X16R", "CRYPTONIGHTV8", "SHA256ASICBOOST", "ZHASH", "BEAM", "GRINCUCKAROO29", "GRINCUCKATOO31", "LYRA2REV3", "CRYPTONIGHTR", "CUCKOOCYCLE", "GRINCUCKAROOD29", "BEAMV2", "X16RV2", "RANDOMXMONERO", "EAGLESONG", "CUCKAROOM", "GRINCUCKATOO32", "HANDSHAKE", "KAWPOW", "CUCKAROO29BFC", "BEAMV3", "CUCKAROOZ29", "OCTOPUS" ]
ALGORITHM_CODES = []
i = 0
for a in ALGORITHMS:
    ALGORITHM_CODES.append(i)
    i+=1
MARKETS = [ "EU", "USA", "EU_N", "USA_E" ]
MARKETS_LONG = [ "EUROPE", "USA", "EUROPE_NORTH", "USA_EAST" ]
OPS = [ "GT", "GE", "LT", "LE" ]
# ORDER_RELATIONS = [ "GT", "GE", "LT", "LE" ]
EXCHANGE_ORDER_TYPES = [ "MARKET", "LIMIT" ]
HASHPOWER_ORDER_TYPES = [ "STANDARD", "FIXED" ]
RIG_ACTIONS = [ "START", "STOP", "POWER_MODE" ]
SORT_PARAMETERS = [ "RIG_NAME", "TIME", "MARKET", "ALGORITHM", "UNPAID_AMOUNT", "DIFFICULTY", "SPEED_ACCEPTED", "SPEED_REJECTED", "PROFITABILITY" ]
SORT_DIRECTIONS = [ "ASC", "DESC" ]
SORT_OPTIONS = [ "NAME", "PROFITABILITY", "ACTIVE", "INACTIVE" ]
SIDES = [ "BUY", "SELL" ]
STATUSES = [ "PENDING", "ACTIVE", "PENDING_CANCELLATION", "CANCELLED", "DEAD", "EXPIRED", "ERROR", "ERROR_ON_CREATION", "ERROR_ON_CREATION_ON_REVERTING_TRANSACTIONS", "COMPLETED", "ERROR_MISSING" ]
TX_TYPES = [ "DEPOSIT", "WITHDRAWAL", "MOVE" ]
WALLET_TYPES = [ "BITGO", "BLOCKCHAIN", "LIGHTNING", "MULTISIG" ]

# Websockets OPTIONS
RESOLUTIONS = [ 1, 60, 1440 ]

# cache
CACHE = dict({})
TIMEOUT = 1000 * 60 * 3 # 3 minutes

class public_api:

    def __init__(self, host, verbose=False):
        self.host = host
        self.verbose = verbose
        self.session = requests.Session()

    def close(self):
        self.session.close()

    def request(self, method, path, query, body):
        url = self.host + path
        if query:
            # TODO
            # why doesn't this work here instead of forcing the check for empty [] at every function???
            # query = query.replace("[]", "") # clean arrays into empty strings
            url += '?' + query

        if self.verbose:
            print()
            print(method, url)
            if query != "":
                print('query: '+str(query))
            if body:
                print('body: '+str(body))

        headers = {
            'Content-Type': 'application/json'
        }

        self.session.headers = headers

        if body:
            body_json = json.dumps(body)
            response = self.session.request(method, url, data=body_json)
        else:
            response = self.session.request(method, url)

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(str(response.status_code) + ": " + response.reason + " " + str(response.content))
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)

    def get_epoch_ms_from_now(self):
        now = datetime.now()
        now_ec_since_epoch = mktime(now.timetuple()) + now.microsecond / 1000000.0
        return int(now_ec_since_epoch * 1000)

    # @staticmethod
    # def algo_to_number(algorithm):
    #     if str(algorithm) in ALGORITHMS:
    #         return ALGORITHMS.index(str(algorithm))
    #     return None

    # @staticmethod
    # def algo_to_name(algo_number):
    #     if int(algo_number) < len(ALGORITHMS):
    #         return ALGORITHMS[int(algo_number)]
    #     return None

    @staticmethod
    def algo_settings_from_response(algo_response, algorithm):
        # if not algorithm and algo_number:
        #     algorithm = public_api.algo_to_name(algo_number)
        # if not algo_number and algorithm:
        #     algo_number = public_api.algo_to_number(algorithm)
        # if not algorithm and not algo_number:
        #     raise Exception('Missing algorithm or algo_number for algo_response parameter')
        algo_setting = None
        for item in algo_response['miningAlgorithms']:
            if item['algorithm'] == algorithm:
                algo_setting = item
        if algo_setting is None:
            raise Exception('Settings for algorithm not found in algo_response parameter')
        return algo_setting

    #############################################################################################

    # External miner REST API methods

    # Getting active workers and information about active workers on external miner, such as current mining algorithm, speed, profitability, etc.
    # btcAddress *    string  Btc address
    # size    integer     Number of elements per page         100
    # page    integer     Page number         0
    # sortParameter   string  Sort parameter         RIG_NAME     [ "RIG_NAME", "TIME", "MARKET", "ALGORITHM", "UNPAID_AMOUNT", "DIFFICULTY", "SPEED_ACCEPTED", "SPEED_REJECTED", "PROFITABILITY" ] 
    # sortDirection   string  Sort direction          ASC    [ "ASC", "DESC" ] 
    def get_active_workers(self, btcAddress, size=100, page=0, sortParameter="RIG_NAME", sortDirection="ASC"):
        query = "size={size}&page={page}&sortParameter={sortParameter}&sortDirection={sortDirection}".format(btcAddress=btcAddress, size=size, page=page, sortParameter=sortParameter, sortDirection=sortDirection)
        return self.request('GET', '/main/api/v2/mining/external/{btcAddress}/rigs/activeWorkers'.format(btcAddress=btcAddress), query, None)

    # Get statistical streams for all mining rigs with external BTC address for selected algorithm. Result consists of following streams:
    # btcAddress *    string  The external BTC address of the RIG(s)
    # algorithm *     integer     Algorithm code
    # afterTimestamp  integer     After timestamp (inclusive, default: now - 1 days)
    # beforeTimestamp     integer     Before timestamp (exclusive, default: now)
    def get_algo_statistics(self, btcAddress, algorithm, afterTimestamp=None, beforeTimestamp=None):
        query = "algorithm={algorithm}&afterTimestamp={afterTimestamp}&beforeTimestamp={beforeTimestamp}".format(algorithm=algorithm, afterTimestamp=afterTimestamp, beforeTimestamp=beforeTimestamp)
        return self.request('GET', '/main/api/v2/mining/external/{btcAddress}/rigs/stats/algo'.format(btcAddress=btcAddress), query, None)

    # Get statistical streams for all mining rigs with external BTC address. Result consists of following streams:
    # btcAddress *    string  The external BTC address of the RIG(s)
    # afterTimestamp  integer     After timestamp (inclusive, default: now - 1 days)
    # beforeTimestamp     integer     Before timestamp (exclusive, default: now)
    def get_unpaid_statistics(self, btcAddress, afterTimestamp=None, beforeTimestamp=None):
        query = "afterTimestamp={afterTimestamp}&beforeTimestamp={beforeTimestamp}".format(afterTimestamp=afterTimestamp, beforeTimestamp=beforeTimestamp)
        return self.request('GET', '/main/api/v2/mining/external/{btcAddress}/rigs/stats/unpaid'.format(btcAddress=btcAddress), query, None)

    # External miner withdrawal list. When external miner reaches minimal value for withdrawal, withdraw is automatically executed on the platform. List consists of the transactions and corresponding information.
    # btcAddress *    string  External BTC address
    # afterTimestamp  integer     After timestamp in milliseconds from 1.1.1970 (default: from now)
    # size    integer     Size       100
    # page    integer     Page       0
    def get_withdrawals(self, btcAddress, afterTimestamp=None, size=100, page=0):
        query = "afterTimestamp={afterTimestamp}&size={size}&page={page}".format(afterTimestamp=afterTimestamp, size=size, page=page)
        return self.request('GET', '/main/api/v2/mining/external/{btcAddress}/rigs/withdrawals'.format(btcAddress=btcAddress), query, None)

    # List rig statuses for external miner.
    # btcAddress *    string  Btc address
    # size    integer     Size      100
    # page    integer     Page      0
    # sort    string  Sort     NAME    [ "NAME", "PROFITABILITY", "ACTIVE", "INACTIVE" ]
    def get_rig_statuses(self, btcAddress, size=100, page=0, sort="NAME"):
        query = "size={size}&page={page}&sort={sort}".format(size=size, page=page, sort=sort)
        return self.request('GET', '/main/api/v2/mining/external/{btcAddress}/rigs/rigs2'.format(btcAddress=btcAddress), query, None)

    #############################################################################################

    # Hashpower public REST API methods

    # Hashpower order book for specified algorithm. Response contains orders for all markest and their stats. When there a lot of orders, response will be paged.
    # algorithm *     string  Mining algorithm
    # size    integer     Page size (optional, default: 100)
    # page    integer     Page number (optional, default: 0)
    def get_hashpower_orderbook(self, algorithm, size=100, page=0):
        query = 'algorithm={algorithm}&size={size}&page={page}'.format(algorithm=algorithm, size=size, page=page)
        return self.request('GET', '/main/api/v2/hashpower/orderBook', query, None)

    # Determines current fixed order price from limit, algorithm and market. Limit should be in market unit. Please check /main/api/v2/public/buy/info to get limits and constants for the specified algorithm.
    # algorithm   string  Algorithm
    # market  string  Market    [ "EU", "USA", "EU_N", "USA_E" ]
    # limit   number  Limit in market unit
    def fixed_price_request(self, algorithm, market, limit):
        request_data = {
            'algorithm': str(algorithm).upper(),
            'market': str(market).upper(),
            'limit': float(limit)
        }
        return self.request('POST', '/main/api/v2/hashpower/orders/fixedPrice', '', request_data)
        # {
        #     fixedMax : number - Maximal allowed speed limit for fixed order [TH/Sol/G]/s
        #     fixedPrice : number - Current price for fixed order in BTC/factor[TH/Sol/G]/day
        # }

    # Get accepted and rejected speeds for rigs and pools, rig count and paying price for selected market and/or algorithm. When no market or algorithm is specified all markets and algorithms are returned.
    # market  string  Market
    # algorithm   string  Mining algorithm
    def get_hashpower_summaries(self, algorithm="", market=""):
        query = 'algorithm={algorithm}&market={market}'.format(algorithm=algorithm, market=market)
        return self.request('GET', '/main/api/v2/hashpower/orders/summaries', query, None)

    # Get accepted and rejected speed from pools and rigs, rig count and paying price for selected market and algorithm.
    # market *    string  Market
    # algorithm *     string  Mining algorithm
    def get_hashpower_orders_summary(self, algorithm, market):
        query = 'algorithm={algorithm}&market={market}'.format(algorithm=algorithm, market=market)
        return self.request('GET', '/main/api/v2/hashpower/orders/summary', query, None)

    # Whole history for the selected algorithm.
    # algorithm *     string  Algorithm code
    def get_algo_history(self, algorithm):
        query = 'algorithm={algorithm}'.format(algorithm=algorithm)
        return self.request('GET', '/main/api/v2/public/algo/history', query, None)

    # Information for each enabled algorithm needed for buying hashpower. Result contains minimum and maximum 
    # values for price, limit, information about minimum pool difficulty and more that can be useful in 
    # automated application like NicehashBot 
    def buy_info(self):
        if "buy_info" in CACHE and int(CACHE["buy_info"]["timeout"]) < datetime.now():
            pass
        else:
            CACHE["buy_info"] = dict({})
            CACHE["buy_info"]["timeout"] = int(datetime.timestamp(datetime.now())) + int(TIMEOUT)
            CACHE["buy_info"]["value"] = self.request('GET', '/main/api/v2/public/buy/info', '', None)
        return CACHE["buy_info"]["value"]

    # Get all hashpower orders. Request parameter work as filter to fine tune the result. The result is paged, when needed.
    # algorithm   string  Algorithm
    # market  string  Market
    # op  string  Relation operation
    # timestamp   integer     The timestamp to compare
    # page    integer     Page
    # size    integer     Size
    def get_orders(self, algorithm="", market="", op="LT", timestamp=None, page=0, size=100):
        if not timestamp: timestamp = self.get_epoch_ms_from_now()
        query = "algorithm={algorithm}&market={market}&op={op}&timestamp={timestamp}&page={page}&size={size}".format(algorithm=algorithm, market=market, op=op, timestamp=timestamp, page=page, size=size)
        return self.request('GET', '/main/api/v2/public/orders', query, None)

    # Get information about speed and price for each enabled algorithm.
    def get_multialgo_info(self):
        return self.request('GET', '/main/api/v2/public/simplemultialgo/info', '', None)

    # Get average price and hashpower speed for all enabled algorithms in average for past 24 hours.
    def get_global_stats_24(self):
        return self.request('GET', '/main/api/v2/public/stats/global/24h', '', None)

    # Get current price and hashpower speed for all enabled algorithms in average for last 5 minutes.
    def get_current_global_stats(self):
        return self.request('GET', '/main/api/v2/public/stats/global/current', '', None)

    #############################################################################################

    # Public REST API methods

    # List the mining algorithms and detailed algorithm information.
    def get_algorithms(self):
        return self.request('GET', '/main/api/v2/mining/algorithms', '', None)

    # Get currency list and details for each currency.
    def get_currencies(self):
        return self.request('GET', '/main/api/v2/public/currencies', '', None)

    # Fee rules for whole platforms. Response contains all possible fee rules on the platform.
    def get_fee_rules(self):
        return self.request('GET', '/main/api/v2/public/service/fee/info', '', None)

    # Get countries info
    def get_countries(self):
        return self.request('GET', '/api/v2/enum/countries', '', None)

    # Get all allowed KM countries
    def get_km_countries(self):
        return self.request('GET', '/api/v2/enum/kmCountries', '', None)

    # Get all possible organization permissions.
    def get_permissions(self):
        return self.request('GET', '/api/v2/enum/permissions', '', None)

    # Get all allowed exchange countries
    def get_xch_countries(self):
        return self.request('GET', '/api/v2/enum/xchCountries', '', None)

    # A list of all API flags and their values. Flag type designates API feature of the platform. Possible values are:
    # IS_MAINTENANCE - is true when maintenance is in progress
    # SYSTEM_UNAVAILABLE - is true when whole REST API is not available
    # DISABLE_REGISTRATION - is true when new registrations are not allowed
    # IS_KM_MAINTENANCE - is true when EUR/BTC exchange is not available
    def get_api_flags(self):
        return self.request('GET', '/api/v2/system/flags', '', None)

    def print_api_flags(self):
        for flag in self.request('GET', '/api/v2/system/flags', '', None)["list"]:
            print("{}: {}".format(flag["flagName"], flag["flagValue"]))

    # Get server time. Can be used for authentication purposes, please check General section with authentication description.
    def get_server_time(self):
        return self.request('GET', '/api/v2/time', '', None)

    #############################################################################################

    # Exchange public REST API methods

    # Get candlesticks for specified resolution. The resolution field must be one of the following values: {1, 60, 1440}. These values correspond to timeslices representing one minute, one hour and one day.
    # market *    string  Market symbol
    # from *  integer     Start time in s
    # to *    integer     End time in s
    # resolution *    string  Time interval (1 - minute, 60 - hour or 1440 - day)
    def get_candlesticks(self, market, from_s, to_s, resolution):
        query = "market={market}&from={from_s}&to={to_s}&resolution={resolution}".format(market=market, from_s=from_s, to_s=to_s, resolution=resolution)
        return self.request('GET', '/exchange/api/v2/candlesticks', query, None)

    # Get statistics for all markets (24 hour lowest price, 24 hour highest price, 24 hour volume in BTC, 24 hour change and 7 days candlesticks).
    def get_exchange_statistics(self):
        return self.request('GET', '/exchange/api/v2/info/marketStats', '', None)

    # Get list of last prices for all markets.
    def get_current_prices(self):
        return self.request('GET', '/exchange/api/v2/info/prices', '', None)

    # Get detailed exchange status information for each market.
    def get_exchange_markets_info(self):
        return self.request('GET', '/exchange/api/v2/info/status', '', None)

    # Get trades for specific market. Limit, sort direction and timestamp can be optionally selected.
    # market *    string  Market symbol
    # sortDirection   string  Sort direction (optional, default value is DESC)
    # limit   integer     Query limit (optional, default value is 25)
    # timestamp   integer     Select older than timestamp in µs (optional, default value is current timestamp)
    def get_trades(self, market, sortDirection='DESC', limit=25, timestamp=None):
        if not timestamp: timestamp = self.get_epoch_ms_from_now()
        query = "market={market}&sortDirection={sortDirection}&limit={limit}&timestamp={timestamp}".format(market=market, sortDirection=sortDirection, limit=limit, timestamp=timestamp)
        return self.request('GET', '/exchange/api/v2/info/trades', query, None)

    # Get a list of asks and bids. Limit determines the size of asks and bids lists.
    # market *    string  Market symbol
    # limit   integer     Query limit (optional, default value is 25)
    def get_exchange_orderbook(self, market, limit=25):
        query = "market={market}&limit={limit}".format(market=market, limit=limit)
        return self.request('GET', '/exchange/api/v2/orderbook', query, None)

    #############################################################################################

    ###########
    # Removed #
    ###########

    # def get_active_orders(self):
    #     return self.request('GET', '/main/api/v2/public/orders/active/', '', None)

    # def get_active_orders2(self):
    #     return self.request('GET', '/main/api/v2/public/orders/active2/', '', None)

    # def get_markets(self):
    #     return self.request('GET', '/main/api/v2/mining/markets/', '', None)

    # def get_exchange_trades(self, market):
    #     return self.request('GET', '/exchange/api/v2/trades', 'market=' + market, None)

class private_api(public_api):

    def __init__(self, host, organisation_id, key, secret, verbose=False):
        self.key = key
        self.secret = secret
        self.organisation_id = organisation_id
        self.host = host
        self.verbose = verbose
        self.session = requests.Session()

    def close(self):
        self.session.close()

    def request(self, method, path, query, body):

        xtime = self.get_epoch_ms_from_now()
        xnonce = str(uuid.uuid4())

        message = bytearray(self.key, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(str(xtime), 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(xnonce, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(self.organisation_id, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(method, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(path, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(query, 'utf-8')

        if body:
            body_json = json.dumps(body)
            message += bytearray('\x00', 'utf-8')
            message += bytearray(body_json, 'utf-8')

        digest = hmac.new(bytearray(self.secret, 'utf-8'), message, sha256).hexdigest()
        xauth = self.key + ":" + digest

        headers = {
            'X-Time': str(xtime),
            'X-Nonce': xnonce,
            'X-Organization-Id': self.organisation_id,
            'X-Request-Id': str(uuid.uuid4()),
            'X-Auth': xauth,
            'Content-Type': 'application/json'
        }

        self.session.headers = headers

        url = self.host + path
        if query:
            # query = query.replace("[]", "") # clean arrays into empty strings
            url += '?' + query

        if self.verbose:
            print()
            print(method, url)
            if query != "":
                print('query: '+str(query))
            if body:
                print('body: '+str(body))

        if body:
            response = self.session.request(method, url, data=body_json)
        else:
            response = self.session.request(method, url)

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(str(response.status_code) + ": " + response.reason + ": " + str(response.content))
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)

    #############################################################################################

    # Accounting REST API methods

    # Get balance for selected currency. When setting extendedResponse to true pending details are added to the response.
    # currency *  string  Currency
    # extendedResponse    boolean     User will receive extended response if set to true (optional)
    def get_accounts_for_currency(self, currency, extendedResponse=False):
        query = "extendedResponse={extendedResponse}".format(extendedResponse=extendedResponse)
        return self.request('GET', '/main/api/v2/accounting/account2/{currency}'.format(currency=currency), query, None)

    # Get total balance and for each currency separated. When setting extendedResponse to true pending details are added to each item in the response.
    # extendedResponse    boolean     User will receive extended response if set to true (optional)
    # fiat    string  User will receive exchange rate from crypto currency to fiat
    def get_accounts(self, extendedResponse=False, fiat="USD"):
        query = "extendedResponse={extendedResponse}&fiat={fiat}".format(extendedResponse=extendedResponse, fiat=fiat)
        return self.request('GET', '/main/api/v2/accounting/accounts2/', query, None)

    # Get activities for specified currency matching the filtering criteria as specified by request parameters.
    # currency *  string  Currency
    # type    string  Activity type       [ "DEPOSIT", "WITHDRAWAL", "HASHPOWER", "MINING", "EXCHANGE", "UNPAID_MINING", "OTHER" ]
    # timestamp   integer     Pagination timestamp
    # stage   string  Activity completion stage       ALL
    # limit   integer     Number of results       10
    def get_account_activity(self, currency, activity_type="", timestamp=None, stage="ALL", limit=10):
        if not timestamp: timestamp = self.get_epoch_ms_from_now()
        query = "type={type}&timestamp={timestamp}&stage={stage}&limit={limit}".format(type=activity_type, timestamp=timestamp, stage=stage, limit=limit)
        return self.request('GET', '/main/api/v2/accounting/activity/{currency}'.format(currency=currency), query, None)

    # Get deposit address for selected currency for all wallet types.
    # currency *  string  Currency
    # walletType  string  Wallet        [ "BITGO", "BLOCKCHAIN", "LIGHTNING", "MULTISIG" ] 
    def get_deposit_addresses(self, currency, walletType=""):
        query = "currency={currency}&walletType={walletType}".format(currency=currency, walletType=walletType)
        return self.request('GET', '/main/api/v2/accounting/depositAddresses/', query, None)

    # List of deposit transactions details matching the filtering criteria as specified by request parameters.
    # currency *  string  Currency
    # statuses    array   Deposit order statuses          example: [COMPLETED]
    # op  string  Order relation operation, also instructs how result is ordered by timestamp for paging     LT     [ "GT", "GE", "LT", "LE" ] 
    # timestamp   integer     The order timestamp to compare
    # page    integer     Page                     0
    # size    integer     Size - max 100                   100
    def get_deposits_for_currency(self, currency, statuses=[], op="LT", timestamp=None, page=0, size=100):
        if not timestamp: timestamp = self.get_epoch_ms_from_now()
        if len(statuses) == 0: statuses = ""
        query = "statuses={statuses}&op={op}&timestamp={timestamp}&page={page}&size={size}".format(statuses=statuses, op=op, timestamp=timestamp, page=page, size=size)
        return self.request('GET', '/main/api/v2/accounting/deposits/{currency}'.format(currency=currency), query, None)

    # Get specific deposit with deposit order id and currency.
    # currency *  string  Currency
    # id *    string  Deposit order id
    def get_deposits_for_currency_by_id(self, currency, order_id):
        return self.request('GET', '/main/api/v2/accounting/deposits2/{currency}/{id}'.format(currency=currency, id=order_id), '', None)

    # Get all transaction for selected exchange order using exchange order id and market pair.
    # id *    string  Exchange order id
    # exchangeMarket *    string  Exchange market symbol
    def get_order_transactions_by_id(self, order_id, exchangeMarket):
        query = "exchangeMarket={exchangeMarket}".format(exchangeMarket=exchangeMarket)
        return self.request('GET', '/main/api/v2/accounting/exchange/{id}/trades'.format(id=order_id), query, None)

    # List of all transactions for selected hashpower order using hashpower order.
    # id *    string  Order id
    # limit   integer     Limit number of results      100
    # timestamp   integer     Pagination timestamp
    def get_hashpower_order_transactions_by_id(self, order_id, limit=100, timestamp=None):
        if not timestamp: timestamp = self.get_epoch_ms_from_now()
        query = "limit={limit}&timestamp={timestamp}".format(limit=limit, timestamp=timestamp)
        return self.request('GET', '/main/api/v2/accounting/hashpower/{id}/transactions'.format(id=order_id), query, None)

    # Get list of mining payments
    # currency *  string  Currency
    # timestamp   integer     Timestamp in milliseconds since 1.1.1970 (default value is now)
    # page    integer     Page       0
    # size    integer     Size       100
    def get_hashpower_earnings_for_currency(self, currency, timestamp=None, page=0, size=100):
        if not timestamp: timestamp = self.get_epoch_ms_from_now()
        query = "timestamp={timestamp}&page={page}&size={size}".format(timestamp=timestamp, page=page, size=size)        
        return self.request('GET', '/main/api/v2/accounting/hashpowerEarnings/{currency}'.format(currency=currency), '', None)

    # Get transaction by transaciton id and currency.
    # currency *  string  Currency
    # transactionId *     string  Transaction id
    def get_transaction_for_currency_by_id(self, currency, transactionId):
        return self.request('GET', '/main/api/v2/accounting/transaction/{currency}/{id}'.format(currency=currency, id=transactionId), '', None)

    # Get all transactions for selected currency matching the filtering criteria as specified by request parameters.
    # currency *  string  Currency
    # type    string  Transaction type                         [ "DEPOSIT", "WITHDRAWAL", "MOVE" ]
    # purposes    array   Transaction purposes
    # op  string  Order relation operation                        [ "GT", "GE", "LT", "LE" ]
    # timestamp   integer     Timestamp to compare
    # page    integer     Page                 0
    # size    integer     Size - max 100           10
    def get_transactions_for_currency(self, currency, tx_type="", purposes=[], op="", timestamp=None, page=0, size=10):
        if not timestamp: timestamp = self.get_epoch_ms_from_now()
        if len(purposes) == 0: purposes = ""
        query = "type={type}&purposes={purposes}&op={op}&timestamp={timestamp}&page={page}&size={size}".format(type=tx_type, purposes=purposes, op=op, timestamp=timestamp, page=page, size=size)        
        return self.request('GET', '/main/api/v2/accounting/transactions/{currency}'.format(currency=currency), query, None)

    # Create withdrawal request with whitelisted address using withdraw address id. 
    # Address can be whitelisted using web page or mobile application. All whitelisted address ids can be listed using /main/api/v2/accounting/withdrawalAddresses endpoint.
    # currency    string  From currency
    # amount  number  Amount in currency max precision
    # withdrawalAddressId     string  Withdrawal address ID (address must be whitelisted first)
    def withdraw_request(self, currency, amount, address_id):
        withdraw_data = {
            "currency": currency,
            "amount": amount,
            "withdrawalAddressId": address_id
        }
        return self.request('POST', '/main/api/v2/accounting/withdrawal/', '', withdraw_data)

    # Cancel withdrawal using withdrawal id and currency.
    # currency *  string  Currency
    # id *    string  Withdrawal Order ID
    def delete_withdrawal(self, currency, withdrawal_id):
        return self.request('DELETE', '/main/api/v2/accounting/withdrawal/{currency}/{id}'.format(currency=currency, id=withdrawal_id), '', None)

    # Get account withdrawal by currency and id.
    # currency *  string  Currency
    # id *    string  Withdrawal Order ID
    def get_withdrawal_for_currency_by_id(self, currency, withdrawal_id):
        return self.request('GET', '/main/api/v2/accounting/withdrawal2/{currency}/{id}'.format(currency=currency, id=withdrawal_id), '', None)

    # Get withdrawal address by widrawal address id.
    # id *    string  Withdrawal address
    def get_withdrawal_address_by_id(self, withdrawal_id):
        return self.request('GET', '/main/api/v2/accounting/withdrawalAddress/{id}'.format(id=withdrawal_id), '', None)

    # List withdrawal addresses for specified currency.
    # currency    string  Currency
    # size    integer     Page size (optional, default: 100)
    # page    integer     Page number (optional, default: 0)
    # type    string  Address type
    def get_withdrawal_addresses(self, currency, size=100, page=0, address_type=""):
        query = "currency={currency}&size={size}&page={page}&type={type}".format(currency=currency, size=size, page=page, type=address_type)
        return self.request('GET', '/main/api/v2/accounting/withdrawalAddresses/', query, None)

    # Get list of withdrawals matching the filtering criteria as specified by request parameters. 
    # currency *  string  Currency
    # statuses    array   Withdrawal order statuses
    # op  string  Order relation operation, also instructs how result is ordered by timestamp for paging                LT
    # timestamp   integer     The order timestamp to compare
    # page    integer     Page                0
    # size    integer     Size - max 100           100
    def get_withdrawals_for_currency(self, currency, statuses=[], op="LT", timestamp=None, page=0, size=100):
        if not timestamp: timestamp = self.get_epoch_ms_from_now()
        if len(statuses) == 0: statuses = ""
        query = "statuses={statuses}&op={op}&timestamp={timestamp}&page={page}&size={size}".format(currency=currency, statuses=statuses, op=op, timestamp=timestamp, page=page, size=size)
        return self.request('GET', '/main/api/v2/accounting/withdrawals/{currency}'.format(currency=currency), query, None)

    #############################################################################################

    # Hashpower private REST API methods

    # Get a list of my hashpower orders matching the filtering criteria as specified by parameters included in the request. 

    # algorithm   string  Mining algorithm (optional, if not supplied all algorithms are returned)    [ "SCRYPT", "SHA256", "SCRYPTNF", "X11", "X13", "KECCAK", "X15", "NIST5", "NEOSCRYPT", "LYRA2RE", "WHIRLPOOLX", "QUBIT", "QUARK", "AXIOM", "LYRA2REV2", "SCRYPTJANENF16", "BLAKE256R8", "BLAKE256R14", "BLAKE256R8VNL", "HODL", "DAGGERHASHIMOTO", "DECRED", "CRYPTONIGHT", "LBRY", "EQUIHASH", "PASCAL", "X11GOST", "SIA", "BLAKE2S", "SKUNK", "CRYPTONIGHTV7", "CRYPTONIGHTHEAVY", "LYRA2Z", "X16R", "CRYPTONIGHTV8", "SHA256ASICBOOST", "ZHASH", "BEAM", "GRINCUCKAROO29", "GRINCUCKATOO31", "LYRA2REV3", "CRYPTONIGHTR", "CUCKOOCYCLE", "GRINCUCKAROOD29", "BEAMV2", "X16RV2", "RANDOMXMONERO", "EAGLESONG", "CUCKAROOM", "GRINCUCKATOO32", "HANDSHAKE", "KAWPOW", "CUCKAROO29BFC", "BEAMV3", "CUCKAROOZ29", "OCTOPUS" ] example: SHA256
    # status  string  Order status (optional, if not supplied, all order statuses are returned)          [ "PENDING", "ACTIVE", "PENDING_CANCELLATION", "CANCELLED", "DEAD", "EXPIRED", "ERROR", "ERROR_ON_CREATION", "ERROR_ON_CREATION_ON_REVERTING_TRANSACTIONS", "COMPLETED", "ERROR_MISSING" ] example: ACTIVE
    # active  boolean     Show only active or not active orders (optional, active orders: PENDING, ACTIVE, PENDING_CANCELLATION)       example: true
    # market  string  Filter by market place (optional)            [ "EU", "USA", "EU_N", "USA_E" ] example: EU
    # ts *    integer     Timestamp to compare           example: 255135600000000
    # op *    string  The order operator to compare timestamp             [ "GT", "GE", "LT", "LE" ] example: GT
    # limit *     integer     Max limit results         example: 100
    def get_my_active_orders(self, op, limit, algorithm="", status="", active=False, market="", timestamp=None):
        if not timestamp: timestamp = self.get_epoch_ms_from_now()
        query = "algorithm={algorithm}&market={market}&ts={timestamp}&limit={limit}&op={op}&active={active}&status={status}".format(active=active, algorithm=algorithm, limit=limit, market=market, op=op, status=status, timestamp=timestamp)
        return self.request('GET', '/main/api/v2/hashpower/myOrders', query, None)

    # Create hashpower order. When constructing order request, some limitation must be taken into 
    # consideration, like minimum amount, minimum speed limit, minimup price, ... Limitation varies 
    # among algorithms and can be fetched using /main/api/v2/public/buy/info endpoints.

    # There are differences between creating FIXED or STANDARD order. To create hashpower order, algorithm 
    # and market has to be specified. Before creating order pool has to be created for the same algorithm 
    # using /main/api/v2/pool endpoint.

    # When creating STANDARD order, speed limit, price, amount and pool id has to be specified, along with 
    # market factor and display market factor from /main/api/v2/public/buy/info endpoint for the same algorithm.
    def create_standard_hashpower_order(self, market, algorithm, price, limit, amount, pool_id):
        algo_response = self.get_algorithms()
        algo_setting = public_api.algo_settings_from_response(algo_response, algorithm)
        order_data = {
            "market": market,
            "algorithm": algorithm,
            "amount": amount,
            "price": price,
            "limit": limit,
            "poolId": pool_id,
            "type": "STANDARD",
            "marketFactor": algo_setting['marketFactor'],
            "displayMarketFactor": algo_setting['displayMarketFactor']
        }
        return self.request('POST', '/main/api/v2/hashpower/order/', '', order_data)

    # When creating FIXED order, first fixed price for selected speed limit must be acquired using 
    # /main/api/v2/hashpower/orders/fixedPrice. The result should be used in create hashpower order request. 
    # It can happen that fixed order price on the server changes before request is received. In that case 
    # fixed price must be aquired again and repeat create fixed order with new price values.

    # When creating FIXED order request, limit and price should not be different from fixedPrice response.
    def create_fixed_hashpower_order(self, market, algorithm, price, limit, amount, pool_id):
        algo_response = self.get_algorithms()
        algo_setting = public_api.algo_settings_from_response(algo_response, algorithm)
        fixed_price = self.fixed_price_request(algorithm, market, limit)
        order_data = {
            "market": market,
            "algorithm": algorithm,
            "amount": amount,
            "price": fixed_price["fixedPrice"],
            "limit": limit,
            "poolId": pool_id,
            "type": "FIXED",
            "marketFactor": algo_setting['marketFactor'],
            "displayMarketFactor": algo_setting['displayMarketFactor']
        }
        return self.request('POST', '/main/api/v2/hashpower/order/', '', order_data)

    # Get hashpower order detailed information using order id.
    def get_order_details(self, order_id):
        return self.request('GET', '/main/api/v2/hashpower/order/{id}'.format(id=order_id), '', None)

    # Cancel hashpower order using order id. Cancel action affects only active orders. When successful, affected order is returned in the response.
    def cancel_hashpower_order(self, order_id):
        return self.request('DELETE', '/main/api/v2/hashpower/order/{id}'.format(id=order_id), '', None)

    # When order is active, amount on the order can be increased and prolong duration of active order in marketplace. The limitation for minimal and maximal amount are defined for each algorithm and can be fetched using /main/api/v2/public/buy/info endpoint.
    def refill_hashpower_order(self, order_id, amount):
        refill_data = {
            "amount": amount
        }
        return self.request('POST', '/main/api/v2/hashpower/order/{id}/refill/'.format(id=order_id), '', refill_data)

    # Get statistical streams for selected order using order id. Result consists of following streams:
    # Timestamp in milliseconds since 1.1.1970
    # Is order alive
    # Accepted speed
    # Rejected speed - share above target
    # Rejected speed - stale shares
    # Rejected speed - duplicate shares
    # Rejected speed - invalid ntime
    # Rejected speed - other reason
    # Rejected speed - unknow worker
    # Rejected speed - response timeout
    # Speed limit
    # Rewareded speed
    # Paying speed
    # Rejected speed
    # Paid amount
    # Price
    def get_order_statistics(self, order_id):
        return self.request('GET' ,'/main/api/v2/hashpower/order/{id}/stats'.format(id=order_id), '', None)

    # At any time order speed limit and price can be altered when hashpower order is active. Changes must be withing limits defined for each algoritm separately. These limits can be fetched using /main/api/v2/public/buy/info endpoint. Order price can be decrease once in 10 minutes and the value of change must not be greater than more than down_step parameter from buy info endpoing.
    # price   number  Order price
    # limit   number  Order speed limit
    # displayMarketFactor     string  Used display market factor
    # marketFactor    number  Used display market factor (numeric)
    def set_price_hashpower_order(self, order_id, price, algorithm):
        algo_response = self.get_algorithms()
        algo_setting = public_api.algo_settings_from_response(algo_response, algorithm)
        price_data = {
            "price": price,
            "marketFactor": algo_setting['marketFactor'],
            "displayMarketFactor": algo_setting['displayMarketFactor']
        }
        return self.request('POST', '/main/api/v2/hashpower/order/{id}/updatePriceAndLimit/'.format(id=order_id), '', price_data)
    
    # At any time order speed limit and price can be altered when hashpower order is active. Changes must be withing limits defined for each algoritm separately. These limits can be fetched using /main/api/v2/public/buy/info endpoint. Order price can be decrease once in 10 minutes and the value of change must not be greater than more than down_step parameter from buy info endpoing.
    def set_limit_hashpower_order(self, order_id, limit, algorithm):
        algo_response = self.get_algorithms()
        algo_setting = public_api.algo_settings_from_response(algo_response, algorithm)
        limit_data = {
            "limit": limit,
            "marketFactor": algo_setting['marketFactor'],
            "displayMarketFactor": algo_setting['displayMarketFactor']
        }
        return self.request('POST', '/main/api/v2/hashpower/order/{id}/updatePriceAndLimit/'.format(id=order_id), '', limit_data)
    
    # At any time order speed limit and price can be altered when hashpower order is active. Changes must be withing limits defined for each algoritm separately. These limits can be fetched using /main/api/v2/public/buy/info endpoint. Order price can be decrease once in 10 minutes and the value of change must not be greater than more than down_step parameter from buy info endpoing.
    def set_price_and_limit_hashpower_order(self, order_id, price, limit, algorithm):
        algo_response = self.get_algorithms()
        algo_setting = public_api.algo_settings_from_response(algo_response, algorithm)
        price_data = {
            "price": price,
            "limit": limit,
            "marketFactor": algo_setting['marketFactor'],
            "displayMarketFactor": algo_setting['displayMarketFactor']
        }
        return self.request('POST', '/main/api/v2/hashpower/order/{id}/updatePriceAndLimit/'.format(id=order_id), '', price_data)

    # Estimated duration of a hashpower order from the order type, amount, price and limit. 
    # The maximal value for STANDARD order is 10 days and for FIXED order 1 day.
    # type    string  Order   [ "STANDARD", "FIXED" ]
    # price   number  Price
    # limit   number  Speed limit
    # amount  number  Amount
    # decreaseFee     boolean     Should be amount decrease by fee amount before estimation
    # displayMarketFactor     string  Unit of market factor
    # marketFactor    number  Market factor
    def estimate_order_duration(self, algorithm, order_type, price, limit, amount, decreaseFee=False):
        algo_response = self.get_algorithms()
        algo_setting = public_api.algo_settings_from_response(algo_response, algorithm)
        estimate_data = {
            "type": order_type,
            "price": price,
            "amount": amount,
            "limit": limit,
            "decreaseFee": decreaseFee,
            "marketFactor": algo_setting['marketFactor'],
            "displayMarketFactor": algo_setting['displayMarketFactor']
        }
        return self.request('POST', '/main/api/v2/hashpower/orders/calculateEstimateDuration', '', estimate_data)
       

    #############################################################################################

    # Miner private REST API methods

    # List of groups with list of rigs in the groups. When extendedResponse is set to true, response contains number of total and active devices for each rig and group.
    # extendedResponse    boolean     Extended Response
    def get_groups(self, extendedResponse=False):
        query = "extendedResponse={extendedResponse}".format(extendedResponse=extendedResponse)
        return self.request('GET', '/main/api/v2/mining/groups/list', query, None)
        # {
        #     groups : {
        #     {
        #         rigs : [
        #         {
        #             rigId : string - Rig id
        #             name : string - Rig name (if rig is unamanaged, then name is worker id)
        #             status : string - Rig status - BENCHMARKING, MINING, STOPPED, OFFLINE, ERROR, PENDING, DISABLED, TRANSFERRED, UNKNOWN
        #             powerMode : string - Rig's devices power mode - UNKNOWN, LOW, MEDIUM, HIGH, MIXED
        #             notifications : [
        #             string - Rig Notifications - UNKNOWN, RIG_OFFLINE, RIG_ERROR, UNRECOGNIZED
        #             ]
        #             totalDevices : integer - Total devices on rig
        #             activeDevices : integer - Active devices on rig
        #             }
        #         ]
        #         totalRigs : integer - Number of total devices in group
        #         miningRigs : integer - Number of active devices
        #         groupPowerMode : string - Group power mode combined from all devices in group or group's subgroup - UNKNOWN, LOW, MEDIUM, HIGH, MIXED
        #         notifications : {
        #         string - Rig Notifications of rigs in group with - ALL, PARTIAL
        #         }
        #         }
        #     }
        # }

    # Getting mining address.
    def get_mining_address(self):
        return self.request('GET', '/main/api/v2/mining/miningAddress', '', None)

    # Get statistical streams for selected rigs and selected algorithm. Algorithm code can be found in buy info endpoint. Result consists of following streams:
    # Timestamp in milliseconds since 1.1.1970
    # Total unpaid amount
    # Accepted speed
    # Rejected speed - share above target
    # Rejected speed - stale shares
    # Rejected speed - duplicate shares
    # Rejected speed - invalid ntime
    # Rejected speed - other issues
    # Profitability

    # rigId *     string  Consolidated rigId
    # algorithm *     integer     Algorithm code
    # afterTimestamp  integer     After timestamp (inclusive, default: now - 1 days)
    # beforeTimestamp     integer     Before timestamp (exclusive)
    def get_rig_algo_stats(self, rig_id, afterTimestamp=-1, beforeTimestamp=-1):
        query = "rigId={id}&afterTimestamp={afterTimestamp}&beforeTimestamp={beforeTimestamp}".format(id=rig_id, afterTimestamp=afterTimestamp, beforeTimestamp=beforeTimestamp)
        return self.request('GET', '/main/api/v2/mining/rig/stats/algo', query, None)

    # Get statistical streams for selected rig. Result consists of following streams:
    # Timestamp in milliseconds since 1.1.1970
    # Algorithm code
    # Total unpaid amount
    # Total unpaid amount for the algorithm
    # Profitability

    # rigId *     string  Consolidated rigId
    # afterTimestamp  integer     After timestamp in milliseconds since 1.1.1970 (inclusive, default: now - 1 days)
    # beforeTimestamp     integer     Before timestamp in milliseconds since 1.1.1970 (exclusive)
    def get_rig_unpaid_stats(self, rig_id, afterTimestamp=-1, beforeTimestamp=-1):
        query = "rigId={id}&afterTimestamp={afterTimestamp}&beforeTimestamp={beforeTimestamp}".format(id=rig_id, afterTimestamp=afterTimestamp, beforeTimestamp=beforeTimestamp)
        return self.request('GET', '/main/api/v2/mining/rig/stats/unpaid', query, None)

    # Get mining rig detailed information for selected rig.
    # rigId *     string  Consolidated rigId
    def get_rig_by_id(self, rig_id):
        return self.request('GET', '/main/api/v2/mining/rig2/{id}'.format(id=rig_id), '', None)

    # Get a list of active worker.
    # btcAddress *    string  Btc address
    # size    integer     Number of elements per page      100
    # page    integer     Page number      0
    # sortParameter   string  Sort parameter        RIG_NAME            [ "RIG_NAME", "TIME", "MARKET", "ALGORITHM", "UNPAID_AMOUNT", "DIFFICULTY", "SPEED_ACCEPTED", "SPEED_REJECTED", "PROFITABILITY" ]
    # sortDirection   string  Sort direction      ASC                   [ "ASC", "DESC" ]
    def get_active_workers(self, btcAddress, size=100, page=0, sortParameter="RIG_NAME", sortDirection="ASC"):
        return self.request('GET', '/main/api/v2/mining/rigs/activeWorkers', '', None)

    # Get list of payouts. 
    # beforeTimestamp     integer     Before timestamp in milliseconds from 1.1.1970 (default: from now)
    # size    integer     Size
    # page    integer     Page
    def get_payouts(self):
        return self.request('GET', '/main/api/v2/mining/rigs/payouts', '', None)

    # Get statistical streams for all mining rigs for selected algorithm. Algorithm code can be found in buy info endpoint. Result consists of following streams:
    # Timestamp in milliseconds since 1.1.1970
    # Accepted speed
    # Rejected speed - share above target
    # Rejected speed - stale shares
    # Rejected speed - duplicate shares
    # Rejected speed - invalid ntime
    # Rejected speed - other issues
    # Profitability

    # algorithm *     integer     Algorithm for stats
    # afterTimestamp  integer     After timestamp (inclusive, default: now - 7 days)
    # beforeTimestamp     integer     Before timestamp (exclusive, default: now)
    def get_algo_statistics(self, algorithm, afterTimestamp=-1, beforeTimestamp=-1):
        query = "algorithm={algorithm}&afterTimestamp={afterTimestamp}&beforeTimestamp={beforeTimestamp}".format(algorithm=algorithm, afterTimestamp=afterTimestamp, beforeTimestamp=beforeTimestamp)
        return self.request('GET', '/main/api/v2/mining/rigs/stats/algo', query, None)

    # Get statistical streams for all mining rigs. Result consists of following streams:
    # Timestamp in milliseconds since 1.1.1970
    # Algorithm code
    # Total unpaid amount
    # Total unpaid amount for the algorithm
    # Profitability
    # Balance

    # afterTimestamp  integer     After timestamp (inclusive, default: now - 7 days)
    # beforeTimestamp     integer     Before timestamp (exclusive, default: now)
    def get_unpaid_statistics(self):
        return self.request('GET', '/main/api/v2/mining/rigs/stats/unpaid', '', None)

    # Update status for one or more rigs with following actions:
    # Start mining,
    # stop mining,
    # set power mode.
    
    # group   string  Mining rig group. When group is empty, all rigs are affected.
    # rigId   string  Rig id
    # deviceId    string  Device id
    # action  string  Action      [ "START", "STOP", "POWER_MODE" ]
    # options     array   List of options
    def update_status(self, action, group_name="", rig_id="", device_id="", options=None):
        status_data = {
            "group": group_name,
            "rigId": rig_id,
            "deviceId": device_id,
            "action": action,
            "options": options
        }
        return self.request('POST', '/main/api/v2/mining/rigs/status2', '', status_data)

    # List rigs and their statuses. Path parameter filters rigs by group. When path is empty, rigs from root group are returned. Rigs can be sorted according to sort parameter.
    # size    integer     Size           25
    # page    integer     Page           0
    # path    string  Path
    # sort    string  Sort        [ "NAME", "PROFITABILITY", "ACTIVE", "INACTIVE" ]
    # system  string  System              example: NHM,NHOS,NHQM
    # status  string  Status                example: Mining,Offline
    def get_rigs(self, size=25, page=0, path="", sort="NAME", system="", status=""):
        return self.request('GET', '/main/api/v2/mining/rigs2', '', None)

    #############################################################################################

    # Pools REST API methods

    # Create or edit pool information. When creating pool, id of pool must not be in the request message. When editing id must match existing pool id, otherwise request will fail. Response contains created or edited pool detailed information.
    # id  string  Pool id (When creating new pool this value should not be set.)
    # name    string  Pool custom name
    # algorithm   string  Pool algorithm          [ "SCRYPT", "SHA256", "SCRYPTNF", "X11", "X13", "KECCAK", "X15", "NIST5", "NEOSCRYPT", "LYRA2RE", "WHIRLPOOLX", "QUBIT", "QUARK", "AXIOM", "LYRA2REV2", "SCRYPTJANENF16", "BLAKE256R8", "BLAKE256R14", "BLAKE256R8VNL", "HODL", "DAGGERHASHIMOTO", "DECRED", "CRYPTONIGHT", "LBRY", "EQUIHASH", "PASCAL", "X11GOST", "SIA", "BLAKE2S", "SKUNK", "CRYPTONIGHTV7", "CRYPTONIGHTHEAVY", "LYRA2Z", "X16R", "CRYPTONIGHTV8", "SHA256ASICBOOST", "ZHASH", "BEAM", "GRINCUCKAROO29", "GRINCUCKATOO31", "LYRA2REV3", "CRYPTONIGHTR", "CUCKOOCYCLE", "GRINCUCKAROOD29", "BEAMV2", "X16RV2", "RANDOMXMONERO", "EAGLESONG", "CUCKAROOM", "GRINCUCKATOO32", "HANDSHAKE", "KAWPOW", "CUCKAROO29BFC", "BEAMV3", "CUCKAROOZ29", "OCTOPUS" ]
    # stratumHostname     string  Hostname or ip of the pool
    # stratumPort     integer     Port of the pool
    # username    string  Username
    # password    string  Password (Set password to # when using ethproxy pool.)
    # status  string  Verification status     [ "VERIFIED", "NOT_VERIFIED" ]
    # updatedTs   string  
    # inMoratorium    boolean     
    def create_pool(self, name, algorithm, pool_host="", pool_port=0, username="", password=""):
        pool_data = {
            "name": name,
            "algorithm": algorithm,
            "stratumHostname": pool_host,
            "stratumPort": pool_port,
            "username": username,
            "password": password
        }
        return self.request('POST', '/main/api/v2/pool/', '', pool_data)

    # Get pool information using pool id.
    # poolId *    string  Pool id
    def get_pool(self, pool_id):
        return self.request('GET', '/main/api/v2/pool/{id}'.format(id=pool_id), '', None)

    # Delete pool using pool id. The operation is not reversible.
    # poolId *    string  Pool id
    def delete_pool(self, pool_id):
        return self.request('DELETE', '/main/api/v2/pool/{id}'.format(id=pool_id), '', None)

    # Fetch whole pool list. When more than 100 pools are contained in the list, pages should be used. Algorithm parameter can be used to filter out pools for selected algorithm.
    # size    integer     Size    100     example: 100
    # page    integer     Page     0   example: 0
    # algorithm   string  Mining algorithm (optional, if not supplied all algorithms are returned)    [ "SCRYPT", "SHA256", "SCRYPTNF", "X11", "X13", "KECCAK", "X15", "NIST5", "NEOSCRYPT", "LYRA2RE", "WHIRLPOOLX", "QUBIT", "QUARK", "AXIOM", "LYRA2REV2", "SCRYPTJANENF16", "BLAKE256R8", "BLAKE256R14", "BLAKE256R8VNL", "HODL", "DAGGERHASHIMOTO", "DECRED", "CRYPTONIGHT", "LBRY", "EQUIHASH", "PASCAL", "X11GOST", "SIA", "BLAKE2S", "SKUNK", "CRYPTONIGHTV7", "CRYPTONIGHTHEAVY", "LYRA2Z", "X16R", "CRYPTONIGHTV8", "SHA256ASICBOOST", "ZHASH", "BEAM", "GRINCUCKAROO29", "GRINCUCKATOO31", "LYRA2REV3", "CRYPTONIGHTR", "CUCKOOCYCLE", "GRINCUCKAROOD29", "BEAMV2", "X16RV2", "RANDOMXMONERO", "EAGLESONG", "CUCKAROOM", "GRINCUCKATOO32", "HANDSHAKE", "KAWPOW", "CUCKAROO29BFC", "BEAMV3", "CUCKAROOZ29", "OCTOPUS" ] example: SHA256
    def get_my_pools(self, algorithm="", size=100, page=0):
        query = "size={size}&page={page}&algorithm={algorithm}".format(size=size, page=page, algorithm=algorithm)
        return self.request('GET', '/main/api/v2/pools/', query, None)

    # Verify connectivity between Nicehash stratum server and selected pool. Basic pool data are also checked like authentication, size of extranonoce, initial difficulty and structure of jobs. This verification cannot find incompatibility or validity of shares sent to the pool. Please note that checks are not complete and there are rare cases where verification cannot identify incompatible pool. 
    def verify_pool(self, market="", algorithm="", pool_host="", pool_port=-1, username="", password=""):
        pool_data = {
            "poolVerificationServiceLocation": market,
            "miningAlgorithm": algorithm,
            "stratumHost": pool_host, # 'stratumHost' instead of 'stratumHostname' from create_pool 
            "stratumPort": pool_port,
            "username": username,
            "password": password
        }
        return self.request('POST', '/main/api/v2/pools/verify', '', pool_data)

    #############################################################################################

    # Exchange private REST API methods

    # Cancel all orders on enumerated markets for organisation that apikey was generated. One or more markets can be enumerated. If no market is defined than orders in all markets will be canceled. Result contains list of orders on markets that were selected for cancellation. When organisation has huge amount of orders in the order book, only subset of orders are selected for the cancellation. In that case this endpoint should be called multiple times. When order is successfully cancelled, the order is in state CANCELLED.
    # market    string  Market symbol - if not defined, orders on all markets are canceled
    # side    string  Order side - if not defined, all orders are canceled
    def cancel_all_orders(self, market="", side=""):
        query = "market={market}&side={side}".format(market=market, side=side)
        return self.request('DELETE', '/exchange/api/v2/info/cancelAllOrders', query, None)

    # According to fee rules, users organisation can lower fee rate for exchange trades. This endpoint returns current fee rates for current organisation and list of fee rules for maket and taker side.
    def get_fee_status(self):
        return self.request('GET', '/exchange/api/v2/info/fees/status', '', None)

    # Get a single order by order ID. Order must be one of orders that have been created in my organisation.
    # market *    string  Market symbol
    # orderId *   string  Order ID
    def get_my_order(self, market, orderId):
        query = "market={market}&orderId={orderId}".format(market=market, orderId=orderId)
        return self.request('GET', '/exchange/api/v2/info/myOrder', query, None)

    # Get a list of my orders matching the filtering criteria as specified.
    # market *    string  Market symbol
    # orderState  string  Order state (optional)
    # orderStatus     string  Order status (optional)
    # sortDirection   string  Sort direction (optional, default value is DESC)
    # limit   integer     Query limit (optional, default value is 25)
    # timestamp   integer     Select older than timestamp in µs (optional, default value is current timestamp)
    def get_my_orders(self, marketSymbol, orderState="", orderStatus="", sortDirection="DESC", limit=25, timestamp=None):
        if not timestamp: timestamp = self.get_epoch_ms_from_now()
        query = "market={market}&orderState={orderState}&orderStatus={orderStatus}&sortDirection={sortDirection}&limit={limit}&timestamp={timestamp}".format(market=marketSymbol, orderState=orderState, orderStatus=orderStatus, sortDirection=sortDirection, limit=limit, timestamp=timestamp)
        return self.request('GET', '/exchange/api/v2/info/myOrders', query, None)

    # Get the list of trades that were executed on my orders matching the filtering criteria as specified.
    # market *    string  Market symbol
    # sortDirection   string  Sort direction (optional, default value is DESC)
    # limit   integer     Query limit (optional, default value is 25)
    # timestamp   integer     Select older than timestamp in µs (optional, default value is current timestamp)
    def get_my_trades(self, market, sortDirection="DESC", limit=25, timestamp=None):
        if not timestamp: timestamp = self.get_epoch_ms_from_now()
        query = "market={market}&sortDirection={sortDirection}&limit={limit}&timestamp={timestamp}".format(market=market, sortDirection=sortDirection, limit=limit, timestamp=timestamp)
        return self.request('GET', '/exchange/api/v2/info/myTrades', query, None)

    # Get trades for the specified order. Order must be created within my organisation.
    # market *    string  Market symbol
    # orderId *   string  Order ID
    # sortDirection   string  Sort direction (optional, default value is DESC)
    def get_trades_for_order(self, market, orderId, sortDirection="DESC"):
        query = "market={market}&orderId={orderId}&sortDirection={sortDirection}".format(market=market, orderId=orderId, sortDirection=sortDirection)
        return self.request('GET', '/exchange/api/v2/info/orderTrades', query, None)

    # Two types or order can be created:
    # limit,
    # market.

    # Each type of order requires different set of parameters. For each market, rules about minimum
    #  and maximum asset values are defined and can be fetched using market 
    #  status API (/exchange/api/v2/info/status).
    # Organisation must have sufficient balance of base or quote assets depending of the order 
    # direction. Order can be placed when market status is TRADING state only.

    # Following rules are defined when placing orders:
    # LIMIT order must have price and quantity parameter.
    # SELL MARKET order must have quantity parameter. (Optionally minSecQuaity parameter can be 
    #     added to the request. This parameter ensures the minimum quote quantity that will be 
    #     produced from request or request will fail with error).
    # BUY MARKET order must have quantity parameter. (Optionally minQuantity parameter can be 
    #     added to the request. This parameter ensures the minimum base quantity that will be 
    #     produced from request or request will fail with error).

    # Response contains created exchange order after the matching engine processed the order. 
    # In a case that not all conditions for placing exchange are met response contains appropriate error.

    # When order doesn't hit any matching order, orders remains in orderbook and state of the order is ENTERED. 
    # If orders finds a match with one or more orders that have together lower quantity, order is partialy 
    # executed and state of the order is PARTIAL. When order finds a match with one or more order that have
    #  together higher quantity, order is fully executed in state of order is FULL. The result of order 
    #  execution are one or more trades.

    # market *    string  Market symbol
    # side *  string  Order side            [ "BUY", "SELL" ]
    # type *  string  Order type        [ "LIMIT", "MARKET" ] 
    # quantity *  number  Order (base) quantity for LIMIT or SELL MARKET order 
    # price *     number  Order price for LIMIT order
    # minSecQuantity *    number  Minimum order secondary (quote) quantity for SELL MARKET order (optional)
    # secQuantity *   number  Order secondary (quote) quantity for BUY MARKET order
    # minQuantity *   number  Minimum order (base) quantity for BUY MARKET order (optional)

    def create_exchange_limit_order(self, market, side, quantity, price):
        query = "market={market}&side={side}&type=limit&quantity={quantity}&price={price}".format(market=market, side=side, quantity=quantity, price=price)
        return self.request('POST', '/exchange/api/v2/order', query, None)

    def create_exchange_buy_market_order(self, market, quantity, secQuantity, minQuantity=None):
        query = "market={market}&side=buy&type=market&secQuantity={secQuantity}&minQuantity={minQuantity}".format(market=market, quantity=quantity, secQuantity=secQuantity, minQuantity=minQuantity)
        return self.request('POST', '/exchange/api/v2/order', query, None)

    def create_exchange_sell_market_order(self, market, quantity, minSecQuantity):
        query = "market={market}&side=sell&type=market&quantity={quantity}&minSecQuantity={minSecQuantity}".format(market=market, quantity=quantity, minSecQuantity=minSecQuantity)
        return self.request('POST', '/exchange/api/v2/order', query, None)

    # Cancel the specified order. If succesfull the response contains cancelled order with order state set to CANCELLED. Exchange orders that are in state ENTERED or PARTIAL can be cancelled, otherwiseerror message is returned.
    # market *    string  Market symbol
    # orderId *   string  Order ID
    def cancel_exchange_order(self, market, order_id):
        query = "market={market}&orderId={orderId}".format(market=market, orderId=order_id)
        return self.request('DELETE', '/exchange/api/v2/order', query, None)

    #############################################################################################

    ###########
    # Removed #
    ###########

    # def get_withdrawal_types(self):
    #     return self.request('GET', '/main/api/v2/accounting/withdrawalAddresses/types/', '', None)

    # def get_my_exchange_orders(self, market):
    #     return self.request('GET', '/exchange/api/v2/myOrders', 'market=' + market, None)

    # def get_my_exchange_trades(self, market):
    #     return self.request('GET','/exchange/api/v2/myTrades', 'market=' + market, None)

class websockets_api(public_api):

    def __init__(self, host, organisation_id, key, secret, verbose=False):
        self.key = key
        self.secret = secret
        self.organisation_id = organisation_id
        self.host = host
        self.verbose = verbose


        self.session = requests.Session()

    def close(self):
        self.session.close()

    def request(self, method, path, query, body):

        xtime = self.get_epoch_ms_from_now()
        xnonce = str(uuid.uuid4())

        message = bytearray(self.key, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(str(xtime), 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(xnonce, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(self.organisation_id, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(method, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(path, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(query, 'utf-8')

        if body:
            body_json = json.dumps(body)
            message += bytearray('\x00', 'utf-8')
            message += bytearray(body_json, 'utf-8')

        digest = hmac.new(bytearray(self.secret, 'utf-8'), message, sha256).hexdigest()
        xauth = self.key + ":" + digest

        headers = {
            'X-Time': str(xtime),
            'X-Nonce': xnonce,
            'X-Auth': xauth,
            'Content-Type': 'application/json',
            'X-Organization-Id': self.organisation_id,
            'X-Request-Id': str(uuid.uuid4())
        }

        s = requests.Session()
        s.headers = headers

        url = self.host + path
        if query:
            url += '?' + query

        if self.verbose:
            print(method, url)

        if body:
            response = s.request(method, url, data=body_json)
        else:
            response = s.request(method, url)

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(str(response.status_code) + ": " + response.reason + ": " + str(response.content))
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)

    # WSS

    # Messages
    # Candlestick Stream

    # ws
    # Subscribe Candlestick Stream
    # Subscribe to candlestick stream. When subscription is successful, last candlestick is returned in message with method c.s. Later updates are sent in messages with method c.u. Request must specify resolution parameter. Supported resolutions are: 1 (minute), 60 (hour), 1440 (day). Only one candlestick subscription is possible at the same time.
    # m   string  Method must be "subscribe.candlesticks"
    # r   number  Candlesticks resolution      [ 1, 60, 1440 ]
    def subscribe_candlestick_stream(self, r):
        data = {
            "m": "subscribe.candlesticks",
            "r": r
        }
        return self.request('GET', '', '', data)

    # ws
    # Unsubscribe Candlestick Stream
    # Unsubscribe from candlesticks stream. No further messages from this stream should be received.
    # m   string  Method must be "unsubscribe.candlesticks"
    def unsubscribe_candlestick_stream(self):
        data = {
            "m": "unsubscribe.candlesticks"
        }
        return self.request('GET', '', '', data)

    # MyTrade stream
    # ws
    # Subscribe My Trade Stream
    # Subscribe to my trade stream. When subscribed, list of last trades is received in message with method mt.s. New trades are received later in messages with method mt.u.
    # m   string  Method should be "subscribe.mytrades"
    def subscribe_trade_stream(self):
        data = {
            "m": "subscribe.mytrades"
        }
        return self.request('GET', '', '', data)

    # ws
    # Unsubscribe My Trade Stream
    # Unsubscribe from my trade stream. No further messages from this stream should be received.
    # m   string  Method should be "subscribe.mytrades" (typo in docs) -> "unsubscribe.mytrades"
    def unsubscribe_trade_stream(self):
        data = {
            "m": "unsubscribe.mytrades"
        }
        return self.request('GET', '', '', data)

    # Order Manipulation

    # ws
    # Cancel All Orders
    # Cancel all orders on a market. Result contains list of orders that were selected for cancellation. When organisation has huge amount of orders in the order book, only subset of orders are selected for the cancellation. In that case this endpoint should be called multiple times. When order is successfully cancelled, the order is in state CANCELLED.
    # m   string  Method must be "o.ca.all"
    # i   string  Message id - any string selected by client
    # s   string  Order side, if order side is not in the request, all orders are canceled        [ "BUY", "SELL" ]
    def cancel_all_orders(self, message_id="", side=""):
        data = {
            "m": "o.ca.all",
            "i": message_id,
            "s": side
        }
        return self.request('GET', '', '', data)

    # ws
    # Cancel Order
    # Cancel selected order with order id.
    # m   string  Method must be "o.ca"
    # i   string  Message id - any string selected by client
    # oid     string  Order id
    def cancel_order(self, message_id="", order_id=""):
        data = {
            "m": "o.ca",
            "i": message_id,
            "oid": order_id
        }
        return self.request('GET', '', '', data)

    # ws
    # Create Order
    # Order Stream
    # Two types or order can be created:
    # limit,
    # market.
    # m   string  Method must be "o.cr"
    # i   string  Message id - any string selected by client
    # sd  string  Order side       [ "BUY", "SELL" ]
    # tp  string  Order type         [ "LIMIT", "MARKET" ]
    # qt  string  Order (base) quantity for LIMIT or SELL MARKET order
    # pr  string  Order price for LIMIT order
    # msqt    string  Minimum order secondary (quote) quantity for SELL MARKET order (optional)
    # sqt     string  Order secondary (quote) quantity for BUY MARKET order
    # mqt     string  Minimum order (base) quantity for BUY MARKET order (optional)

    def create_limit_order(self, message_id, side, quantity, price):
        data = {
            "m": "o.cr",
            "i": message_id,
            "sd": side,
            "tp": "LIMIT",
            "qt": quantity,
            "pr": price
        }
        return self.request('GET', '', '', data)

    def create_buy_market_order(self, message_id, quantityQuote, quantityBase=""):
        data = {
            "m": "o.cr",
            "i": message_id,
            "sd": "BUY",
            "tp": "MARKET",
            "sqt": quantityQuote,
            "mqt": quantityBase
        }
        return self.request('GET', '', '', data)

    def create_sell_market_order(self, message_id, quantity, minSecQuantity=""):
        data = {
            "m": "o.cr",
            "i": message_id,
            "sd": "SELL",
            "tp": "MARKET",
            "qt": quantity,
            "msqt": minSecQuantity
        }
        return self.request('GET', '', '', data)

    # ws
    # Subscribe Order Stream
    # Subscribe to order stream where only my orders will be received. When subscribing, reponse message will be sent with method o.s. Later order updates will be sent in messages with method o.u. 
    # m   string  Method must be "subscribe.orders"
    def subscribe_order_stream(self):
        data = {
            "m": "subscribe.orders"
        }
        return self.request('GET', '', '', data)        

    # ws
    # Unsubscribe Order Stream
    # Unsubscribe from orders stream. No further messages from this stream should be received.
    # m   string  Method must be "unsubscribe.orders"
    def unsubscribe_order_stream(self):
        data = {
            "m": "unsubscribe.orders"
        }
        return self.request('GET', '', '', data)

    # Orderbook Stream

    # ws
    # Subscribe Order Book Stream
    # Subscribe to order book stream. Order book state is returned after orderbook subscribe message with method ob.s. Later only the order book changes are notified with messages with method ob.u. When orderbook update contains price with value 0, entry is cleared from order book. 
    # m   string  Method must be "subscribe.orderbook"
    def subscribe_order_book_stream(self):
        data = {
            "m": "subscribe.orderbook"
        }
        return self.request('GET', '', '', data)

    # ws
    # Unsubscribe Order Book Stream
    # Unsubscribe from orderbook stream. No further messages from this stream should be received.
    # m   string  Method must be "unsubscribe.orderbook"
    def unsubscribe_order_book_stream(self):
        data = {
            "m": "subscribe.orderbook"
        }
        return self.request('GET', '', '', data)

    # Trade Stream

    # ws
    # Subscribe Trade Stream
    # Subscribe to trade stream. When subscribed, list of last trades is received in message with method m.s. New trades are received later in messages with method m.u.
    # m   string  Method must be "subscribe.trades"
    def subscribe_trade_stream(self):
        data = {
            "m": "subscribe.trades"
        }
        return self.request('GET', '', '', data)

    # ws
    # Unsubscribe Trade Stream
    # Unsubscribe from trades stream. No further messages from this stream should be received.
    # m   string  Method must be "unsubscribe.trades"
    def unsubscribe_order_stream(self):
        data = {
            "m": "unsubscribe.trades"
        }
        return self.request('GET', '', '', data)

def main():
    parser = optparse.OptionParser()

    parser.add_option('-b', '--base_url', dest="base", help="Api base url", default="https://api2.nicehash.com")
    parser.add_option('-o', '--organization_id', dest="org", help="Organization id")
    parser.add_option('-k', '--key', dest="key", help="Api key")
    parser.add_option('-s', '--secret', dest="secret", help="Secret for api key")
    parser.add_option('-m', '--method', dest="method", help="Method for request", default="GET")
    parser.add_option('-p', '--path', dest="path", help="Path for request", default="/")
    parser.add_option('-q', '--params', dest="params", help="Parameters for request")
    parser.add_option('-d', '--body', dest="body", help="Body for request")

    options, args = parser.parse_args()

    _private_api = private_api(options.base, options.org, options.key, options.secret)

    query = ''
    if options.params is not None:
        query = options.params

    try:
        response = _private_api.request(options.method, options.path, query, options.body)
    except Exception as ex:
        print("Unexpected error:", ex)
        exit(1)

    print(response)
    exit(0)

if __name__ == "__main__":
    main()
