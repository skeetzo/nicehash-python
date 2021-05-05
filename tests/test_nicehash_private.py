import unittest
import os
import time
from dotenv import load_dotenv
load_dotenv()
#
from python import nicehash

ADDRESS = os.environ.get("TEST_ADDRESS") # needs to be Nicehash BTC address with active miners
HOST = os.environ.get("TEST_HOST")
ORGANIZATION_ID = os.environ.get("TEST_ORGANIZATION_ID")
KEY = os.environ.get("TEST_KEY")
SECRET = os.environ.get("TEST_SECRET")
###
# Parameters for testing
###
# ACTIVITY_TYPES = nicehash.ACTIVITY_TYPES[0]
ALGORITHM = nicehash.ALGORITHMS[0]
ALGORITHM_CODES = nicehash.ALGORITHM_CODES
ALGORITHM_CODE = ALGORITHM_CODES[0]
AMOUNT = 1
CURRENCY = "TBTC"
LIMIT = 0.0001
MARKET = nicehash.MARKETS[0]
MARKET_LONG = nicehash.MARKETS_LONG[0]
MARKET_SYMBOLS = ["TETHTBTC", "TBTCTUSDT", "TBCHTBTC"]
MARKET_SYMBOL = MARKET_SYMBOLS[0]
RESOLUTION = nicehash.RESOLUTIONS[0]
OP = nicehash.OPS[0]
# ORDER_RELATION = nicehash.ORDER_RELATION[0]
EXCHANGE_ORDER_TYPE = nicehash.EXCHANGE_ORDER_TYPES[0]
HASHPOWER_ORDER_TYPE = nicehash.HASHPOWER_ORDER_TYPES[0]
PAGE = 0
PRICE = 0.0001
RESULTS_LIMIT = 100
QUANTITY = 1
SEC_QUANTITY = 0
min_SEC_QUANTITY = 0
RIG_ACTION = nicehash.RIG_ACTIONS[0]
SIZE = 100
SORT_PARAMETER = nicehash.SORT_PARAMETERS[0]
SORT_DIRECTION = nicehash.SORT_DIRECTIONS[0]
SORT_OPTION = nicehash.SORT_OPTIONS[0]
SIDE = nicehash.SIDES[0]
STATUS = nicehash.STATUSES[0]
TIMESTAMP = int(time.time())
# TRANSACTION_TYPE = nicehash.TX_TYPES[0]
# WALLET_TYPE = nicehash.WALLET_TYPES[0]
WITHDRAWAL_AMOUNT = 1
#
FROM_S = int(time.time()) - 300
TO_S = FROM_S
# TODO
# have a mining rig on test net?
# or use public and get mining rig ID
RIG_ID = None
# TODO
# create group name on test net?
# create group name on live?
RIG_GROUP_NAME = None
ORDER_ID = None
TRANSACTION_ID = None
WITHDRAWAL_ID = None
# TODO
# any pool stuff
POOL_ID = None
POOL_NAME = None
POOL_PORT = 3443
POOL_HOST = None
POOL_USERNAME = None
POOL_PASSWORD = None
# TODO
WHITELISTED_WITHDRAWAL_ADDRESS_ID = None
###

# test values in lists
TEST_LISTS = False
# For selectively mass testing, ignoring tests that fail because rigs or orders don't exist to check
TESTING_URIS = [
	"/main/api/v2/accounting/account2/{currency}",
	"/main/api/v2/accounting/accounts2",
	"/main/api/v2/accounting/activity/{currency}",
	"/main/api/v2/accounting/depositAddresses",
	"/main/api/v2/accounting/deposits/{currency}",
	"/main/api/v2/accounting/deposits2/{currency}/{id}",
	"/main/api/v2/accounting/exchange/{id}/trades",
	"/main/api/v2/accounting/hashpower/{id}/transactions",
	"/main/api/v2/accounting/hashpowerEarnings/{currency}",
	"/main/api/v2/accounting/transaction/{currency}/{transactionId}",
	"/main/api/v2/accounting/transactions/{currency}",
	"/main/api/v2/accounting/withdrawal",
	"/main/api/v2/accounting/withdrawal/{currency}/{id}",
	"/main/api/v2/accounting/withdrawal2/{currency}/{id}",
	"/main/api/v2/accounting/withdrawalAddress/{id}",
	"/main/api/v2/accounting/withdrawalAddresses",
	"/main/api/v2/accounting/withdrawals/{currency}",
	"/main/api/v2/hashpower/myOrders",
	"/main/api/v2/hashpower/order",
	"/main/api/v2/hashpower/order/{id}",
	"/main/api/v2/hashpower/order/{id}",
	"/main/api/v2/hashpower/order/{id}/refill",
	"/main/api/v2/hashpower/order/{id}/stats",
	"/main/api/v2/hashpower/order/{id}/updatePriceAndLimit",
	"/main/api/v2/hashpower/orders/calculateEstimateDuration",
	"/main/api/v2/mining/groups/list",
	"/main/api/v2/mining/miningAddress",
	"/main/api/v2/mining/rig/stats/algo",
	"/main/api/v2/mining/rig/stats/unpaid",
	"/main/api/v2/mining/rig2/{rigId}",
	"/main/api/v2/mining/rigs/activeWorkers",
	"/main/api/v2/mining/rigs/payouts",
	"/main/api/v2/mining/rigs/stats/algo",
	"/main/api/v2/mining/rigs/stats/unpaid",
	"/main/api/v2/mining/rigs/status2",
	"/main/api/v2/mining/rigs2",
	"/main/api/v2/pool",
	"/main/api/v2/pool/{poolId}",
	"/main/api/v2/pool/{poolId}",
	"/main/api/v2/pools",
	"/main/api/v2/pools/verify",
	"/exchange/api/v2/info/cancelAllOrders",
	"/exchange/api/v2/info/fees/status",
	"/exchange/api/v2/info/myOrder",
	"/exchange/api/v2/info/myOrders",
	"/exchange/api/v2/info/myTrades",
	"/exchange/api/v2/info/orderTrades",
	"/exchange/api/v2/order",
	"/exchange/api/v2/order"
]
VERBOSE = True

def check_test_paramters(parameters):
	for p in parameters:
		if "algorithm_code" in str(p):
			if (not ALGORITHM_CODES or len(ALGORITHM_CODES) == 0 or not ALGORITHM_CODE) or (not MARKET_SYMBOLS or len(MARKET_SYMBOLS) == 0 or not MARKET_SYMBOL):
				raise Exception("Missing test value: {}".format(p))
		if not globals()[p.upper()]: raise Exception("Missing test value: {}".format(p))

class TestNiceHashPrivate(unittest.TestCase):

	def setUp(self):
		self.private_api = nicehash.private_api(HOST, ORGANIZATION_ID, KEY, SECRET, verbose=VERBOSE)

	def tearDown(self):
		self.private_api.close()

	#########################################

	def assert_is_number(self, value):
		if not value: return
		if "." in str(value) or "e" in str(value):
			try:
				self.assertIsInstance(value, float)
			except AssertionError:
				self.assertIsInstance(float(value), float)
		elif "\'" in str(value):
			self.assertIsInstance(int(value), int)
		else:
			try:
				self.assertIsInstance(value, int)
			except AssertionError:
				self.assertIsInstance(int(value), int)

	# Accounting

	# /main/api/v2/accounting/account2/{currency}

	@unittest.skipIf("/main/api/v2/accounting/account2/{currency}" not in TESTING_URIS, "skipping successful")
	def test_accounts_for_currency(self):
		check_test_paramters(["currency"])
		accounts_for_currency = self.private_api.get_accounts_for_currency(CURRENCY)
		# print(accounts_for_currency)
		self.assertIsInstance(accounts_for_currency, dict)
		self.assertIsInstance(accounts_for_currency["active"], bool)
		self.assertIsInstance(accounts_for_currency["currency"], str)
		self.assert_is_number(accounts_for_currency["totalBalance"])
		self.assert_is_number(accounts_for_currency["available"])
		self.assert_is_number(accounts_for_currency["pending"])
		try:
			self.assertIsInstance(accounts_for_currency["pendingDetails"], dict)
			self.assertIsInstance(accounts_for_currency["pendingDetails"]["deposit"], dict)
			self.assertIsInstance(accounts_for_currency["pendingDetails"]["withdrawal"], dict)
			self.assertIsInstance(accounts_for_currency["pendingDetails"]["exchange"], dict)
			self.assertIsInstance(accounts_for_currency["pendingDetails"]["hashpowerOrders"], dict)
			self.assertIsInstance(accounts_for_currency["pendingDetails"]["unpaidMining"], dict)
		except KeyError: pass
		try:
			self.assertIsInstance(accounts_for_currency["enabled"], bool)
		except KeyError: pass
		try:
			self.assert_is_number(accounts_for_currency["btcRate"])
		except KeyError: pass
		try:
			self.assert_is_number(accounts_for_currency["fiatRate"])
		except KeyError: pass
	# {
	# 	active : boolean - Active
	# 	currency : string - Currency - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 	totalBalance : object - Pending unpaid mining Balance
	# 	available : object - Pending unpaid mining Balance
	# 	pending : object - Pending unpaid mining Balance
	# 	pendingDetails : {
	# 		deposit : object - Pending unpaid mining Balance
	# 		withdrawal : object - Pending unpaid mining Balance
	# 		exchange : object - Pending unpaid mining Balance
	# 		hashpowerOrders : object - Pending unpaid mining Balance
	# 		unpaidMining : object - Pending unpaid mining Balance
	# 	}
	# 	enabled : boolean - Enabled
	# 	btcRate : number - Rate between currency and btc
	# 	fiatRate : number - Rate between currency and fiat
	# }

	# /main/api/v2/accounting/accounts2

	@unittest.skipIf("/main/api/v2/accounting/accounts2" not in TESTING_URIS, "skipping successful")
	def test_accounts(self):
		accounts = self.private_api.get_accounts()
		# print(accounts)
		self.assertIsInstance(accounts, dict)
		self.assertIsInstance(accounts["total"], dict)
		try:
			self.assertIsInstance(accounts["total"]["active"], bool)
		except KeyError: pass
		self.assertIsInstance(accounts["total"]["currency"], str)
		self.assert_is_number(accounts["total"]["totalBalance"])
		self.assert_is_number(accounts["total"]["available"])
		self.assert_is_number(accounts["total"]["pending"])
		try:
			self.assertIsInstance(accounts["total"]["pendingDetails"], dict)
			self.assertIsInstance(accounts["total"]["pendingDetails"]["deposit"], dict)
			self.assertIsInstance(accounts["total"]["pendingDetails"]["withdrawal"], dict)
			self.assertIsInstance(accounts["total"]["pendingDetails"]["exchange"], dict)
			self.assertIsInstance(accounts["total"]["pendingDetails"]["hashpowerOrders"], dict)
			self.assertIsInstance(accounts["total"]["pendingDetails"]["unpaidMining"], dict)
		except KeyError: pass
		try:
			self.assertIsInstance(accounts["total"]["enabled"], bool)
		except KeyError: pass
		try:
			self.assert_is_number(accounts["total"]["btcRate"])
		except KeyError: pass
		try:
			self.assert_is_number(accounts["total"]["fiatRate"])
		except KeyError: pass
		self.assertIsInstance(accounts["currencies"], list)
		def test(currency):
			self.assertIsInstance(currency, dict)
			self.assertIsInstance(currency["active"], bool)
			self.assertIsInstance(currency["currency"], str)
			self.assert_is_number(currency["totalBalance"])
			self.assert_is_number(currency["available"])
			self.assert_is_number(currency["pending"])
			try:
				self.assertIsInstance(currency["pendingDetails"], dict)
				self.assertIsInstance(currency["pendingDetails"]["deposit"], dict)
				self.assertIsInstance(currency["pendingDetails"]["withdrawal"], dict)
				self.assertIsInstance(currency["pendingDetails"]["exchange"], dict)
				self.assertIsInstance(currency["pendingDetails"]["hashpowerOrders"], dict)
				self.assertIsInstance(currency["pendingDetails"]["unpaidMining"], dict)
				self.assertIsInstance(currency["enabled"], bool)
			except KeyError: pass
			try:
				self.assert_is_number(currency["btcRate"])
			except KeyError: pass
			try:
				self.assert_is_number(currency["fiatRate"])
			except KeyError: pass
		if TEST_LISTS:
			for currency in acounts["currencies"]:
				test(currency)
		elif len(accounts["currencies"]) > 0:
		 	test(accounts["currencies"][0])
		else: raise Exception("Empty return data for testing; missing currencies")
	# {
	# 	total : {
	# 		active : boolean - Active
	# 		currency : string - Currency - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 		totalBalance : object - Pending unpaid mining Balance
	# 		available : object - Pending unpaid mining Balance
	# 		pending : object - Pending unpaid mining Balance
	# 		pendingDetails : {
	# 			deposit : object - Pending unpaid mining Balance
	# 			withdrawal : object - Pending unpaid mining Balance
	# 			exchange : object - Pending unpaid mining Balance
	# 			hashpowerOrders : object - Pending unpaid mining Balance
	# 			unpaidMining : object - Pending unpaid mining Balance
	# 		}
	# 		enabled : boolean - Enabled
	# 		btcRate : number - Rate between currency and btc
	# 		fiatRate : number - Rate between currency and fiat
	# 	}
	# 	currencies : [
	# 		{
	# 			active : boolean - Active
	# 			currency : string - Currency - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 			totalBalance : object - Pending unpaid mining Balance
	# 			available : object - Pending unpaid mining Balance
	# 			pending : object - Pending unpaid mining Balance
	# 			pendingDetails : {
	# 				deposit : object - Pending unpaid mining Balance
	# 				withdrawal : object - Pending unpaid mining Balance
	# 				exchange : object - Pending unpaid mining Balance
	# 				hashpowerOrders : object - Pending unpaid mining Balance
	# 				unpaidMining : object - Pending unpaid mining Balance
	# 			}
	# 			enabled : boolean - Enabled
	# 			btcRate : number - Rate between currency and btc
	# 			fiatRate : number - Rate between currency and fiat
	# 		}
	# 	]
	# }

	# /main/api/v2/accounting/activity/{currency}

	@unittest.skipIf("/main/api/v2/accounting/activity/{currency}" not in TESTING_URIS, "skipping successful")
	def test_account_activity(self):
		check_test_paramters(["currency"])
		account_activity = self.private_api.get_account_activity(CURRENCY)
		# print(account_activity)
		self.assertIsInstance(account_activity, list)
		def test(activity):
			self.assertIsInstance(activity, dict)
			self.assert_is_number(activity["time"])
			self.assertIsInstance(activity["status"], str)
			self.assertIsInstance(activity["amount"], dict)
			self.assertIsInstance(activity["feeAmount"], dict)
			self.assertIsInstance(activity["id"], str)
			self.assertIsInstance(activity["type"], str)
		if TEST_LISTS:
			for activity in account_activity:
				test(activity)
		elif len(account_activity) > 0:
			test(account_activity[0])
		else: raise Exception("Empty return data for testing; missing account activity")
	# [
	# 	{
	# 		time : integer - Activity time (used for sorting)
	# 		status : string - Get activity status
	# 		amount : object - Pending unpaid mining Balance
	# 		feeAmount : object - Pending unpaid mining Balance
	# 		id : string - Get activity Id
	# 		type : string - Get activity type - DEPOSIT, WITHDRAWAL, HASHPOWER, MINING, EXCHANGE, UNPAID_MINING, OTHER
	# 	}
	# ]

	# /main/api/v2/accounting/depositAddresses

	@unittest.skipIf("/main/api/v2/accounting/depositAddresses" not in TESTING_URIS, "skipping successful")
	def test_deposit_addresses(self):
		check_test_paramters(["currency"])
		deposit_addresses = self.private_api.get_deposit_addresses(CURRENCY)
		# print(deposit_addresses)
		self.assertIsInstance(deposit_addresses, dict)
		self.assertIsInstance(deposit_addresses["list"], list)
		def test(list_):
			self.assertIsInstance(list_, dict)
			self.assertIsInstance(list_["type"], dict)
			self.assertIsInstance(list_["type"]["code"], str)
			self.assertIsInstance(list_["type"]["description"], str)
			self.assertIsInstance(list_["type"]["supportedCurrencies"], list)
			def test2(currency):
				self.assertIsInstance(currency, str)
			if TEST_LISTS:
				for currency in list_["type"]["supportedCurrencies"]:
					test2(currency)
			elif len(list_["type"]["supportedCurrencies"]) > 0:
				test2(list_["type"]["supportedCurrencies"][0])
			self.assertIsInstance(list_["address"], str)
			self.assertIsInstance(list_["currency"], str)
		if TEST_LISTS:
			for list_ in deposit_addresses["list"]:
				test(list_)
		elif len(deposit_addresses["list"]) > 0:
			test(deposit_addresses["list"][0])
		else: raise Exception("Empty return data for testing; missing deposit addresses")
	# {
	# 	list : [
	# 		{
	# 			type : {
	# 				code : string - Enum code - BITGO, COINBASE, PAYEER, EXTERNAL, FEES, KRIPTOMAT, BLOCKCHAIN, LIGHTNING, INTERNAL, MULTISIG
	# 				description : string - Translated enum
	# 				supportedCurrencies : [
	# 					string - Supported currencies - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 				]
	# 			}
	# 			address : string - Address
	# 			currency : string - Currency - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 		}
	# 	]
	# }

	# /main/api/v2/accounting/deposits/{currency}

	@unittest.skipIf("/main/api/v2/accounting/deposits/{currency}" not in TESTING_URIS, "skipping successful")
	def test_deposits_for_currency(self):
		check_test_paramters(["currency"])
		deposits_for_currency = self.private_api.get_deposits_for_currency(CURRENCY)
		# print(deposits_for_currency)
		self.assertIsInstance(deposits_for_currency, dict)
		self.assertIsInstance(deposits_for_currency["list"], list)
		def test(deposit):
			self.assertIsInstance(deposit, dict)
			self.assertIsInstance(deposit["id"], str)
			self.assert_is_number(deposit["created"])
			self.assertIsInstance(deposit["currency"], dict)
			self.assertIsInstance(deposit["currency"]["enumName"], str)
			self.assertIsInstance(deposit["currency"]["description"], str)
			self.assert_is_number(deposit["amount"])
			self.assertIsInstance(deposit["metadata"], str)
			self.assertIsInstance(deposit["accountType"], dict)
			self.assertIsInstance(deposit["accountType"]["enumName"], str)
			self.assertIsInstance(deposit["accountType"]["description"], str)
			self.assert_is_number(deposit["feeAmount"])
			self.assertIsInstance(deposit["feeMetadata"], str)
		if TEST_LISTS:
			for deposit in deposits_for_currency["list"]:
				test(deposit)
		elif len(deposits_for_currency["list"]) > 0:
			test(deposits_for_currency["list"][0])
		else: raise Exception("Empty return data for testing; missing deposits for currency")
		try:
			self.assertIsInstance(deposits_for_currency["pagination"], dict)
			self.assert_is_number(deposits_for_currency["pagination"]["size"])
			self.assert_is_number(deposits_for_currency["pagination"]["page"])
			self.assert_is_number(deposits_for_currency["pagination"]["totalPageCount"])
		except KeyError: pass
	# {
	# 	list : [
	# 		{
	# 			id : string - Id of the transaction
	# 			created : integer - Transaction creation timestamp in milliseconds since 1.1.1970
	# 			currency : {
	# 				enumName : string - Name - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 				description : string - Translated description
	# 			}
	# 			amount : number - Transaction amount
	# 			metadata : string - Transation metadata
	# 			accountType : {
	# 				enumName : string - Name - USER, USER_EXCHANGE_PENDING, USER_WITHDRAWAL_PENDING, USER_DEBT, EXCHANGE_FEE, HASHPOWER_ORDERS, HASHPOWER_PAYOUTS, HASHPOWER_ORDER_FEE, HASHPOWER_PAYOUT_FEE, WALLET_BITGO_BLOCKCHAIN, WALLET_BITGO_DEPOSIT_PENDING, WALLET_BITGO_DEPOSIT_CONFIRMED, WALLET_BITGO_DEPOSITS_FEES, WALLET_BITGO_DEPOSIT_CONFISCATED, WALLET_BITGO_DEPOSIT_UNASSIGNED, WALLET_BITGO_WITHDRAWAL_PENDING, WALLET_BITGO_WITHDRAWAL_CONFIRMED, WALLET_BITGO_WITHDRAWALS_FEES, WALLET_COINBASE_BLOCKCHAIN, WALLET_COINBASE_WITHDRAWAL_PENDING, WALLET_COINBASE_WITHDRAWALS_FEES, WALLET_COINBASE_DEPOSIT_PENDING, WALLET_COINBASE_DEPOSIT_CONFIRMED, WALLET_COINBASE_DEPOSIT_UNASSIGNED, WALLET_PAYEER_WITHDRAWAL_PENDING, WALLET_PAYEER_WITHDRAWALS_FEES, TESTING, WALLET_BITGO_WITHDRAWAL_UNASSIGNED, WALLET_KRIPTOMAT_DEPOSIT_UNASSIGNED, WALLET_KRIPTOMAT_DEPOSIT_FEES, WALLET_KRIPTOMAT_WITHDRAWAL_PENDING, WALLET_KRIPTOMAT_WITHDRAWAL_FEES, WALLET_BLOCKCHAIN_DEPOSIT_PENDING, WALLET_BLOCKCHAIN_DEPOSITS_FEES, WALLET_BLOCKCHAIN_DEPOSIT_UNASSIGNED, WALLET_BLOCKCHAIN_WITHDRAWAL_PENDING, WALLET_BLOCKCHAIN_WITHDRAWALS_FEES, WALLET_LIGHTNING_DEPOSIT_UNASSIGNED, WALLET_LIGHTNING_WITHDRAWAL_PENDING, WALLET_LIGHTNING_WITHDRAWALS_FEES, WALLET_LIGHTNING_DEPOSITS_FEES, WALLET_MULTISIG_DEPOSIT_UNASSIGNED, WALLET_MULTISIG_DEPOSITS_FEES, WALLET_MULTISIG_WITHDRAWALS_FEES, TOKEN_WITHDRAWAL_FEE_PENDING, WALLET_MULTISIG_DEPOSIT_FEES, CHARITY, HASHPOWER_ORDERS_PENDING, USER_FEE, USER_MNG_FEE, USER_EX_FEE
	# 				description : string - Translated description
	# 			}
	# 			feeAmount : number - Fee amount
	# 			feeMetadata : string - Fee metadata
	# 		}
	# 	]
	# 	pagination : {
	# 		size : integer - Page size
	# 		page : integer - Page number (first page is 0)
	# 		totalPageCount : integer - Total page count
	# 	}
	# }

	# /main/api/v2/accounting/deposits2/{currency}/{id}

	@unittest.skipIf("/main/api/v2/accounting/deposits2/{currency}/{id}" not in TESTING_URIS, "skipping successful")
	def test_deposits_for_currency_by_id(self):
		check_test_paramters(["currency", "transaction_id"])
		deposits_for_currency_by_id = self.private_api.get_deposits_for_currency_by_id(CURRENCY, TRANSACTION_ID)
		# print(deposits_for_currency_by_id)
		self.assertIsInstance(deposits_for_currency_by_id, dict)
		self.assertIsInstance(deposits_for_currency_by_id["id"], str)
		self.assertIsInstance(deposits_for_currency_by_id["amount"], str)
		self.assertIsInstance(deposits_for_currency_by_id["amountReceived"], str)
		self.assertIsInstance(deposits_for_currency_by_id["feeAmount"], str)
		self.assertIsInstance(deposits_for_currency_by_id["address"], str)
		self.assertIsInstance(deposits_for_currency_by_id["txid"], str)
		self.assertIsInstance(deposits_for_currency_by_id["status"], str)
		self.assert_is_number(deposits_for_currency_by_id["minConfirmations"])
		self.assert_is_number(deposits_for_currency_by_id["confirmations"])
		self.assert_is_number(deposits_for_currency_by_id["time"])
		self.assertIsInstance(deposits_for_currency_by_id["activityCurrency"], str)
		self.assertIsInstance(deposits_for_currency_by_id["type"], str)
	# {
	# 	id : string - Activity id
	# 	amount : string - Amount
	# 	amountReceived : string - Amount received
	# 	feeAmount : string - Fee amount
	# 	address : string - Address
	# 	txid : string - Transaction id
	# 	status : string - Status
	# 	minConfirmations : integer - Minimal confirmation required
	# 	confirmations : integer - Actual confirmation received
	# 	time : integer - Timestamp in milliseconds since 1.1.1970
	# 	activityCurrency : string
	# 	type : string - Activity type - DEPOSIT, WITHDRAWAL, HASHPOWER, MINING, EXCHANGE, UNPAID_MINING, OTHER
	# }

	# /main/api/v2/accounting/exchange/{id}/trades

	@unittest.skipIf("/main/api/v2/accounting/exchange/{id}/trades" not in TESTING_URIS, "skipping successful")
	def test_order_transactions_by_id(self):
		check_test_paramters(["market_symbol", "transaction_id"])
		order_transactions_by_id = self.private_api.get_order_transactions_by_id(TRANSACTION_ID, MARKET_SYMBOL)
		# print(order_transactions_by_id)
		self.assertIsInstance(order_transactions_by_id, dict)
		self.assertIsInstance(order_transactions_by_id["trades"], list)
		def test(trade):
			self.assertIsInstance(trade, dict)
			self.assertIsInstance(trade["sellQty"], str)
			self.assertIsInstance(trade["buyQty"], str)
			self.assert_is_number(trade["time"])
			self.assertIsInstance(trade["fee"], str)
		if TEST_LISTS:
			for trade in order_transactions_by_id["trades"]:
				test(trade)
		elif len(order_transactions_by_id["trades"]) > 0:
			test(order_transactions_by_id["trades"][0])
		else: raise Exception("Empty return data for testing; missing trades")
	# {
	# 	trades : [
	# 		{
	# 			sellQty : string - Sell quantity
	# 			buyQty : string - Buy quantity
	# 			time : integer - Trade timestamp in milliseconds since 1.1.1970
	# 			fee : string - Fee for trade
	# 		}
	# 	]
	# }

	# /main/api/v2/accounting/hashpower/{id}/transactions

	@unittest.skipIf("/main/api/v2/accounting/hashpower/{id}/transactions" not in TESTING_URIS, "skipping successful")
	def test_hashpower_order_transactions_by_id(self):
		check_test_paramters(["transaction_id"])
		hashpower_order_transactions_by_id = self.private_api.get_hashpower_order_transactions_by_id(TRANSACTION_ID)
		# print(hashpower_order_transactions_by_id)
		self.assertIsInstance(hashpower_order_transactions_by_id, dict)
		self.assertIsInstance(hashpower_order_transactions_by_id["transactions"], list)
		def test(transaction):
			self.assertIsInstance(transaction, dict)
			self.assert_is_number(transaction["created"])
			self.assertIsInstance(transaction["desc"], str)
			self.assertIsInstance(transaction["amount"], str)
		if TEST_LISTS:
			for transaction in hashpower_order_transactions_by_id["transactions"]:
				test(transaction)
		elif len(hashpower_order_transactions_by_id["transactions"]) > 0:
			test(hashpower_order_transactions_by_id["transactions"][0])
		else: raise Exception("Empty return data for testing; missing transactions")
	# {
	# 	transactions : [
	# 		{
	# 			created : integer - Creation timestamp in milliseconds since 1.1.1970
	# 			desc : string - Description for hashpower
	# 			amount : string - Amount
	# 		}
	# 	]
	# }

	# /main/api/v2/accounting/hashpowerEarnings/{currency}

	@unittest.skipIf("/main/api/v2/accounting/hashpowerEarnings/{currency}" not in TESTING_URIS, "skipping successful")
	def test_hashpower_earnings_for_currency(self):
		check_test_paramters(["currency"])
		hashpower_earnings_for_currency = self.private_api.get_hashpower_earnings_for_currency(CURRENCY)
		# print(hashpower_earnings_for_currency)
		self.assertIsInstance(hashpower_earnings_for_currency, dict)
		self.assertIsInstance(hashpower_earnings_for_currency["list"], list)
		def test(transaction):
			self.assertIsInstance(transaction, dict)
			self.assertIsInstance(transaction["id"], str)
			self.assert_is_number(transaction["created"])
			self.assertIsInstance(transaction["currency"], dict)
			self.assertIsInstance(transaction["currency"]["enumName"], str)
			self.assertIsInstance(transaction["currency"]["description"], str)
			self.assert_is_number(transaction["amount"])
			self.assertIsInstance(transaction["metadata"], str)
			self.assertIsInstance(transaction["accountType"], dict)
			self.assertIsInstance(transaction["accountType"]["enumName"], str)
			self.assertIsInstance(transaction["accountType"]["description"], str)
			self.assert_is_number(transaction["feeAmount"])
			self.assertIsInstance(transaction["feeMetadata"], str)
		if TEST_LISTS:
			for transaction in hashpower_earnings_for_currency["list"]:
				test(transaction)
		elif len(hashpower_earnings_for_currency["list"]) > 0:
			test(hashpower_earnings_for_currency["list"][0])
		else: raise Exception("Empty return data for testing; missing hashpower earnings for currencies")
		try:
			self.assertIsInstance(hashpower_earnings_for_currency["pagination"], dict)
			self.assert_is_number(hashpower_earnings_for_currency["pagination"]["size"])
			self.assert_is_number(hashpower_earnings_for_currency["pagination"]["page"])
			self.assert_is_number(hashpower_earnings_for_currency["pagination"]["totalPageCount"])
		except KeyError: pass
	# {
	# 	list : [
	# 		{
	# 			id : string - Id of the transaction
	# 			created : integer - Transaction creation timestamp in milliseconds since 1.1.1970
	# 			currency : {
	# 				enumName : string - Name - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 				description : string - Translated description
	# 			}
	# 			amount : number - Transaction amount
	# 			metadata : string - Transation metadata
	# 			accountType : {
	# 				enumName : string - Name - USER, USER_EXCHANGE_PENDING, USER_WITHDRAWAL_PENDING, USER_DEBT, EXCHANGE_FEE, HASHPOWER_ORDERS, HASHPOWER_PAYOUTS, HASHPOWER_ORDER_FEE, HASHPOWER_PAYOUT_FEE, WALLET_BITGO_BLOCKCHAIN, WALLET_BITGO_DEPOSIT_PENDING, WALLET_BITGO_DEPOSIT_CONFIRMED, WALLET_BITGO_DEPOSITS_FEES, WALLET_BITGO_DEPOSIT_CONFISCATED, WALLET_BITGO_DEPOSIT_UNASSIGNED, WALLET_BITGO_WITHDRAWAL_PENDING, WALLET_BITGO_WITHDRAWAL_CONFIRMED, WALLET_BITGO_WITHDRAWALS_FEES, WALLET_COINBASE_BLOCKCHAIN, WALLET_COINBASE_WITHDRAWAL_PENDING, WALLET_COINBASE_WITHDRAWALS_FEES, WALLET_COINBASE_DEPOSIT_PENDING, WALLET_COINBASE_DEPOSIT_CONFIRMED, WALLET_COINBASE_DEPOSIT_UNASSIGNED, WALLET_PAYEER_WITHDRAWAL_PENDING, WALLET_PAYEER_WITHDRAWALS_FEES, TESTING, WALLET_BITGO_WITHDRAWAL_UNASSIGNED, WALLET_KRIPTOMAT_DEPOSIT_UNASSIGNED, WALLET_KRIPTOMAT_DEPOSIT_FEES, WALLET_KRIPTOMAT_WITHDRAWAL_PENDING, WALLET_KRIPTOMAT_WITHDRAWAL_FEES, WALLET_BLOCKCHAIN_DEPOSIT_PENDING, WALLET_BLOCKCHAIN_DEPOSITS_FEES, WALLET_BLOCKCHAIN_DEPOSIT_UNASSIGNED, WALLET_BLOCKCHAIN_WITHDRAWAL_PENDING, WALLET_BLOCKCHAIN_WITHDRAWALS_FEES, WALLET_LIGHTNING_DEPOSIT_UNASSIGNED, WALLET_LIGHTNING_WITHDRAWAL_PENDING, WALLET_LIGHTNING_WITHDRAWALS_FEES, WALLET_LIGHTNING_DEPOSITS_FEES, WALLET_MULTISIG_DEPOSIT_UNASSIGNED, WALLET_MULTISIG_DEPOSITS_FEES, WALLET_MULTISIG_WITHDRAWALS_FEES, TOKEN_WITHDRAWAL_FEE_PENDING, WALLET_MULTISIG_DEPOSIT_FEES, CHARITY, HASHPOWER_ORDERS_PENDING, USER_FEE, USER_MNG_FEE, USER_EX_FEE
	# 				description : string - Translated description
	# 			}
	# 			feeAmount : number - Fee amount
	# 			feeMetadata : string - Fee metadata
	# 		}
	# 	]
	# 	pagination : {
	# 		size : integer - Page size
	# 		page : integer - Page number (first page is 0)
	# 		totalPageCount : integer - Total page count
	# 	}
	# }

	# /main/api/v2/accounting/transaction/{currency}/{transactionId}

	@unittest.skipIf("/main/api/v2/accounting/transaction/{currency}/{transactionId}" not in TESTING_URIS, "skipping successful")
	def test_transaction_for_currency_by_id(self):
		check_test_paramters(["currency", "transaction_id"])
		transaction_for_currency_by_id = self.private_api.get_transaction_for_currency_by_id(CURRENCY, TRANSACTION_ID)
		# print(transaction_for_currency_by_id)
		self.assertIsInstance(transaction_for_currency_by_id, dict)
		self.assertIsInstance(transaction_for_currency_by_id["id"], str)
		self.assert_is_number(transaction_for_currency_by_id["created"])
		self.assertIsInstance(transaction_for_currency_by_id["currency"], dict)
		self.assertIsInstance(transaction_for_currency_by_id["currency"]["enumName"], str)
		self.assertIsInstance(transaction_for_currency_by_id["currency"]["description"], str)
		self.assert_is_number(transaction_for_currency_by_id["amount"])
		self.assertIsInstance(transaction_for_currency_by_id["metadata"],str)
		self.assertIsInstance(transaction_for_currency_by_id["type"], dict)
		self.assertIsInstance(transaction_for_currency_by_id["type"]["enumName"], str)
		self.assertIsInstance(transaction_for_currency_by_id["type"]["description"], str)
		self.assertIsInstance(transaction_for_currency_by_id["fromOwner"], str)
		self.assertIsInstance(transaction_for_currency_by_id["fromAccountType"], dict)
		self.assertIsInstance(transaction_for_currency_by_id["fromAccountType"]["enumName"], str)
		self.assertIsInstance(transaction_for_currency_by_id["fromAccountType"]["description"], str)
		self.assertIsInstance(transaction_for_currency_by_id["toOwner"], str)
		self.assertIsInstance(transaction_for_currency_by_id["toAccountType"], str)
	# {
	# 	id : string - Id of the transaction
	# 	created : integer - Transaction creation timestamp in milliseconds since 1.1.1970
	# 	currency : {
	# 		enumName : string - Name - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 		description : string - Translated description
	# 	}
	# 	amount : number - Transaction amount
	# 	metadata : string - Transation metadata
	# 	type : {
	# 		enumName : string - Name - DEPOSIT, WITHDRAWAL, MOVE
	# 		description : string - Translated description
	# 	}
	# 	fromOwner : string - Source of the transaction
	# 	fromAccountType : {
	# 		enumName : string - Name - USER, USER_EXCHANGE_PENDING, USER_WITHDRAWAL_PENDING, USER_DEBT, EXCHANGE_FEE, HASHPOWER_ORDERS, HASHPOWER_PAYOUTS, HASHPOWER_ORDER_FEE, HASHPOWER_PAYOUT_FEE, WALLET_BITGO_BLOCKCHAIN, WALLET_BITGO_DEPOSIT_PENDING, WALLET_BITGO_DEPOSIT_CONFIRMED, WALLET_BITGO_DEPOSITS_FEES, WALLET_BITGO_DEPOSIT_CONFISCATED, WALLET_BITGO_DEPOSIT_UNASSIGNED, WALLET_BITGO_WITHDRAWAL_PENDING, WALLET_BITGO_WITHDRAWAL_CONFIRMED, WALLET_BITGO_WITHDRAWALS_FEES, WALLET_COINBASE_BLOCKCHAIN, WALLET_COINBASE_WITHDRAWAL_PENDING, WALLET_COINBASE_WITHDRAWALS_FEES, WALLET_COINBASE_DEPOSIT_PENDING, WALLET_COINBASE_DEPOSIT_CONFIRMED, WALLET_COINBASE_DEPOSIT_UNASSIGNED, WALLET_PAYEER_WITHDRAWAL_PENDING, WALLET_PAYEER_WITHDRAWALS_FEES, TESTING, WALLET_BITGO_WITHDRAWAL_UNASSIGNED, WALLET_KRIPTOMAT_DEPOSIT_UNASSIGNED, WALLET_KRIPTOMAT_DEPOSIT_FEES, WALLET_KRIPTOMAT_WITHDRAWAL_PENDING, WALLET_KRIPTOMAT_WITHDRAWAL_FEES, WALLET_BLOCKCHAIN_DEPOSIT_PENDING, WALLET_BLOCKCHAIN_DEPOSITS_FEES, WALLET_BLOCKCHAIN_DEPOSIT_UNASSIGNED, WALLET_BLOCKCHAIN_WITHDRAWAL_PENDING, WALLET_BLOCKCHAIN_WITHDRAWALS_FEES, WALLET_LIGHTNING_DEPOSIT_UNASSIGNED, WALLET_LIGHTNING_WITHDRAWAL_PENDING, WALLET_LIGHTNING_WITHDRAWALS_FEES, WALLET_LIGHTNING_DEPOSITS_FEES, WALLET_MULTISIG_DEPOSIT_UNASSIGNED, WALLET_MULTISIG_DEPOSITS_FEES, WALLET_MULTISIG_WITHDRAWALS_FEES, TOKEN_WITHDRAWAL_FEE_PENDING, WALLET_MULTISIG_DEPOSIT_FEES, CHARITY, HASHPOWER_ORDERS_PENDING, USER_FEE, USER_MNG_FEE, USER_EX_FEE
	# 		description : string - Translated description
	# 	}
	# 	toOwner : string - Destination of the transaction
	# 	toAccountType : string - Destination account type - USER, USER_EXCHANGE_PENDING, USER_WITHDRAWAL_PENDING, USER_DEBT, EXCHANGE_FEE, HASHPOWER_ORDERS, HASHPOWER_PAYOUTS, HASHPOWER_ORDER_FEE, HASHPOWER_PAYOUT_FEE, WALLET_BITGO_BLOCKCHAIN, WALLET_BITGO_DEPOSIT_PENDING, WALLET_BITGO_DEPOSIT_CONFIRMED, WALLET_BITGO_DEPOSITS_FEES, WALLET_BITGO_DEPOSIT_CONFISCATED, WALLET_BITGO_DEPOSIT_UNASSIGNED, WALLET_BITGO_WITHDRAWAL_PENDING, WALLET_BITGO_WITHDRAWAL_CONFIRMED, WALLET_BITGO_WITHDRAWALS_FEES, WALLET_COINBASE_BLOCKCHAIN, WALLET_COINBASE_WITHDRAWAL_PENDING, WALLET_COINBASE_WITHDRAWALS_FEES, WALLET_COINBASE_DEPOSIT_PENDING, WALLET_COINBASE_DEPOSIT_CONFIRMED, WALLET_COINBASE_DEPOSIT_UNASSIGNED, WALLET_PAYEER_WITHDRAWAL_PENDING, WALLET_PAYEER_WITHDRAWALS_FEES, TESTING, WALLET_BITGO_WITHDRAWAL_UNASSIGNED, WALLET_KRIPTOMAT_DEPOSIT_UNASSIGNED, WALLET_KRIPTOMAT_DEPOSIT_FEES, WALLET_KRIPTOMAT_WITHDRAWAL_PENDING, WALLET_KRIPTOMAT_WITHDRAWAL_FEES, WALLET_BLOCKCHAIN_DEPOSIT_PENDING, WALLET_BLOCKCHAIN_DEPOSITS_FEES, WALLET_BLOCKCHAIN_DEPOSIT_UNASSIGNED, WALLET_BLOCKCHAIN_WITHDRAWAL_PENDING, WALLET_BLOCKCHAIN_WITHDRAWALS_FEES, WALLET_LIGHTNING_DEPOSIT_UNASSIGNED, WALLET_LIGHTNING_WITHDRAWAL_PENDING, WALLET_LIGHTNING_WITHDRAWALS_FEES, WALLET_LIGHTNING_DEPOSITS_FEES, WALLET_MULTISIG_DEPOSIT_UNASSIGNED, WALLET_MULTISIG_DEPOSITS_FEES, WALLET_MULTISIG_WITHDRAWALS_FEES, TOKEN_WITHDRAWAL_FEE_PENDING, WALLET_MULTISIG_DEPOSIT_FEES, CHARITY, HASHPOWER_ORDERS_PENDING, USER_FEE, USER_MNG_FEE, USER_EX_FEE
	# }

	# /main/api/v2/accounting/transactions/{currency}

	@unittest.skipIf("/main/api/v2/accounting/transactions/{currency}" not in TESTING_URIS, "skipping successful")
	def test_transactions_for_currency(self):
		check_test_paramters(["currency"])
		transactions_for_currency = self.private_api.get_transactions_for_currency(CURRENCY)
		# print(transactions_for_currency)
		self.assertIsInstance(transactions_for_currency, dict)
		self.assertIsInstance(transactions_for_currency["list"], list)
		def test(transaction):
			self.assertIsInstance(transaction, dict)
			self.assertIsInstance(transaction["id"], str)
			self.assert_is_number(transaction["created"])
			self.assertIsInstance(transaction["currency"], dict)
			self.assertIsInstance(transaction["currency"]["enumName"], str)
			self.assertIsInstance(transaction["currency"]["description"], str)
			self.assert_is_number(transaction["amount"])
			self.assertIsInstance(transaction["metadata"], str)
			self.assertIsInstance(transaction["accountType"], dict)
			self.assertIsInstance(transaction["accountType"]["enumName"], str)
			self.assertIsInstance(transaction["accountType"]["description"], str)
			self.assert_is_number(transaction["feeAmount"])
			self.assertIsInstance(transaction["feeMetadata"], str)
		if TEST_LISTS:
			for transaction in transactions_for_currency["list"]:
				test(transaction)
		elif len(transactions_for_currency["list"]) > 0:
			test(transactions_for_currency["list"][0])
		else: raise Exception("Empty return data for testing; missing transactions for currencies")
		try:
			self.assertIsInstance(transactions_for_currency["pagination"], dict)
			self.assert_is_number(transactions_for_currency["pagination"]["size"])
			self.assert_is_number(transactions_for_currency["pagination"]["page"])
			self.assert_is_number(transactions_for_currency["pagination"]["totalPageCount"])
		except KeyError: pass
	# {
	# 	list : [
	# 		{
	# 			id : string - Id of the transaction
	# 			created : integer - Transaction creation timestamp in milliseconds since 1.1.1970
	# 			currency : {
	# 				enumName : string - Name - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 				description : string - Translated description
	# 			}
	# 			amount : number - Transaction amount
	# 			metadata : string - Transation metadata
	# 			accountType : {
	# 				enumName : string - Name - USER, USER_EXCHANGE_PENDING, USER_WITHDRAWAL_PENDING, USER_DEBT, EXCHANGE_FEE, HASHPOWER_ORDERS, HASHPOWER_PAYOUTS, HASHPOWER_ORDER_FEE, HASHPOWER_PAYOUT_FEE, WALLET_BITGO_BLOCKCHAIN, WALLET_BITGO_DEPOSIT_PENDING, WALLET_BITGO_DEPOSIT_CONFIRMED, WALLET_BITGO_DEPOSITS_FEES, WALLET_BITGO_DEPOSIT_CONFISCATED, WALLET_BITGO_DEPOSIT_UNASSIGNED, WALLET_BITGO_WITHDRAWAL_PENDING, WALLET_BITGO_WITHDRAWAL_CONFIRMED, WALLET_BITGO_WITHDRAWALS_FEES, WALLET_COINBASE_BLOCKCHAIN, WALLET_COINBASE_WITHDRAWAL_PENDING, WALLET_COINBASE_WITHDRAWALS_FEES, WALLET_COINBASE_DEPOSIT_PENDING, WALLET_COINBASE_DEPOSIT_CONFIRMED, WALLET_COINBASE_DEPOSIT_UNASSIGNED, WALLET_PAYEER_WITHDRAWAL_PENDING, WALLET_PAYEER_WITHDRAWALS_FEES, TESTING, WALLET_BITGO_WITHDRAWAL_UNASSIGNED, WALLET_KRIPTOMAT_DEPOSIT_UNASSIGNED, WALLET_KRIPTOMAT_DEPOSIT_FEES, WALLET_KRIPTOMAT_WITHDRAWAL_PENDING, WALLET_KRIPTOMAT_WITHDRAWAL_FEES, WALLET_BLOCKCHAIN_DEPOSIT_PENDING, WALLET_BLOCKCHAIN_DEPOSITS_FEES, WALLET_BLOCKCHAIN_DEPOSIT_UNASSIGNED, WALLET_BLOCKCHAIN_WITHDRAWAL_PENDING, WALLET_BLOCKCHAIN_WITHDRAWALS_FEES, WALLET_LIGHTNING_DEPOSIT_UNASSIGNED, WALLET_LIGHTNING_WITHDRAWAL_PENDING, WALLET_LIGHTNING_WITHDRAWALS_FEES, WALLET_LIGHTNING_DEPOSITS_FEES, WALLET_MULTISIG_DEPOSIT_UNASSIGNED, WALLET_MULTISIG_DEPOSITS_FEES, WALLET_MULTISIG_WITHDRAWALS_FEES, TOKEN_WITHDRAWAL_FEE_PENDING, WALLET_MULTISIG_DEPOSIT_FEES, CHARITY, HASHPOWER_ORDERS_PENDING, USER_FEE, USER_MNG_FEE, USER_EX_FEE
	# 				description : string - Translated description
	# 			}
	# 			feeAmount : number - Fee amount
	# 			feeMetadata : string - Fee metadata
	# 		}
	# 	]
	# 	pagination : {
	# 		size : integer - Page size
	# 		page : integer - Page number (first page is 0)
	# 		totalPageCount : integer - Total page count
	# 	}
	# }

	# /main/api/v2/accounting/withdrawal

	@unittest.skipIf("/main/api/v2/accounting/withdrawal" not in TESTING_URIS, "skipping successful")
	def test_withdraw_request(self):
		check_test_paramters(["currency", "withdrawal_amount", "whitelisted_withdrawal_address_id"])
		withdrawal = self.private_api.withdraw_request(CURRENCY, WITHDRAWAL_AMOUNT, WHITELISTED_WITHDRAWAL_ADDRESS_ID)
		# print(withdrawal)
		self.assertIsInstance(withdrawal, dict)
		self.assertIsInstance(withdrawal["id"], str)
	# {
	# 	id : string - Withdrawal request id
	# }

	# /main/api/v2/accounting/withdrawal/{currency}/{id}

	@unittest.skipIf("/main/api/v2/accounting/withdrawal/{currency}/{id}" not in TESTING_URIS, "skipping successful")
	def test_delete_withdrawal(self):
		check_test_paramters(["currency", "withdrawal_id"])
		delete_withdrawal = self.private_api.delete_withdrawal(CURRENCY, WITHDRAWAL_ID)
		# print(delete_withdrawal)
		self.assertIsInstance(delete_withdrawal, dict)
		self.assertIsInstance(delete_withdrawal["success"], bool)
		self.assertIsInstance(delete_withdrawal["successType"], str)
		self.assertIsInstance(delete_withdrawal["message"], str)
	# {
	# 	success : boolean
	# 	successType : string - SUCCESSFUL, PARTIAL_SUCCESS, NOT_SUCCESSFUL
	# 	message : string
	# }

	# /main/api/v2/accounting/withdrawal2/{currency}/{id}

	@unittest.skipIf("/main/api/v2/accounting/withdrawal2/{currency}/{id}" not in TESTING_URIS, "skipping successful")
	def test_withdrawal_for_currency_by_id(self):
		check_test_paramters(["currency", "withdrawal_id"])
		withdrawal_for_currency_by_id = self.private_api.get_withdrawal_for_currency_by_id(CURRENCY, WITHDRAWAL_ID)
		# print(withdrawal_for_currency_by_id)
		self.assertIsInstance(withdrawal_for_currency_by_id, dict)
		self.assertIsInstance(withdrawal_for_currency_by_id["id"], str)
		self.assertIsInstance(withdrawal_for_currency_by_id["amount"], str)
		self.assertIsInstance(withdrawal_for_currency_by_id["amountReceived"], str)
		self.assertIsInstance(withdrawal_for_currency_by_id["feeAmount"], str)
		self.assertIsInstance(withdrawal_for_currency_by_id["address"], str)
		self.assertIsInstance(withdrawal_for_currency_by_id["status"], str)
		self.assertIsInstance(withdrawal_for_currency_by_id["wallet"], str)
		self.assert_is_number(withdrawal_for_currency_by_id["time"])
		self.assertIsInstance(withdrawal_for_currency_by_id["activityCurrency"], str)
		self.assertIsInstance(withdrawal_for_currency_by_id["type"], str)
	# {
	# 	id : string - Withdrawal id
	# 	amount : string - Amount
	# 	amountReceived : string - Amount received
	# 	feeAmount : string - Fee amount
	# 	address : string - Withdrawal address
	# 	status : string - Withdrawal status
	# 	wallet : string - Wallet type - BITGO, COINBASE, PAYEER, EXTERNAL, FEES, KRIPTOMAT, BLOCKCHAIN, LIGHTNING, INTERNAL, MULTISIG
	# 	time : integer - Time in milliseconds since 1.1.1970
	# 	activityCurrency : string
	# 	type : string - Activity type - DEPOSIT, WITHDRAWAL, HASHPOWER, MINING, EXCHANGE, UNPAID_MINING, OTHER
	# }

	# /main/api/v2/accounting/withdrawalAddress/{id}

	@unittest.skipIf("/main/api/v2/accounting/withdrawalAddress/{id}" not in TESTING_URIS, "skipping successful")
	def test_withdrawal_address_by_id(self):
		check_test_paramters(["withdrawal_id"])
		withdrawal_address_by_id = self.private_api.get_withdrawal_address_by_id(WITHDRAWAL_ID)
		# print(withdrawal_address_by_id)
		self.assertIsInstance(withdrawal_address_by_id, dict)
		self.assertIsInstance(withdrawal["id"], str)
		self.assertIsInstance(withdrawal["type"], dict)
		self.assertIsInstance(withdrawal["type"]["code"], str)
		self.assertIsInstance(withdrawal["type"]["description"], str)
		self.assertIsInstance(withdrawal["type"]["supportedCurrencies"], list)
		def test(withdrawal):
			self.assertIsInstance(withdrawal, str)
		if TEST_LISTS:
			for withdrawal in withdrawal["type"]["supportedCurrencies"]:
				test(withdrawal)
		elif len(withdrawal["type"]["supportedCurrencies"]) > 0:
			test(withdrawal["type"]["supportedCurrencies"][0])
		else: raise Exception("Empty return data for testing; missing withdrawal supported currencies")
		self.assertIsInstance(withdrawal["name"], str)
		self.assertIsInstance(withdrawal["address"], str)
		self.assertIsInstance(withdrawal["createdTs"], str)
		self.assertIsInstance(withdrawal["currency"], dict)
		self.assertIsInstance(withdrawal["status"], dict)
		self.assertIsInstance(withdrawal["status"]["code"], str)
		self.assertIsInstance(withdrawal["status"]["description"], str)
		self.assertIsInstance(withdrawal["emailConfirmationType"]["description"], str)
		self.assertIsInstance(withdrawal["meta"], str)
		self.assertIsInstance(withdrawal["updatedTs"], str)
		self.assertIsInstance(withdrawal["inMoratorium"], bool)
	# {
	# 	id : string
	# 	type : {
	# 		code : string - Enum code - BITGO, COINBASE, PAYEER, EXTERNAL, FEES, KRIPTOMAT, BLOCKCHAIN, LIGHTNING, INTERNAL, MULTISIG
	# 		description : string - Translated enum
	# 		supportedCurrencies : [
	# 			string - Supported currencies - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 		]
	# 	}
	# 	name : string
	# 	address : string
	# 	createdTs : string - Created timestamp
	# 	currency : string - Currency - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 	status : {
	# 		code : string - Enum code - PENDING_EMAIL_CONFIRMATION, ACTIVE, INACTIVE, INVALID, PENDING_DEPOSIT_CONFIRMATION
	# 		description : string - Translated enum
	# 	}
	# 	emailConfirmationType : string - E-mail confirmation type (type used on /api/v2/emailConfirmation/verify), optional, set only if status requires e-mail confirmation
	# 	meta : string - Address metadata
	# 	updatedTs : string
	# 	inMoratorium : boolean
	# }

	# /main/api/v2/accounting/withdrawalAddresses

	@unittest.skipIf("/main/api/v2/accounting/withdrawalAddresses" not in TESTING_URIS, "skipping successful")
	def test_withdrawal_addresses(self):
		check_test_paramters(["currency"])
		withdrawal_addresses = self.private_api.get_withdrawal_addresses(CURRENCY)
		# print(withdrawal_addresses)  
		self.assertIsInstance(withdrawal_addresses, dict)
		self.assertIsInstance(withdrawal_addresses["list"], list)
		def test(withdrawal):
			self.assertIsInstance(withdrawal, dict)
			self.assertIsInstance(withdrawal["id"], str)
			self.assertIsInstance(withdrawal["type"], dict)
			self.assertIsInstance(withdrawal["type"]["code"], str)
			self.assertIsInstance(withdrawal["type"]["description"], str)
			self.assertIsInstance(withdrawal["type"]["supportedCurrencies"], list)
			def test2(currency):
				self.assertIsInstance(currency, str)
			if TEST_LISTS:
				for currency in withdrawal["type"]["supportedCurrencies"]:
					test2(currency)
			elif len(withdrawal["type"]["supportedCurrencies"]) > 0:
				test2(withdrawal["type"]["supportedCurrencies"][0])
			self.assertIsInstance(withdrawal["name"], str)
			self.assertIsInstance(withdrawal["address"], str)
			self.assertIsInstance(withdrawal["createdTs"], str)
			self.assertIsInstance(withdrawal["currency"], dict)
			self.assertIsInstance(withdrawal["status"], dict)
			self.assertIsInstance(withdrawal["status"]["code"], str)
			self.assertIsInstance(withdrawal["status"]["description"], str)
			self.assertIsInstance(withdrawal["emailConfirmationType"]["description"], str)
			self.assertIsInstance(withdrawal["meta"], str)
			self.assertIsInstance(withdrawal["updatedTs"], str)
			self.assertIsInstance(withdrawal["inMoratorium"], bool)
		if TEST_LISTS:
			for withdrawal in withdrawal_addresses["list"]:
				test(withdrawal)
		elif len(withdrawal_addresses["list"]) > 0:
			test(withdrawal_addresses["list"][0])
		else: raise Exception("Empty return data for testing; missing withdrawal addresses")
		try:
			self.assertIsInstance(withdrawal_addresses["pagination"], dict)
			self.assert_is_number(withdrawal_addresses["pagination"]["size"])
			self.assert_is_number(withdrawal_addresses["pagination"]["page"])
			self.assert_is_number(withdrawal_addresses["pagination"]["totalPageCount"])
		except KeyError: pass
	# {
	# 	list : [
	# 		{
	# 			id : string
	# 			type : {
	# 				code : string - Enum code - BITGO, COINBASE, PAYEER, EXTERNAL, FEES, KRIPTOMAT, BLOCKCHAIN, LIGHTNING, INTERNAL, MULTISIG
	# 				description : string - Translated enum
	# 				supportedCurrencies : [
	# 					string - Supported currencies - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 				]
	# 			}
	# 			name : string
	# 			address : string
	# 			createdTs : string - Created timestamp
	# 			currency : string - Currency - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 			status : {
	# 				code : string - Enum code - PENDING_EMAIL_CONFIRMATION, ACTIVE, INACTIVE, INVALID, PENDING_DEPOSIT_CONFIRMATION
	# 				description : string - Translated enum
	# 			}
	# 			emailConfirmationType : string - E-mail confirmation type (type used on /api/v2/emailConfirmation/verify), optional, set only if status requires e-mail confirmation
	# 			meta : string - Address metadata
	# 			updatedTs : string
	# 			inMoratorium : boolean
	# 		}
	# 	]
	# 	pagination : {
	# 		size : integer - Page size
	# 		page : integer - Page number (first page is 0)
	# 		totalPageCount : integer - Total page count
	# 	}
	# }

	# /main/api/v2/accounting/withdrawals/{currency}

	@unittest.skipIf("/main/api/v2/accounting/withdrawals/{currency}" not in TESTING_URIS, "skipping successful")
	def test_withdrawals_for_currency(self):
		check_test_paramters(["currency", "op", "page", "size", "status", "timestamp"])
		withdrawals_for_currency = self.private_api.get_withdrawals_for_currency(CURRENCY, [STATUS], OP, TIMESTAMP, PAGE, SIZE)
		# print(withdrawals_for_currency)
		self.assertIsInstance(withdrawals_for_currency, dict)
		self.assertIsInstance(withdrawals_for_currency["list"], list)
		def test(withdrawal):
			self.assertIsInstance(withdrawal, dict)
			self.assertIsInstance(withdrawal["id"], str)
			self.assert_is_number(withdrawal["created"])
			self.assertIsInstance(withdrawal["currency"], dict)
			self.assertIsInstance(withdrawal["currency"]["enumName"], str)
			self.assertIsInstance(withdrawal["currency"]["description"], str)
			self.assert_is_number(withdrawal["amount"])
			self.assertIsInstance(withdrawal["metadata"], str)
			self.assertIsInstance(withdrawal["accountType"], dict)
			self.assertIsInstance(withdrawal["accountType"]["enumName"], str)
			self.assertIsInstance(withdrawal["accountType"]["description"], str)
			self.assert_is_number(withdrawal["feeAmount"])
			self.assertIsInstance(withdrawal["feeMetadata"], str)
		if TEST_LISTS:
			for withdrawal in withdrawals_for_currency["list"]:
				test(withdrawal)
		elif len(withdrawals_for_currency["list"]) > 0:
			test(withdrawals_for_currency["list"][0])
		else: raise Exception("Empty return data for testing; missing withdrawals for currency")
	# {
	# 	list : [
	# 		{
	# 			id : string - Id of the transaction
	# 			created : integer - Transaction creation timestamp in milliseconds since 1["1"][1970
	# 			currency : {
	# 				enumName : string - Name - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 				description : string - Translated description
	# 			}
	# 			amount : number - Transaction amount
	# 			metadata : string - Transation metadata
	# 			accountType : {
	# 				enumName : string - Name - USER, USER_EXCHANGE_PENDING, USER_WITHDRAWAL_PENDING, USER_DEBT, EXCHANGE_FEE, HASHPOWER_ORDERS, HASHPOWER_PAYOUTS, HASHPOWER_ORDER_FEE, HASHPOWER_PAYOUT_FEE, WALLET_BITGO_BLOCKCHAIN, WALLET_BITGO_DEPOSIT_PENDING, WALLET_BITGO_DEPOSIT_CONFIRMED, WALLET_BITGO_DEPOSITS_FEES, WALLET_BITGO_DEPOSIT_CONFISCATED, WALLET_BITGO_DEPOSIT_UNASSIGNED, WALLET_BITGO_WITHDRAWAL_PENDING, WALLET_BITGO_WITHDRAWAL_CONFIRMED, WALLET_BITGO_WITHDRAWALS_FEES, WALLET_COINBASE_BLOCKCHAIN, WALLET_COINBASE_WITHDRAWAL_PENDING, WALLET_COINBASE_WITHDRAWALS_FEES, WALLET_COINBASE_DEPOSIT_PENDING, WALLET_COINBASE_DEPOSIT_CONFIRMED, WALLET_COINBASE_DEPOSIT_UNASSIGNED, WALLET_PAYEER_WITHDRAWAL_PENDING, WALLET_PAYEER_WITHDRAWALS_FEES, TESTING, WALLET_BITGO_WITHDRAWAL_UNASSIGNED, WALLET_KRIPTOMAT_DEPOSIT_UNASSIGNED, WALLET_KRIPTOMAT_DEPOSIT_FEES, WALLET_KRIPTOMAT_WITHDRAWAL_PENDING, WALLET_KRIPTOMAT_WITHDRAWAL_FEES, WALLET_BLOCKCHAIN_DEPOSIT_PENDING, WALLET_BLOCKCHAIN_DEPOSITS_FEES, WALLET_BLOCKCHAIN_DEPOSIT_UNASSIGNED, WALLET_BLOCKCHAIN_WITHDRAWAL_PENDING, WALLET_BLOCKCHAIN_WITHDRAWALS_FEES, WALLET_LIGHTNING_DEPOSIT_UNASSIGNED, WALLET_LIGHTNING_WITHDRAWAL_PENDING, WALLET_LIGHTNING_WITHDRAWALS_FEES, WALLET_LIGHTNING_DEPOSITS_FEES, WALLET_MULTISIG_DEPOSIT_UNASSIGNED, WALLET_MULTISIG_DEPOSITS_FEES, WALLET_MULTISIG_WITHDRAWALS_FEES, TOKEN_WITHDRAWAL_FEE_PENDING, WALLET_MULTISIG_DEPOSIT_FEES, CHARITY, HASHPOWER_ORDERS_PENDING, USER_FEE, USER_MNG_FEE, USER_EX_FEE
	# 				description : string - Translated description
	# 			}
	# 			feeAmount : number - Fee amount
	# 			feeMetadata : string - Fee metadata
	# 		}
	# 	]
	# 	pagination : {
	# 		size : integer - Page size
	# 		page : integer - Page number (first page is 0)
	# 		totalPageCount : integer - Total page count
	# 	}
	# }

	# Hashpower private

	# /main/api/v2/hashpower/myOrders

	@unittest.skipIf("/main/api/v2/hashpower/myOrders" not in TESTING_URIS, "skipping successful")
	def test_active_orders(self):
		check_test_paramters(["algorithm", "market", "results_limit"])
		active_orders = self.private_api.get_my_active_orders(OP, RESULTS_LIMIT, algorithm=ALGORITHM, market=MARKET)
		# print(active_orders)
		self.assertIsInstance(active_orders, dict)
		self.assertIsInstance(active_orders["list"], list)
		def test(active_order):
			self.assert_is_order_response(active_order)
		if TEST_LISTS:
			for active_order in active_orders["list"]:
				test(active_order)
		elif len(active_orders["list"]) > 0:
			test(active_orders["list"][0])
		else: raise Exception("Empty return data for testing; missing active orders")
	# {
	# 	list : [
	# 		{
	# 			id : string - Order ID
	# 			availableAmount : number - Available total amount
	# 			payedAmount : number - Amount payed for hashpower
	# 			endTs : string - End timestamp in ISO format
	# 			updatedTs : string - Order last updated timestamp in ISO format
	# 			estimateDurationInSeconds : integer - Estimated duration in seconds
	# 			type : {
	# 				code : string - Enum code - STANDARD, FIXED
	# 				description : string - Translated enum
	# 			}
	# 			market : string - Market - EU, USA, EU_N, USA_E
	# 			algorithm : {
	# 				algorithm : string - Algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 				title : string - Title of the algorithm
	# 				enabled : boolean - Is the algorithm Enabled
	# 				order : integer - Algorithm order number
	# 			}
	# 			status : {
	# 				code : string - Order status code - PENDING, ACTIVE, PENDING_CANCELLATION, CANCELLED, DEAD, EXPIRED, ERROR, ERROR_ON_CREATION, ERROR_ON_CREATION_ON_REVERTING_TRANSACTIONS, COMPLETED, ERROR_MISSING
	# 				description : string - Translated description of status
	# 			}
	# 			liquidation : string - Order liquidation
	# 			meta : string - Order meta
	# 			price : number - Order price in BTC/factor[TH/Sol/G]/day
	# 			limit : number - Speed limit [TH/Sol/G]/s
	# 			amount : number - Amount
	# 			displayMarketFactor : string - Unit of market factor
	# 			marketFactor : number - Market factor
	# 			alive : boolean - Order is alive
	# 			startTs : string - Start timestamp in ISO format
	# 			pool : {
	# 				id : string - Pool id (When creating new pool this value should not be set.)
	# 				name : string - Pool custom name
	# 				algorithm : string - Pool algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 				stratumHostname : string - Hostname or not ip of the pool
	# 				stratumPort : integer - Port of the pool
	# 				username : string - Username
	# 				password : string - Password (Set password to # when using ethproxy pool.)
	# 				status : string - Verification status - VERIFIED, NOT_VERIFIED
	# 				updatedTs : string
	# 				inMoratorium : boolean
	# 			}
	# 			acceptedCurrentSpeed : number - Current accepted speed [TH/Sol/G]/s
	# 			rigsCount : integer - Rigs count
	# 			organizationId : string - Organization Id
	# 			creatorUserId : string - Creator Id
	# 		}
	# 	]
	# }

	# /main/api/v2/hashpower/order

	@unittest.skipIf("/main/api/v2/hashpower/order" not in TESTING_URIS, "skipping successful")
	def test_standard_hashpower_order(self):
		check_test_paramters(["algorithm", "market", "limit", "price", "amount", "pool_id"])
		standard_hashpower_order = self.private_api.create_standard_hashpower_order(MARKET, ALGORITHM, PRICE, LIMIT, AMOUNT, POOL_ID)
		print(standard_hashpower_order)
		self.assert_is_order_response(standard_hashpower_order)
	# {
	# 	id : string - Id of hashpower order
	# 	createdTs : string - Timestamp when order was created in ISO format
	# 	updatedTs : string - Timestamp when order was last updated in ISO format
	# 	requestId : string - Idem of order
	# 	type : {
	# 		code : string - Enum code - STANDARD, FIXED
	# 		description : string - Translated enum
	# 	}
	# 	market : string - Location where order was placed - EU, USA, EU_N, USA_E
	# 	algorithm : {
	# 		algorithm : string - Algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 		title : string - Title of the algorithm
	# 		enabled : boolean - Is the algorithm Enabled
	# 		order : integer - Algorithm order number
	# 	}
	# 	status : {
	# 		code : string - Order status code - PENDING, ACTIVE, PENDING_CANCELLATION, CANCELLED, DEAD, EXPIRED, ERROR, ERROR_ON_CREATION, ERROR_ON_CREATION_ON_REVERTING_TRANSACTIONS, COMPLETED, ERROR_MISSING
	# 		description : string - Translated description of status
	# 	}
	# 	price : number - Order price
	# 	limit : number - Speed limit
	# 	amount : number - Amount in the order
	# 	availableAmount : number - Available amount
	# 	payedAmount : number - Amount payed for hashpower
	# 	alive : boolean - Is order alive
	# 	startTs : string - Start timestamp in ISO format
	# 	endTs : string - End timestamp in ISO format
	# 	pool : {
	# 		id : string - Pool id (When creating new pool this value should not be set.)
	# 		name : string - Pool custom name
	# 		algorithm : string - Pool algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 		stratumHostname : string - Hostname or ip of the pool
	# 		stratumPort : integer - Port of the pool
	# 		username : string - Username
	# 		password : string - Password (Set password to # when using ethproxy pool.)
	# 		status : string - Verification status - VERIFIED, NOT_VERIFIED
	# 		updatedTs : string
	# 		inMoratorium : boolean
	# 	}
	# 	organizationId : string - Organisation Id
	# 	creatorUserId : string - User Id
	# 	rigsCount : integer - Number of rigs mining for this order
	# 	acceptedCurrentSpeed : number - Accepted speed
	# 	miningStatus : string - Current mining status, available only when active - INACTIVE, LIVE, DEAD_POOL
	# 	displayMarketFactor : string - Market faktor unit
	# 	marketFactor : number - Market factor
	# 	estimateDurationInSeconds : integer - Estimated duration in seconds
	# 	bridges : [
	# 		{
	# 			rigsCount : integer - Numer of rigs on bridge
	# 			speedAccepted : number - Speed accepted by the bridge
	# 			speedRewarded : number - Speed rewarded by the bridge
	# 			difficulty : number - Pool difficulty
	# 			status : string - Bridge statues
	# 		}
	# 	]
	# 	liquidation : string - Order liquidation
	# }

	@unittest.skipIf("/main/api/v2/hashpower/order" not in TESTING_URIS, "skipping successful")
	def test_fixed_hashpower_order(self):
		check_test_paramters(["algorithm", "market", "limit", "price", "amount", "pool_id"])
		fixed_hashpower_order = self.private_api.create_fixed_hashpower_order(MARKET, ALGORITHM, PRICE, LIMIT, AMOUNT, POOL_ID)
		# print(fixed_hashpower_order)
		self.assert_is_order_response(fixed_hashpower_order)
	# {
	# 	id : string - Id of hashpower order
	# 	createdTs : string - Timestamp when order was created in ISO format
	# 	updatedTs : string - Timestamp when order was last updated in ISO format
	# 	requestId : string - Idem of order
	# 	type : {
	# 		code : string - Enum code - STANDARD, FIXED
	# 		description : string - Translated enum
	# 	}
	# 	market : string - Location where order was placed - EU, USA, EU_N, USA_E
	# 	algorithm : {
	# 		algorithm : string - Algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 		title : string - Title of the algorithm
	# 		enabled : boolean - Is the algorithm Enabled
	# 		order : integer - Algorithm order number
	# 	}
	# 	status : {
	# 		code : string - Order status code - PENDING, ACTIVE, PENDING_CANCELLATION, CANCELLED, DEAD, EXPIRED, ERROR, ERROR_ON_CREATION, ERROR_ON_CREATION_ON_REVERTING_TRANSACTIONS, COMPLETED, ERROR_MISSING
	# 		description : string - Translated description of status
	# 	}
	# 	price : number - Order price
	# 	limit : number - Speed limit
	# 	amount : number - Amount in the order
	# 	availableAmount : number - Available amount
	# 	payedAmount : number - Amount payed for hashpower
	# 	alive : boolean - Is order alive
	# 	startTs : string - Start timestamp in ISO format
	# 	endTs : string - End timestamp in ISO format
	# 	pool : {
	# 		id : string - Pool id (When creating new pool this value should not be set.)
	# 		name : string - Pool custom name
	# 		algorithm : string - Pool algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 		stratumHostname : string - Hostname or ip of the pool
	# 		stratumPort : integer - Port of the pool
	# 		username : string - Username
	# 		password : string - Password (Set password to # when using ethproxy pool.)
	# 		status : string - Verification status - VERIFIED, NOT_VERIFIED
	# 		updatedTs : string
	# 		inMoratorium : boolean
	# 	}
	# 	organizationId : string - Organisation Id
	# 	creatorUserId : string - User Id
	# 	rigsCount : integer - Number of rigs mining for this order
	# 	acceptedCurrentSpeed : number - Accepted speed
	# 	miningStatus : string - Current mining status, available only when active - INACTIVE, LIVE, DEAD_POOL
	# 	displayMarketFactor : string - Market faktor unit
	# 	marketFactor : number - Market factor
	# 	estimateDurationInSeconds : integer - Estimated duration in seconds
	# 	bridges : [
	# 		{
	# 			rigsCount : integer - Numer of rigs on bridge
	# 			speedAccepted : number - Speed accepted by the bridge
	# 			speedRewarded : number - Speed rewarded by the bridge
	# 			difficulty : number - Pool difficulty
	# 			status : string - Bridge statues
	# 		}
	# 	]
	# 	liquidation : string - Order liquidation
	# }

	# /main/api/v2/hashpower/order/{id}

	@unittest.skipIf("/main/api/v2/hashpower/order/{id}" not in TESTING_URIS, "skipping successful")
	def test_order_details(self):
		check_test_paramters(["order_id"])
		order_details = self.private_api.get_order_details(ORDER_ID)
		# print(order_details)
		self.assert_is_order_response(order_details)
	# {
	# 	id : string - Id of hashpower order
	# 	createdTs : string - Timestamp when order was created in ISO format
	# 	updatedTs : string - Timestamp when order was last updated in ISO format
	# 	requestId : string - Idem of order
	# 	type : {
	# 		code : string - Enum code - STANDARD, FIXED
	# 		description : string - Translated enum
	# 	}
	# 	market : string - Location where order was placed - EU, USA, EU_N, USA_E
	# 	algorithm : {
	# 		algorithm : string - Algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 		title : string - Title of the algorithm
	# 		enabled : boolean - Is the algorithm Enabled
	# 		order : integer - Algorithm order number
	# 	}
	# 	status : {
	# 		code : string - Order status code - PENDING, ACTIVE, PENDING_CANCELLATION, CANCELLED, DEAD, EXPIRED, ERROR, ERROR_ON_CREATION, ERROR_ON_CREATION_ON_REVERTING_TRANSACTIONS, COMPLETED, ERROR_MISSING
	# 		description : string - Translated description of status
	# 	}
	# 	price : number - Order price
	# 	limit : number - Speed limit
	# 	amount : number - Amount in the order
	# 	availableAmount : number - Available amount
	# 	payedAmount : number - Amount payed for hashpower
	# 	alive : boolean - Is order alive
	# 	startTs : string - Start timestamp in ISO format
	# 	endTs : string - End timestamp in ISO format
	# 	pool : {
	# 		id : string - Pool id (When creating new pool this value should not be set.)
	# 		name : string - Pool custom name
	# 		algorithm : string - Pool algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 		stratumHostname : string - Hostname or ip of the pool
	# 		stratumPort : integer - Port of the pool
	# 		username : string - Username
	# 		password : string - Password (Set password to # when using ethproxy pool.)
	# 		status : string - Verification status - VERIFIED, NOT_VERIFIED
	# 		updatedTs : string
	# 		inMoratorium : boolean
	# 	}
	# 	organizationId : string - Organisation Id
	# 	creatorUserId : string - User Id
	# 	rigsCount : integer - Number of rigs mining for this order
	# 	acceptedCurrentSpeed : number - Accepted speed
	# 	miningStatus : string - Current mining status, available only when active - INACTIVE, LIVE, DEAD_POOL
	# 	displayMarketFactor : string - Market faktor unit
	# 	marketFactor : number - Market factor
	# 	estimateDurationInSeconds : integer - Estimated duration in seconds
	# 	bridges : [
	# 		{
	# 			rigsCount : integer - Numer of rigs on bridge
	# 			speedAccepted : number - Speed accepted by the bridge
	# 			speedRewarded : number - Speed rewarded by the bridge
	# 			difficulty : number - Pool difficulty
	# 			status : string - Bridge statues
	# 		}
	# 	]
	# 	liquidation : string - Order liquidation
	# }


	# /main/api/v2/hashpower/order/{id}

	@unittest.skipIf("/main/api/v2/hashpower/order/{id}" not in TESTING_URIS, "skipping successful")
	def test_hashpower_order(self):
		check_test_paramters(["order_id"])
		hashpower_order = self.private_api.cancel_hashpower_order(ORDER_ID)
		# print(hashpower_order)
		self.assert_is_order_response(hashpower_order)
	# {
	# 	id : string - Id of hashpower order
	# 	createdTs : string - Timestamp when order was created in ISO format
	# 	updatedTs : string - Timestamp when order was last updated in ISO format
	# 	requestId : string - Idem of order
	# 	type : {
	# 		code : string - Enum code - STANDARD, FIXED
	# 		description : string - Translated enum
	# 	}
	# 	market : string - Location where order was placed - EU, USA, EU_N, USA_E
	# 	algorithm : {
	# 		algorithm : string - Algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 		title : string - Title of the algorithm
	# 		enabled : boolean - Is the algorithm Enabled
	# 		order : integer - Algorithm order number
	# 	}
	# 	status : {
	# 		code : string - Order status code - PENDING, ACTIVE, PENDING_CANCELLATION, CANCELLED, DEAD, EXPIRED, ERROR, ERROR_ON_CREATION, ERROR_ON_CREATION_ON_REVERTING_TRANSACTIONS, COMPLETED, ERROR_MISSING
	# 		description : string - Translated description of status
	# 	}
	# 	price : number - Order price
	# 	limit : number - Speed limit
	# 	amount : number - Amount in the order
	# 	availableAmount : number - Available amount
	# 	payedAmount : number - Amount payed for hashpower
	# 	alive : boolean - Is order alive
	# 	startTs : string - Start timestamp in ISO format
	# 	endTs : string - End timestamp in ISO format
	# 	pool : {
	# 		id : string - Pool id (When creating new pool this value should not be set.)
	# 		name : string - Pool custom name
	# 		algorithm : string - Pool algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 		stratumHostname : string - Hostname or ip of the pool
	# 		stratumPort : integer - Port of the pool
	# 		username : string - Username
	# 		password : string - Password (Set password to # when using ethproxy pool.)
	# 		status : string - Verification status - VERIFIED, NOT_VERIFIED
	# 		updatedTs : string
	# 		inMoratorium : boolean
	# 	}
	# 	organizationId : string - Organisation Id
	# 	creatorUserId : string - User Id
	# 	rigsCount : integer - Number of rigs mining for this order
	# 	acceptedCurrentSpeed : number - Accepted speed
	# 	miningStatus : string - Current mining status, available only when active - INACTIVE, LIVE, DEAD_POOL
	# 	displayMarketFactor : string - Market faktor unit
	# 	marketFactor : number - Market factor
	# 	estimateDurationInSeconds : integer - Estimated duration in seconds
	# 	bridges : [
	# 		{
	# 			rigsCount : integer - Numer of rigs on bridge
	# 			speedAccepted : number - Speed accepted by the bridge
	# 			speedRewarded : number - Speed rewarded by the bridge
	# 			difficulty : number - Pool difficulty
	# 			status : string - Bridge statues
	# 		}
	# 	]
	# 	liquidation : string - Order liquidation
	# }


	# /main/api/v2/hashpower/order/{id}/refill

	@unittest.skipIf("/main/api/v2/hashpower/order/{id}/refill" not in TESTING_URIS, "skipping successful")
	def test_hashpower_order(self):
		check_test_paramters(["order_id", "amount"])
		hashpower_order = self.private_api.refill_hashpower_order(ORDER_ID, AMOUNT)
		# print(hashpower_order)
		self.assert_is_order_response(hashpower_order)
	# {
	# 	id : string - Id of hashpower order
	# 	createdTs : string - Timestamp when order was created in ISO format
	# 	updatedTs : string - Timestamp when order was last updated in ISO format
	# 	requestId : string - Idem of order
	# 	type : {
	# 		code : string - Enum code - STANDARD, FIXED
	# 		description : string - Translated enum
	# 	}
	# 	market : string - Location where order was placed - EU, USA, EU_N, USA_E
	# 	algorithm : {
	# 		algorithm : string - Algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 		title : string - Title of the algorithm
	# 		enabled : boolean - Is the algorithm Enabled
	# 		order : integer - Algorithm order number
	# 	}
	# 	status : {
	# 		code : string - Order status code - PENDING, ACTIVE, PENDING_CANCELLATION, CANCELLED, DEAD, EXPIRED, ERROR, ERROR_ON_CREATION, ERROR_ON_CREATION_ON_REVERTING_TRANSACTIONS, COMPLETED, ERROR_MISSING
	# 		description : string - Translated description of status
	# 	}
	# 	price : number - Order price
	# 	limit : number - Speed limit
	# 	amount : number - Amount in the order
	# 	availableAmount : number - Available amount
	# 	payedAmount : number - Amount payed for hashpower
	# 	alive : boolean - Is order alive
	# 	startTs : string - Start timestamp in ISO format
	# 	endTs : string - End timestamp in ISO format
	# 	pool : {
	# 		id : string - Pool id (When creating new pool this value should not be set.)
	# 		name : string - Pool custom name
	# 		algorithm : string - Pool algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 		stratumHostname : string - Hostname or ip of the pool
	# 		stratumPort : integer - Port of the pool
	# 		username : string - Username
	# 		password : string - Password (Set password to # when using ethproxy pool.)
	# 		status : string - Verification status - VERIFIED, NOT_VERIFIED
	# 		updatedTs : string
	# 		inMoratorium : boolean
	# 	}
	# 	organizationId : string - Organisation Id
	# 	creatorUserId : string - User Id
	# 	rigsCount : integer - Number of rigs mining for this order
	# 	acceptedCurrentSpeed : number - Accepted speed
	# 	miningStatus : string - Current mining status, available only when active - INACTIVE, LIVE, DEAD_POOL
	# 	displayMarketFactor : string - Market faktor unit
	# 	marketFactor : number - Market factor
	# 	estimateDurationInSeconds : integer - Estimated duration in seconds
	# 	bridges : [
	# 		{
	# 			rigsCount : integer - Numer of rigs on bridge
	# 			speedAccepted : number - Speed accepted by the bridge
	# 			speedRewarded : number - Speed rewarded by the bridge
	# 			difficulty : number - Pool difficulty
	# 			status : string - Bridge statues
	# 		}
	# 	]
	# 	liquidation : string - Order liquidation
	# }

	# /main/api/v2/hashpower/order/{id}/stats

	@unittest.skipIf("/main/api/v2/hashpower/order/{id}/stats" not in TESTING_URIS, "skipping successful")
	def test_order_statistics(self):
		check_test_paramters(["order_id"])
		order_statistics = self.private_api.get_order_statistics(ORDER_ID)
		# print(order_statistics)
		self.assertIsInstance(order_statistics, dict)
		self.assertIsInstance(order_statistics["displayMarketFactor"], str)
		self.assert_is_number(order_statistics["marketFactor"])
		self.assertIsInstance(order_statistics["columns"], list)
		def test(col):
			self.assertIsInstance(col, str)
		if TEST_LISTS:
			for col in order_statistics["columns"]:
				test(col)
		elif len(order_statistics["columns"]) > 0:
			test(order_statistics["columns"][0])
		else: raise Exception("Empty return data for testing; missing order statistics columns")
		self.assertIsInstance(order_statistics["data"], list)
		def test2(data):
			self.assertIsInstance(data, list)
			def test3(stat):
				self.assertIsInstance(stat, dict)
			if TEST_LISTS:
				for stat in data:
					test3(stat)
			elif len(data) > 0:
				test3(data[0])
		if TEST_LISTS:
			for data in  order_statistics["data"]:
				test2(data)
		elif len(order_statistics["data"]) > 0:
			test2(order_statistics["data"][0])
		else: raise Exception("Empty return data for testing; missing order statistics data")
	# {
	# 	displayMarketFactor : string - Unit for market factor
	# 	marketFactor : number - Market factor
	# 	columns : [
	# 		string - Stream definition
	# 	]
	# 	data : [
	# 		[
	# 			object - Statistical data
	# 		]
	# 	]
	# }

	# /main/api/v2/hashpower/order/{id}/updatePriceAndLimit

	@unittest.skipIf("/main/api/v2/hashpower/order/{id}/updatePriceAndLimit" not in TESTING_URIS, "skipping successful")
	def test_set_price_hashpower_order(self):
		check_test_paramters(["order_id", "algorithm", "price"])
		hashpower_order = self.private_api.set_price_hashpower_order(ORDER_ID, PRICE, ALGORITHM)
		# print(hashpower_order)
		self.assert_is_order_response(order)

	@unittest.skipIf("/main/api/v2/hashpower/order/{id}/updatePriceAndLimit" not in TESTING_URIS, "skipping successful")
	def test_set_limit_hashpower_order(self):
		check_test_paramters(["order_id", "algorithm", "price"])
		hashpower_order = self.private_api.set_limit_hashpower_order(ORDER_ID, LIMIT, ALGORITHM)
		# print(hashpower_order)
		self.assert_is_order_response(order)

	@unittest.skipIf("/main/api/v2/hashpower/order/{id}/updatePriceAndLimit" not in TESTING_URIS, "skipping successful")
	def test_set_price_and_limit_hashpower_order(self):
		check_test_paramters(["order_id", "algorithm", "price", "limit"])
		hashpower_order = self.private_api.set_price_and_limit_hashpower_order(ORDER_ID, PRICE, LIMIT, ALGORITHM)
		# print(hashpower_order)
		self.assert_is_order_response(order)

	def assert_is_order_response(self, order):
		self.assertIsInstance(order, dict)
		self.assertIsInstance(order["list"], list)
		self.assertIsInstance(order, dict)
		self.assertIsInstance(order["id"], str)
		self.assertIsInstance(order["createdTs"], str)
		self.assertIsInstance(order["updatedTs"], str)
		self.assertIsInstance(order["requestId"], str)
		self.assertIsInstance(order["type"], dict)
		self.assertIsInstance(order["type"]["code"], str)
		self.assertIsInstance(order["type"]["description"], str)
		self.assertIsInstance(order["market"], str)
		self.assertIsInstance(order["algorithm"], dict)
		self.assertIsInstance(order["algorithm"]["algorithm"], str)
		self.assertIsInstance(order["algorithm"]["title"], str)
		self.assertIsInstance(order["algorithm"]["enabled"], bool)
		self.assert_is_number(order["algorithm"]["order"])
		self.assertIsInstance(order["status"], dict)
		self.assertIsInstance(order["status"]["code"], str)
		self.assertIsInstance(order["status"]["description"], str)
		self.assert_is_number(order["price"])
		self.assert_is_number(order["limit"])
		self.assert_is_number(order["amount"])
		self.assert_is_number(order["availableAmount"])
		self.assert_is_number(order["payedAmount"])
		self.assertIsInstance(order["alive"], bool)
		self.assertIsInstance(order["startTs"], str)
		self.assertIsInstance(order["endTs"], str)
		self.assertIsInstance(order["pool"], dict)
		self.assertIsInstance(order["pool"]["id"], str)
		self.assertIsInstance(order["pool"]["name"], str)
		self.assertIsInstance(order["pool"]["algorithm"], str)
		self.assertIsInstance(order["pool"]["stratumHostname"], str)
		self.assert_is_number(order["pool"]["stratumPort"])
		self.assertIsInstance(order["pool"]["username"], str)
		self.assertIsInstance(order["pool"]["password"], str)
		self.assertIsInstance(order["pool"]["status"], str)
		self.assertIsInstance(order["pool"]["updatedTs"], str)
		self.assertIsInstance(order["pool"]["inMoratorium"], bool)
		self.assertIsInstance(order["organizationId"], str)
		self.assertIsInstance(order["creatorUserId"], str)
		self.assert_is_number(order["rigsCount"])
		self.assert_is_number(order["acceptedCurrentSpeed"])
		self.assert_is_number(order["miningStatus"])
		self.assertIsInstance(order["displayMarketFactor"], str)
		self.assert_is_number(order["marketFactor"])
		self.assert_is_number(order["estimateDurationInSeconds"])
		self.assertIsInstance(order["bridges"], list)
		def test(bridge):
			self.assert_is_number(bridge["rigsCount"])
			self.assert_is_number(bridge["speedAccepted"])
			self.assert_is_number(bridge["speedRewarded"])
			self.assert_is_number(bridge["difficulty"])
			self.assertIsInstance(bridge["status"], str)
		if TEST_LISTS:
			for bridge in order["bridges"]:
				test(bridge)
		elif len(order["bridges"]) > 0:
			test(order["bridges"][0])
		else: raise Exception("Empty return data for testing; missing order bridges")
		self.assertIsInstance(order["liquidation"], str)
	# {
	# 	id : string - Id of hashpower order
	# 	createdTs : string - Timestamp when order was created in ISO format
	# 	updatedTs : string - Timestamp when order was last updated in ISO format
	# 	requestId : string - Idem of order
	# 	type : {
	# 		code : string - Enum code - STANDARD, FIXED
	# 		description : string - Translated enum
	# 	}
	# 	market : string - Location where order was placed - EU, USA, EU_N, USA_E
	# 	algorithm : {
	# 		algorithm : string - Algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 		title : string - Title of the algorithm
	# 		enabled : boolean - Is the algorithm Enabled
	# 		order : integer - Algorithm order number
	# 	}
	# 	status : {
	# 		code : string - Order status code - PENDING, ACTIVE, PENDING_CANCELLATION, CANCELLED, DEAD, EXPIRED, ERROR, ERROR_ON_CREATION, ERROR_ON_CREATION_ON_REVERTING_TRANSACTIONS, COMPLETED, ERROR_MISSING
	# 		description : string - Translated description of status
	# 	}
	# 	price : number - Order price
	# 	limit : number - Speed limit
	# 	amount : number - Amount in the order
	# 	availableAmount : number - Available amount
	# 	payedAmount : number - Amount payed for hashpower
	# 	alive : boolean - Is order alive
	# 	startTs : string - Start timestamp in ISO format
	# 	endTs : string - End timestamp in ISO format
	# 	pool : {
	# 		id : string - Pool id (When creating new pool this value should not be set.)
	# 		name : string - Pool custom name
	# 		algorithm : string - Pool algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 		stratumHostname : string - Hostname or ip of the pool
	# 		stratumPort : integer - Port of the pool
	# 		username : string - Username
	# 		password : string - Password (Set password to # when using ethproxy pool.)
	# 		status : string - Verification status - VERIFIED, NOT_VERIFIED
	# 		updatedTs : string
	# 		inMoratorium : boolean
	# 	}
	# 	organizationId : string - Organisation Id
	# 	creatorUserId : string - User Id
	# 	rigsCount : integer - Number of rigs mining for this order
	# 	acceptedCurrentSpeed : number - Accepted speed
	# 	miningStatus : string - Current mining status, available only when active - INACTIVE, LIVE, DEAD_POOL
	# 	displayMarketFactor : string - Market faktor unit
	# 	marketFactor : number - Market factor
	# 	estimateDurationInSeconds : integer - Estimated duration in seconds
	# 	bridges : [
	# 		{
	# 			rigsCount : integer - Numer of rigs on bridge
	# 			speedAccepted : number - Speed accepted by the bridge
	# 			speedRewarded : number - Speed rewarded by the bridge
	# 			difficulty : number - Pool difficulty
	# 			status : string - Bridge statues
	# 		}
	# 	]
	# 	liquidation : string - Order liquidation
	# }

	# /main/api/v2/hashpower/orders/calculateEstimateDuration

	@unittest.skipIf("/main/api/v2/hashpower/orders/calculateEstimateDuration" not in TESTING_URIS, "skipping successful")
	def test_order_duration(self):
		check_test_paramters(["algorithm", "hashpower_order_type", "price", "limit", "amount"])
		order_duration = self.private_api.estimate_order_duration(ALGORITHM, HASHPOWER_ORDER_TYPE, PRICE, LIMIT, AMOUNT)
		# print(order_duration)
		self.assertIsInstance(order_duration, dict)
		self.assert_is_number(order_duration["estimateDurationInSeconds"])
	# {
	# 	estimateDurationInSeconds : integer - Estimated duration in seconds
	# }

	# Miner private

	# /main/api/v2/mining/groups/list

	@unittest.skipIf("/main/api/v2/mining/groups/list" not in TESTING_URIS, "skipping successful")
	@unittest.expectedFailure
	def test_groups(self):
		groups = self.private_api.get_groups()
		# print(groups)
		self.assertIsInstance(groups, dict)
		self.assertIsInstance(groups["groups"], dict)
		if len(groups["groups"].keys()) == 0:
			raise Exception("Empty return data for testing; must mine with rig and create group online")
		# try:
		self.assertIsInstance(groups["rigs"], list)
		def test(rig):
			self.assertIsInstance(rig["rigId"], str)
			self.assertIsInstance(rig["name"], str)
			self.assertIsInstance(rig["status"], str)
			self.assertIsInstance(rig["powerMode"], str)
			self.assertIsInstance(rig["notifications"], list)
			def test2(n):
				self.assertIsInstance(n, str)
			if TEST_LISTS:
				for n in rig["notifications"]:
					test2(n)
			elif len(rig["notifications"]) > 0:
				test2(rig["notifications"][0])
			self.assert_is_number(rig["totalDevices"])
			self.assert_is_number(rig["activeDevices"])
		if TEST_LISTS:
			for rig in groups["rigs"]:
				test(rig)
		elif len(groups["rigs"]) > 0:
			test(groups["rigs"][0])
		else: raise Exception("Empty return data for testing; missing rig groups")
		# except KeyError: pass
		self.assert_is_number(groups["totalRigs"])
		self.assert_is_number(groups["miningRigs"])
		self.assertIsInstance(groups["groupPowerMode"], str)
		self.assertIsInstance(groups["notifications"], dict)
	# {
	# 	groups : {
	# 		{
	# 			rigs : [
	# 				{
	# 					rigId : string - Rig id
	# 					name : string - Rig name (if rig is unamanaged, then name is worker id)
	# 					status : string - Rig status - BENCHMARKING, MINING, STOPPED, OFFLINE, ERROR, PENDING, DISABLED, TRANSFERRED, UNKNOWN
	# 					powerMode : string - Rig's devices power mode - UNKNOWN, LOW, MEDIUM, HIGH, MIXED
	# 					notifications : [
	# 						string - Rig Notifications - UNKNOWN, RIG_OFFLINE, RIG_ERROR, UNRECOGNIZED
	# 					]
	# 					totalDevices : integer - Total devices on rig
	# 					activeDevices : integer - Active devices on rig
	# 				}
	# 			]
	# 			totalRigs : integer - Number of total devices in group
	# 			miningRigs : integer - Number of active devices
	# 			groupPowerMode : string - Group power mode combined from all devices in group or group's subgroup - UNKNOWN, LOW, MEDIUM, HIGH, MIXED
	# 			notifications : {
	# 				string - Rig Notifications of rigs in group with - ALL, PARTIAL
	# 			}
	# 		}
	# 	}
	# }

	# /main/api/v2/mining/miningAddress

	@unittest.skipIf("/main/api/v2/mining/miningAddress" not in TESTING_URIS, "skipping successful")
	def test_mining_address(self):
		mining_address = self.private_api.get_mining_address()
		# print(mining_address)
		self.assertIsInstance(mining_address, dict)
		self.assertIsInstance(mining_address["address"], str)
	# {
	# 	address : string - BTC mining address
	# }

	# /main/api/v2/mining/rig/stats/algo

	@unittest.skipIf("/main/api/v2/mining/rig/stats/algo" not in TESTING_URIS, "skipping successful")
	def test_rig_algo_statst(self):
		check_test_paramters(["rig_id"])
		rig_algo_stats = self.private_api.get_rig_algo_stats(RIG_ID)
		# print(rig_algo_stats)
		self.assertIsInstance(rig_algo_stats, dict)
		def test(col):
			self.assertIsInstance(col, str)
		if TEST_LISTS:
			for col in rig_algo_stats["columns"]:
				test(col)
		elif len(rig_algo_stats["columns"]) > 0:
			test(rig_algo_stats["columns"][0])
		else: raise Exception("Empty return data for testing; missing algo statistics columns")
		def test2(data):
			self.assertIsInstance(data, list)
			def test3(stat):
				self.assertIsInstance(stat, dict)
			if TEST_LISTS:
				for stat in data:
					test3(stat)
			elif len(data) > 0:
				test3(data[0])
		if TEST_LISTS:
			for data in rig_algo_stats["data"]:
				test2(data)
		elif len(rig_algo_stats["data"]) > 0:
			test2(rig_algo_stats["data"][0]) 
		else: raise Exception("Empty return data for testing; missing algo statistics data")
	# {
	# 	columns : [
	# 		string - Column definition of statistical streams
	# 	]
	# 	data : [
	# 		[
	# 			object - Statistical data
	# 		]
	# 	]
	# }

	# /main/api/v2/mining/rig/stats/unpaid

	@unittest.skipIf("/main/api/v2/mining/rig/stats/unpaid" not in TESTING_URIS, "skipping successful")
	def test_rig_unpaid_stats(self):
		check_test_paramters(["rig_id"])
		rig_unpaid_stats = self.private_api.get_rig_unpaid_stats(RIG_ID)
		# print(rig_unpaid_stats)
		self.assertIsInstance(rig_unpaid_stats, dict)
		def test(col):
			self.assertIsInstance(col, str)
		if TEST_LISTS:
			for col in rig_unpaid_stats["columns"]:
				test(col)
		elif len(rig_unpaid_stats["columns"]) > 0:
			test(rig_unpaid_stats["columns"][0])
		else: raise Exception("Empty return data for testing; missing unpaid rig statistical columns")
		def test2(data):
			self.assertIsInstance(data, list)
			def test3(stat):
				self.assertIsInstance(stat, dict)
			if TEST_LISTS:
				for stat in data:
					test3(stat)
			elif len(data) > 0:
				test3(data[0])
		if TEST_LISTS:
			for data in rig_unpaid_stats["data"]:
				test2(data)
		elif len(rig_unpaid_stats["data"]) > 0:
			test2(rig_unpaid_stats["data"][0])
		else: raise Exception("Empty return data for testing; missing unpaid rig statistical data")
# {
# 	columns : [
# 		string - Column definition of statistical streams
# 	]
# 	data : [
# 		[
# 			object - Statistical data
# 		]
# 	]
# }

	# /main/api/v2/mining/rig2/{rigId}

	@unittest.skipIf("/main/api/v2/mining/rig2/{rigId}" not in TESTING_URIS, "skipping successful")
	def test_rig_by_id(self):
		check_test_paramters(["rig_id"])
		rig = self.private_api.get_rig_by_id(RIG_ID)
		# print(rig)
		self.assertIsInstance(rig, dict)
		self.assertIsInstance(rig["rigId"], str)
		self.assertIsInstance(rig["type"], str)
		self.assertIsInstance(rig["name"], str)
		self.assert_is_number(rig["statusTime"])
		self.assert_is_number(rig["joinTime"])
		self.assertIsInstance(rig["minerStatus"], str)
		self.assertIsInstance(rig["groupName"], str)
		self.assert_is_number(rig["unpaidAmount"])
		self.assertIsInstance(rig["notifications"], list)
		def test(n):
			self.assertIsInstance(n, str)
		if TEST_LISTS:
			for n in rig["notifications"]:
				test(n)
		elif len(rig["notifications"]) > 0:
			test(rig["notifications"][0])
		else: raise Exception("Empty return data for testing; missing rig notifications")
		self.assertIsInstance(rig["softwareVersions"], str)
		self.assertIsInstance(rig["devices"], list)
		def test2(device):
			self.assertIsInstance(device["id"], str)
			self.assertIsInstance(device["name"], str)
			self.assertIsInstance(device["deviceType"], dict)
			self.assertIsInstance(device["deviceType"]["enumName"], str)
			self.assertIsInstance(device["deviceType"]["description"], str)
			self.assertIsInstance(device["status"], dict)
			self.assertIsInstance(device["status"]["enumName"], str)
			self.assertIsInstance(device["status"]["description"], str)
			self.assert_is_number(device["temperature"])
			self.assert_is_number(device["load"])
			self.assert_is_number(device["revolutionsPerMinute"])
			self.assert_is_number(device["revolutionsPerMinutePercentage"])
			self.assertIsInstance(device["powerMode"], dict)
			self.assertIsInstance(device["powerMode"]["enumName"], str)
			self.assertIsInstance(device["powerMode"]["description"], str)
			self.assert_is_number(device["powerUsage"])
			self.assertIsInstance(device["speeds"], list)
			def test3(speed):
				self.assertIsInstance(speed, dict)
				self.assertIsInstance(speed["algorithm"], str)
				self.assertIsInstance(speed["title"], str)
				self.assert_is_number(speed["speed"])
				self.assertIsInstance(speed["displaySuffix"], str)
			if TEST_LISTS:
				for speed in device["speeds"]:
					test3(speed)
			elif len(device["speeds"]) > 0:
				test3(device["speeds"][0])
			else: raise Exception("Empty return data for testing; missing device speeds")
			self.assertIsInstance(device["intensity"], dict)
			self.assertIsInstance(device["intensity"]["enumName"], str)
			self.assertIsInstance(device["intensity"]["description"], str)
			self.assertIsInstance(device["nhqm"], str)
		if TEST_LISTS:
			for device in rig["devices"]:
				test2(device)
		elif len(rig["devices"]) > 0:
			test2(rig["devices"][0])
		else: raise Exception("Empty return data for testing; missing rig devices")
		self.assertIsInstance(rig["cpuMiningEnabled"], bool)
		self.assertIsInstance(rig["cpuExists"], bool)
		self.assertIsInstance(rig["stats"], list)
		def test4(stat):
			self.assertIsInstance(stat, dict)
			self.assert_is_number(stat["statsTime"])
			self.assert_is_number(stat["market"])
			self.assertIsInstance(stat["algorithm"], dict)
			self.assertIsInstance(stat["algorithm"]["enumName"], str)
			self.assertIsInstance(stat["algorithm"]["description"], str)
			self.assert_is_number(stat["unpaidAmount"])
			self.assert_is_number(stat["difficulty"])
			self.assert_is_number(stat["proxyId"])
			self.assert_is_number(stat["timeConnected"])
			self.assertIsInstance(stat["xnsub"], bool)
			self.assert_is_number(stat["speedAccepted"])
			self.assert_is_number(stat["speedRejectedR1Target"])
			self.assert_is_number(stat["speedRejectedR2Stale"])
			self.assert_is_number(stat["speedRejectedR3Duplicate"])
			self.assert_is_number(stat["speedRejectedR4NTime"])
			self.assert_is_number(stat["speedRejectedR5Other"])
			self.assert_is_number(stat["speedRejectedTotal"])
			self.assert_is_number(stat["profitability"])
		if TEST_LISTS:
			for stat in rig["stats"]:
				test4(stat)
		elif len(rig["stats"]) > 0:
			test4(rig["stats"][0])
		else: raise Exception("Empty return data for testing; missing rig stats")
		self.assert_is_number(rig["profitability"])
		self.assert_is_number(rig["localProfitability"])
		self.assertIsInstance(rig["rigPowerMode"], str)
	# {
	# 	rigId : string - consolidated rigId (part of RIG identity, see {@link RigIdentifier#getRigId()})
	# 	type : string - Rig type - MANAGED, UNMANAGED
	# 	name : string - Worker Name (optional)
	# 	statusTime : integer - The timestamp (EPOCH millis) of this status
	# 	joinTime : integer - The timestamp (EPOCH millis) of RIG joining
	# 	minerStatus : string - Miner status (passed directly from NHM) - BENCHMARKING, MINING, STOPPED, OFFLINE, ERROR, PENDING, DISABLED, TRANSFERRED, UNKNOWN
	# 	groupName : string - Group name
	# 	unpaidAmount : number - Mining rig unpaid amount
	# 	notifications : [
	# 		string - Mining rig notification settings - UNKNOWN, RIG_OFFLINE, RIG_ERROR, UNRECOGNIZED
	# 	]
	# 	softwareVersions : string - Software versions used on rig. E.g.: NHM3_WIN/3.0.0["5"]EXCAVATOR/1.5["13a"]XMR-STAK/2.5.1
	# 	devices : [
	# 		{
	# 			id : string - MiningDevice id
	# 			name : string - MiningDevice name
	# 			deviceType : {
	# 				enumName : string - Name - UNKNOWN, NVIDIA, AMD, CPU
	# 				description : string - Translated description
	# 			}
	# 			status : {
	# 				enumName : string - Name - UNKNOWN, DISABLED, INACTIVE, MINING, BENCHMARKING, ERROR, PENDING, OFFLINE
	# 				description : string - Translated description
	# 			}
	# 			temperature : number - Current temperature of mining device
	# 			load : number - Load of mining device (in %)
	# 			revolutionsPerMinute : number - Mining device fan RPM
	# 			revolutionsPerMinutePercentage : number - Mining device fan speed percentage
	# 			powerMode : {
	# 				enumName : string - Name - UNKNOWN, LOW, MEDIUM, HIGH, MIXED
	# 				description : string - Translated description
	# 			}
	# 			powerUsage : number - Mining device power usage
	# 			speeds : [
	# 				{
	# 					algorithm : string - Algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 					title : string - Title
	# 					speed : number - Mining algorithm speed
	# 					displaySuffix : string - Display suffix
	# 				}
	# 			]
	# 			intensity : {
	# 				enumName : string - Name - UNKNOWN, LOW, HIGH
	# 				description : string - Translated description
	# 			}
	# 			nhqm : string - NHQM string
	# 		}
	# 	]
	# 	cpuMiningEnabled : boolean - CPU mining enabled
	# 	cpuExists : boolean - Does rig contain CPU that is able to mine
	# 	stats : [
	# 		{
	# 			statsTime : integer - Last information fetch timestamp in milliseconds since 1.1.1970
	# 			market : string - Market where the rig is mining - EU, USA, EU_N, USA_E
	# 			algorithm : {
	# 				enumName : string - Name - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 				description : string - Translated description
	# 			}
	# 			unpaidAmount : number - Unpaid amount
	# 			difficulty : number - Current rig difficulty
	# 			proxyId : integer - Id of proxy where rig is connected
	# 			timeConnected : integer - Connection timestamp in milliseconds since 1.1.1970
	# 			xnsub : boolean - Rig uses xn subscription
	# 			speedAccepted : number - Accepted speed
	# 			speedRejectedR1Target : number - Rejected speed - share above target
	# 			speedRejectedR2Stale : number - Rejected speed - stale shares
	# 			speedRejectedR3Duplicate : number - Rejected speed - duplicate jobs
	# 			speedRejectedR4NTime : number - Rejected speed - incorrect ntime
	# 			speedRejectedR5Other : number - Rejected speed - other reasons
	# 			speedRejectedTotal : number - Rejected speed - total
	# 			profitability : number - Rig profitability
	# 		}
	# 	]
	# 	profitability : number - Rig profitability
	# 	localProfitability : number - Rig local profitability
	# 	rigPowerMode : string - Devices power mode - UNKNOWN, LOW, MEDIUM, HIGH, MIXED
	# }

	# /main/api/v2/mining/rigs/activeWorkers

	@unittest.skipIf("/main/api/v2/mining/rigs/activeWorkers" not in TESTING_URIS, "skipping successful")
	def test_active_workers(self):
		check_test_paramters(["address", "page", "size", "sort_parameter", "sort_direction"])
		active_workers = self.private_api.get_active_workers(ADDRESS, size=SIZE, page=PAGE, sortParameter=SORT_PARAMETER, sortDirection=SORT_DIRECTION)
		# print(active_workers)
		self.assertIsInstance(active_workers, dict)
		self.assert_is_number(active_workers["pagination"]["size"])
		self.assert_is_number(active_workers["pagination"]["page"])
		self.assert_is_number(active_workers["pagination"]["totalPageCount"])
		self.assertIsInstance(active_workers["workers"], list)
		def test(worker):
			self.assertIsInstance(worker, dict)
			self.assert_is_number(worker["statsTime"])
			self.assertIsInstance(worker["market"], str)
			self.assertIsInstance(worker["algorithm"], dict)
			self.assertIsInstance(worker["algorithm"]["enumName"], str)
			self.assertIsInstance(worker["algorithm"]["description"], str)
			self.assert_is_number(worker["unpaidAmount"])
			self.assert_is_number(worker["difficulty"])
			self.assert_is_number(worker["proxyId"])
			self.assert_is_number(worker["timeConnected"])
			self.assertIsInstance(worker["xnsub"], bool)
			self.assert_is_number(worker["speedAccepted"])
			self.assert_is_number(worker["speedRejectedR1Target"])
			self.assert_is_number(worker["speedRejectedR2Stale"])
			self.assert_is_number(worker["speedRejectedR3Duplicate"])
			self.assert_is_number(worker["speedRejectedR4NTime"])
			self.assert_is_number(worker["speedRejectedR5Other"])
			self.assert_is_number(worker["speedRejectedTotal"])
			self.assert_is_number(worker["profitability"])
			self.assertIsInstance(worker["rigName"], str)
		if TEST_LISTS:
			for worker in active_workers["workers"]:
				test(worker)
		elif len(active_workers["workers"]) > 0:
			test(active_workers["workers"][0])
		else: raise Exception("Empty return data for testing; missing active workers")
	# {
	# 	pagination : {
	# 		size : integer - Page size
	# 		page : integer - Page number (first page is 0)
	# 		totalPageCount : integer - Total page count
	# 	}
	# 	workers : [
	# 		{
	# 			statsTime : integer - Last information fetch timestamp in milliseconds since 1.1.1970
	# 			market : string - Market where the rig is mining - EU, USA, EU_N, USA_E
	# 			algorithm : {
	# 				enumName : string - Name - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 				description : string - Translated description
	# 			}
	# 			unpaidAmount : number - Unpaid amount
	# 			difficulty : number - Current rig difficulty
	# 			proxyId : integer - Id of proxy where rig is connected
	# 			timeConnected : integer - Connection timestamp in milliseconds since 1.1.1970
	# 			xnsub : boolean - Rig uses xn subscription
	# 			speedAccepted : number - Accepted speed
	# 			speedRejectedR1Target : number - Rejected speed - share above target
	# 			speedRejectedR2Stale : number - Rejected speed - stale shares
	# 			speedRejectedR3Duplicate : number - Rejected speed - duplicate jobs
	# 			speedRejectedR4NTime : number - Rejected speed - incorrect ntime
	# 			speedRejectedR5Other : number - Rejected speed - other reasons
	# 			speedRejectedTotal : number - Rejected speed - total
	# 			profitability : number - Rig profitability
	# 			rigName : string - Rig name
	# 		}
	# 	]
	# }

	# /main/api/v2/mining/rigs/payouts

	@unittest.skipIf("/main/api/v2/mining/rigs/payouts" not in TESTING_URIS, "skipping successful")
	def test_payouts(self):
		payouts = self.private_api.get_payouts()
		# print(payouts)
		self.assertIsInstance(payouts, dict)
		self.assertIsInstance(payouts["list"], list)
		def test(payout):
			self.assertIsInstance(payout, dict)
			self.assertIsInstance(payout["id"], str)
			self.assert_is_number(payout["created"])
			self.assertIsInstance(payout["currency"], dict)
			self.assertIsInstance(payout["currency"]["enumName"], str)
			self.assertIsInstance(payout["currency"]["description"], str)
			self.assert_is_number(payout["amount"])
			self.assertIsInstance(payout["metadata"], str)
			self.assertIsInstance(payout["accountType"], dict)
			self.assertIsInstance(payout["accountType"]["enumName"], str)
			self.assertIsInstance(payout["accountType"]["description"], str)
			self.assert_is_number(payout["feeAmount"])
			self.assertIsInstance(payout["feeMetadata"], str)
		if TEST_LISTS:
			for payout in payouts["list"]:
				test(payout)
		elif len(payouts["list"]) > 0:
			test(payouts["list"][0])
		else: raise Exception("Empty return data for testing; missing payouts")
	# {
	# 	list : [
	# 		{
	# 			id : string - Id of the transaction
	# 			created : integer - Transaction creation timestamp in milliseconds since 1.1.1970
	# 			currency : {
	# 				enumName : string - Name - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 				description : string - Translated description
	# 			}
	# 			amount : number - Transaction amount
	# 			metadata : string - Transation metadata
	# 			accountType : {
	# 				enumName : string - Name - USER, USER_EXCHANGE_PENDING, USER_WITHDRAWAL_PENDING, USER_DEBT, EXCHANGE_FEE, HASHPOWER_ORDERS, HASHPOWER_PAYOUTS, HASHPOWER_ORDER_FEE, HASHPOWER_PAYOUT_FEE, WALLET_BITGO_BLOCKCHAIN, WALLET_BITGO_DEPOSIT_PENDING, WALLET_BITGO_DEPOSIT_CONFIRMED, WALLET_BITGO_DEPOSITS_FEES, WALLET_BITGO_DEPOSIT_CONFISCATED, WALLET_BITGO_DEPOSIT_UNASSIGNED, WALLET_BITGO_WITHDRAWAL_PENDING, WALLET_BITGO_WITHDRAWAL_CONFIRMED, WALLET_BITGO_WITHDRAWALS_FEES, WALLET_COINBASE_BLOCKCHAIN, WALLET_COINBASE_WITHDRAWAL_PENDING, WALLET_COINBASE_WITHDRAWALS_FEES, WALLET_COINBASE_DEPOSIT_PENDING, WALLET_COINBASE_DEPOSIT_CONFIRMED, WALLET_COINBASE_DEPOSIT_UNASSIGNED, WALLET_PAYEER_WITHDRAWAL_PENDING, WALLET_PAYEER_WITHDRAWALS_FEES, TESTING, WALLET_BITGO_WITHDRAWAL_UNASSIGNED, WALLET_KRIPTOMAT_DEPOSIT_UNASSIGNED, WALLET_KRIPTOMAT_DEPOSIT_FEES, WALLET_KRIPTOMAT_WITHDRAWAL_PENDING, WALLET_KRIPTOMAT_WITHDRAWAL_FEES, WALLET_BLOCKCHAIN_DEPOSIT_PENDING, WALLET_BLOCKCHAIN_DEPOSITS_FEES, WALLET_BLOCKCHAIN_DEPOSIT_UNASSIGNED, WALLET_BLOCKCHAIN_WITHDRAWAL_PENDING, WALLET_BLOCKCHAIN_WITHDRAWALS_FEES, WALLET_LIGHTNING_DEPOSIT_UNASSIGNED, WALLET_LIGHTNING_WITHDRAWAL_PENDING, WALLET_LIGHTNING_WITHDRAWALS_FEES, WALLET_LIGHTNING_DEPOSITS_FEES, WALLET_MULTISIG_DEPOSIT_UNASSIGNED, WALLET_MULTISIG_DEPOSITS_FEES, WALLET_MULTISIG_WITHDRAWALS_FEES, TOKEN_WITHDRAWAL_FEE_PENDING, WALLET_MULTISIG_DEPOSIT_FEES, CHARITY, HASHPOWER_ORDERS_PENDING, USER_FEE, USER_MNG_FEE, USER_EX_FEE
	# 				description : string - Translated description
	# 			}
	# 			feeAmount : number - Fee amount
	# 			feeMetadata : string - Fee metadata
	# 		}
	# 	]
	# 	pagination : {
	# 		size : integer - Page size
	# 		page : integer - Page number (first page is 0)
	# 		totalPageCount : integer - Total page count
	# 	}
	# }

	# /main/api/v2/mining/rigs/stats/algo

	@unittest.skipIf("/main/api/v2/mining/rigs/stats/algo" not in TESTING_URIS, "skipping successful")
	def test_algo_statistics(self):
		check_test_paramters(["algorithm_codes", "algorithm_code"])
		if TEST_LISTS:
			for algorithm in ALGORITHM_CODES:
				algo_statistics = self.private_api.get_algo_statistics(algorithm)
		else:
			algo_statistics = self.private_api.get_algo_statistics(ALGORITHM_CODE)
		# print(algo_statistics)
		
		def test(col):
			self.assertIsInstance(col, str)
		if TEST_LISTS:
			for col in algo_statistics["columns"]:
				test(col)
		elif len(algo_statistics["columns"]) > 0:
			test(algo_statistics["columns"][0])
		else: raise Exception("Empty return data for testing; missing algo statistics columns")
		def test2(data):
			self.assertIsInstance(data, list)
			def test3(stat):
				self.assertIsInstance(stat, dict)
			if TEST_LISTS:
				for stat in data:
					test3(stat)
			elif len(data) > 0:
				test3(data[0])
		if TEST_LISTS:
			for data in algo_statistics["data"]:
				test2(data)
		elif len(algo_statistics["data"]) > 0:
			test2(algo_statistics["data"][0])
		else: raise Exception("Empty return data for testing; missing algo statistics data")
	# {
	# 	columns : [
	# 		string - Column definition of statistical streams
	# 	]
	# 	data : [
	# 		[
	# 			object - Statistical data
	# 		]
	# 	]
	# }

	# /main/api/v2/mining/rigs/stats/unpaid

	@unittest.skipIf("/main/api/v2/mining/rigs/stats/unpaid" not in TESTING_URIS, "skipping successful")
	def test_unpaid_statistics(self):
		unpaid_statistics = self.private_api.get_unpaid_statistics()
		# print(unpaid_statistics)
		self.assertIsInstance(unpaid_statistics, dict)
		def test(col):
			self.assertIsInstance(col, str)
		if TEST_LISTS:
			for col in unpaid_statistics["columns"]:
				test(col)
		elif len(unpaid_statistics["columns"]) > 0:
			test(unpaid_statistics["columns"][0])
		else: raise Exception("Empty return data for testing; missing unpaid rig statistics columns")
		def test2(data):
			self.assertIsInstance(data, list)
			def test3(stat):
				self.assertIsInstance(stat, dict)
			if TEST_LISTS:
				for stat in data:
					test3(stat)
			elif len(data) > 0:
				test3(data[0])
		if TEST_LISTS:
			for data in unpaid_statistics["data"]:
				test2(data)
		elif len(unpaid_statistics["data"]) > 0:
			test2(unpaid_statistics["data"][0]) 
		else: raise Exception("Empty return data for testing; missing unpaid rig statistics data")
	# {
	# 	columns : [
	# 		string - Column definition of statistical streams
	# 	]
	# 	data : [
	# 		[
	# 			object - Statistical data
	# 		]
	# 	]
	# }

	# /main/api/v2/mining/rigs/status2

	@unittest.skipIf("/main/api/v2/mining/rigs/status2" not in TESTING_URIS, "skipping successful")
	def test_status(self):
		check_test_paramters(["rig_id"])
		status = self.private_api.update_status(RIG_ACTION, rig_id=RIG_ID)
		# print(status)
		self.assertIsInstance(status, dict)
		self.assertIsInstance(status["success"], bool)
		self.assertIsInstance(status["successType"], str)
		self.assertIsInstance(status["message"], str)

	@unittest.skipIf("/main/api/v2/mining/rigs/status2" not in TESTING_URIS, "skipping successful")
	def test_status2(self):
		if not RIG_ACTION or RIG_GROUP_NAME: return
		status = self.private_api.update_status(RIG_ACTION, group_name=RIG_GROUP_NAME)
		# print(status)
		self.assertIsInstance(status, dict)
		self.assertIsInstance(status["success"], bool)
		self.assertIsInstance(status["successType"], str)
		self.assertIsInstance(status["message"], str)
	# {
	# 	success : boolean
	# 	successType : string - SUCCESSFUL, PARTIAL_SUCCESS, NOT_SUCCESSFUL
	# 	message : string
	# }

	# /main/api/v2/mining/rigs2

	@unittest.skipIf("/main/api/v2/mining/rigs2" not in TESTING_URIS, "skipping successful")
	def test_rigs(self):
		rigs = self.private_api.get_rigs()
		# print(rigs)
		self.assertIsInstance(rigs, dict)
		def test(address):
			self.assertIsInstance(address, str)
		for address in rigs.keys():
			test(address)
			if not TEST_LISTS: break
	# {
	# 	address : string - BTC mining address
	# }

	# Pools

	# /main/api/v2/pool

	@unittest.skipIf("/main/api/v2/pool" not in TESTING_URIS, "skipping successful")
	def test_create_pool(self):
		check_test_paramters(["algorithm", "pool_host", "pool_name", "pool_port", "pool_password", "pool_username"])
		pool = self.private_api.create_pool(POOL_NAME, ALGORITHM, pool_host=POOL_HOST, pool_port=POOL_PORT, username=POOL_USERNAME, password=POOL_PASSWORD)
		# print(pool)
		self.assertIsInstance(pool, dict)
		self.assertIsInstance(pool["id"], bool)
		self.assertIsInstance(pool["name"], str)
		self.assertIsInstance(pool["algorithm"], str)
		self.assertIsInstance(pool["stratumHostname"], str)
		self.assert_is_number(pool["stratumPort"])
		self.assertIsInstance(pool["username"], str)
		self.assertIsInstance(pool["password"], str)
		self.assertIsInstance(pool["status"], str)
		self.assertIsInstance(pool["updatedTs"], str)
		self.assertIsInstance(pool["inMoratorium"], bool)
	# {
	# 	id : string - Pool id (When creating new pool this value should not be set.)
	# 	name : string - Pool custom name
	# 	algorithm : string - Pool algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 	stratumHostname : string - Hostname or ip of the pool
	# 	stratumPort : integer - Port of the pool
	# 	username : string - Username
	# 	password : string - Password (Set password to # when using ethproxy pool.)
	# 	status : string - Verification status - VERIFIED, NOT_VERIFIED
	# 	updatedTs : string
	# 	inMoratorium : boolean
	# }

	# /main/api/v2/pool/{poolId}

	@unittest.skipIf("/main/api/v2/pool/{poolId}" not in TESTING_URIS, "skipping successful")
	def test_pool(self):
		check_test_paramters(["pool_id"])
		pool = self.private_api.get_pool(POOL_ID)
		# print(pool)
		self.assertIsInstance(pool, dict)
		self.assertIsInstance(pool["id"], bool)
		self.assertIsInstance(pool["name"], str)
		self.assertIsInstance(pool["algorithm"], str)
		self.assertIsInstance(pool["stratumHostname"], str)
		self.assert_is_number(pool["stratumPort"])
		self.assertIsInstance(pool["username"], str)
		self.assertIsInstance(pool["password"], str)
		self.assertIsInstance(pool["status"], str)
		self.assertIsInstance(pool["updatedTs"], str)
		self.assertIsInstance(pool["inMoratorium"], bool)
	# {
	# 	id : string - Pool id (When creating new pool this value should not be set.)
	# 	name : string - Pool custom name
	# 	algorithm : string - Pool algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 	stratumHostname : string - Hostname or ip of the pool
	# 	stratumPort : integer - Port of the pool
	# 	username : string - Username
	# 	password : string - Password (Set password to # when using ethproxy pool.)
	# 	status : string - Verification status - VERIFIED, NOT_VERIFIED
	# 	updatedTs : string
	# 	inMoratorium : boolean
	# }

	# /main/api/v2/pool/{poolId}

	@unittest.skipIf("/main/api/v2/pool/{poolId}" not in TESTING_URIS, "skipping successful")
	def test_delete_pool(self):
		check_test_paramters(["pool_id"])
		delete_pool = self.private_api.delete_pool(POOL_ID)
		# print(delete_pool)
		self.assertIsInstance(delete_pool, dict)
		self.assertIsInstance(delete_pool["success"], bool)
		self.assertIsInstance(delete_pool["successType"], str)
		self.assertIsInstance(delete_pool["message"], str)
	# {
	# 	success : boolean
	# 	successType : string - SUCCESSFUL, PARTIAL_SUCCESS, NOT_SUCCESSFUL
	# 	message : string
	# }

	# /main/api/v2/pools

	@unittest.skipIf("/main/api/v2/pools" not in TESTING_URIS, "skipping successful")
	def test_my_pools(self):
		my_pools = self.private_api.get_my_pools()
		# print(my_pools)
		self.assertIsInstance(my_pools, dict)
		self.assertIsInstance(my_pools["list"], list)
		def test(pool):
			self.assertIsInstance(pool, dict)
			self.assertIsInstance(pool["id"], str)
			self.assertIsInstance(pool["algorithm"], str)
			self.assertIsInstance(pool["stratumHostname"], str)
			self.assert_is_number(pool["stratumPort"])
			self.assertIsInstance(pool["username"], str)
			self.assertIsInstance(pool["password"], str)
			self.assertIsInstance(pool["status"], str)
			self.assertIsInstance(pool["updatedTs"], str)
			self.assertIsInstance(pool["inMoratorium"], bool)
		if TEST_LISTS:
			for pool in my_pools["list"]:
				test(pool)
		elif len(my_pools["list"]) > 0:
			test(my_pools["list"][0])
		else: raise Exception("Empty return data for testing; missing pools list")
		try:
			self.assertIsInstance(my_pools["pagination"], dict)
			self.assert_is_number(my_pools["pagination"]["size"])
			self.assert_is_number(my_pools["pagination"]["page"])
			self.assert_is_number(my_pools["pagination"]["totalPageCount"])
		except KeyError: pass
	# {
	# 	list : [
	# 		{
	# 			id : string - Pool id (When creating new pool this value should not be set.)
	# 			name : string - Pool custom name
	# 			algorithm : string - Pool algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 			stratumHostname : string - Hostname or ip of the pool
	# 			stratumPort : integer - Port of the pool
	# 			username : string - Username
	# 			password : string - Password (Set password to # when using ethproxy pool.)
	# 			status : string - Verification status - VERIFIED, NOT_VERIFIED
	# 			updatedTs : string
	# 			inMoratorium : boolean
	# 		}
	# 	]
	# 	pagination : {
	# 		size : integer - Page size
	# 		page : integer - Page number (first page is 0)
	# 		totalPageCount : integer - Total page count
	# 	}
	# }

	# /main/api/v2/pools/verify

	@unittest.skipIf("/main/api/v2/pools/verify" not in TESTING_URIS, "skipping successful")
	def test_verify_pools(self):
		check_test_paramters(["algorithm", "market_long", "pool_host", "pool_port", "pool_password", "pool_username"])
		verify_pools = self.private_api.verify_pool(market=MARKET_LONG, algorithm=ALGORITHM, pool_host=POOL_HOST, pool_port=POOL_PORT, username=POOL_USERNAME, password=POOL_PASSWORD)
		# print(verify_pools)
		self.assertIsInstance(verify_pools, dict)
		self.assertIsInstance(verify_pools["success"], bool)
		self.assertIsInstance(verify_pools["logs"], list)
		def test(log):
			self.assertIsInstance(log, dict)
			self.assertIsInstance(pool["timestamp"], str)
			self.assertIsInstance(pool["level"], str)
			self.assertIsInstance(pool["poolVerificationMessage"], str)
			self.assertIsInstance(pool["params"], str)
			self.assertIsInstance(pool["message"], str)
		if TEST_LISTS:
			for log in verify_pools["logs"]:
				test(log)
		elif len(verify_pools["logs"]) > 0:
			test(verify_pools["logs"][0])
		else: raise Exception("Empty return data for testing; missing pools logs")
		self.assert_is_number(verify_pools["highestDifficulty"])
		self.assertIsInstance(verify_pools["highestDifficultyFormatted"], str)
		self.assertIsInstance(verify_pools["difficultyCorrect"], bool)
	# {
	# 	success : boolean - Pool verification status
	# 	logs : [
	# 		{
	# 			timestamp : string - Timestamp
	# 			level : string - Level - INFO, WARNING, SEVERE
	# 			poolVerificationMessage : string - Pool verification message - INVALID_PORT_NUMBER, INVALID_HOST, NICEHASH_HOSTS_NOT_ALLOWED, INVALID_USERNAME, INVALID_PASSWORD, BLACKLISTED_POOL_HOST, POOL_HOST_SHOULD_NOT_INCLUDE_COLON, POOL_HOST_RESOLVED_TO_IP, POOL_HOST_CANNOT_BE_RESOLVED_TO_IP, CONNECTING_TO_STRATUM_PROXY_FOR_REGION, SELECTED_MINING_ALGORITHM, SELECTED_MINING_ALGORITHM_WITH_WARNING, UNKNOWN_PROXY_ERROR, PROXY_CONNECTION_REFUSED, SENDING_LOGIN_INFORMATION, RECEIVED_NO_RESPONSE_ON_LOGIN, UNKNOWN_MESSAGE, SENDING_MINING_SUBSCRIBE_REQUEST, SENDING_ETH_GET_WORK, RECEIVED_NO_RESPONSE, MINING_SUBSCRIBE_REQUEST_SUCCESSFUL, AUTHORIZATION_FAILED_WRONG_USERNAME_OR_PASSWORD, RECEIVED_MINING_SET_TARGET, RECEIVED_MINING_SET_DIFFICULTY, POOL_DIFFICULTY_TOO_LOW, POOL_EXTRANONCE_TOO_HIGH, POOL_EXTRANONCE_AND_EXTRANONCE2_TOO_HIGH, POOL_EXTRANONCE2_TOO_LOW, POOL_DIFFICULTY_CORRECT, QUESTIONABLE_STRATUM_VERSION, SENDING_MINING_CONFIG, RECEIVED_NO_RESPONSE_ON_MINING_CONFIG, FAILED_TO_PARSE_ROLING_VERSION, SENDING_GRIN_GET_WORK, FAILED_TO_PARSE_WORK, FAILED_TO_PARSE_DIFFICULTY, INVALID_JOB_BLOB_LENGTH, INVALID_POOL_EXTRANONCE, INVALID_MINING_SUBSCRIBE_RESPONSE, INVALID_LOGIN_RESPONSE, INVALID_WORK_RESPONSE
	# 			params : {
	# 				string - Map of Pool verification params with status
	# 			}
	# 			message : string - Message
	# 		}
	# 	]
	# 	highestDifficulty : number - Highest difficulty set by pool
	# 	highestDifficultyFormatted : string - Highest difficulty set by pool formatted
	# 	difficultyCorrect : boolean - Is pool difficulty correct
	# }


	# Exchange private

	# /exchange/api/v2/info/cancelAllOrders

	@unittest.skipIf("/exchange/api/v2/info/cancelAllOrders" not in TESTING_URIS, "skipping successful")
	def test_canceled_orders(self):
		check_test_paramters(["market_symbol", "side"])
		canceled_orders = self.private_api.cancel_all_orders(market=MARKET_SYMBOL, side=SIDE)
		# print(order)
		self.assertIsInstance(canceled_orders, list)
		def test(order):
			self.assertIsInstance(order, dict)
			self.assertIsInstance(order["market"], str)
			self.assertIsInstance(order["orderId"], str)
			self.assertIsInstance(order["owner"], str)
			self.assert_is_number(order["price"])
			self.assert_is_number(order["origQty"])
			self.assert_is_number(order["origSndQty"])
			self.assert_is_number(order["executedQty"])
			self.assertIsInstance(order["type"], str)
			self.assertIsInstance(order["side"], str)
			self.assert_is_number(order["submitTime"])
			self.assert_is_number(order["lastResponseTime"])
			self.assertIsInstance(order["state"], str)
		if TEST_LISTS:
			for order in canceled_orders:
				test(order)
		elif len(canceled_orders) > 0:
			test(canceled_orders[0])
		else: raise Exception("Empty return data for testing; missing canceled orders")
	# {
	# 	market : string - Market symbol - ETHBTC, BTCUSDT, BCHBTC, ...
	# 	orderId : string - Order Id
	# 	owner : string - Organisation Id
	# 	price : number - Order price
	# 	origQty : number - Base quantity in order
	# 	origSndQty : number - Quote quantity in order
	# 	executedQty : number - Executed base quantity in order
	# 	executedSndQty : number - Executed quote quantity in order
	# 	type : string - Order type - LIMIT, MARKET
	# 	side : string - Order side or direction - BUY, SELL
	# 	submitTime : integer - Order submission timestamp in microsecond since 1.1.1970
	# 	lastResponseTime : integer - The response time of order's last response in microsecond since 1.1.1970
	# 	state : string - State of the order - CREATED, RESERVED, RESERVED_ERROR, INSERTED, INSERTED_ERROR, RELEASED, RELEASED_ERROR, PARTIAL, ENTERED, FULL, PROCESSED_ERROR, CANCEL_REQUEST, CANCELLED, CANCELLED_ERROR, REJECTED
	# }

	# /exchange/api/v2/info/fees/status

	@unittest.skipIf("/exchange/api/v2/info/fees/status" not in TESTING_URIS, "skipping successful")
	def test_fee_status(self):
		fee_status = self.private_api.get_fee_status()
		# print(fee_status)
		self.assertIsInstance(fee_status, dict)
		self.assert_is_number(fee_status["makerCoefficient"])
		self.assert_is_number(fee_status["takerCoefficient"])
		self.assert_is_number(fee_status["sum"])
		self.assertIsInstance(fee_status["makerLimits"], dict)
		self.assertIsInstance(fee_status["takerLimits"], dict)
		self.assertIsInstance(fee_status["currency"], str)
	# {
	# 	makerCoefficient : number - Maker exchange fee coefficient
	# 	takerCoefficient : number - Taker exchange fee coefficient
	# 	sum : number - The total trade amount of the user (buy + sell)
	# 	makerLimits : {
	# 		number - Maker fee limits list
	# 	}
	# 	takerLimits : {
	# 		number - Taker fee limits list
	# 	}
	# 	currency : string - The currency in which the total fee amount is calculated
	# }

	# /exchange/api/v2/info/myOrder

	def assert_is_order_response_response(self, order):
		self.assertIsInstance(order, dict)
		self.assertIsInstance(order["market"], str)
		self.assertIsInstance(order["orderId"], str)
		self.assertIsInstance(order["owner"], str)
		self.assert_is_number(order["price"])
		self.assert_is_number(order["origQty"])
		self.assert_is_number(order["origSndQty"])
		self.assert_is_number(order["executedQty"])
		self.assert_is_number(order["executedSndQty"])
		self.assertIsInstance(order["type"], str)
		self.assertIsInstance(order["side"], str)
		self.assert_is_number(order["submitTime"])
		self.assert_is_number(order["lastResponseTime"])
		self.assertIsInstance(order["state"], str)

	@unittest.skipIf("/exchange/api/v2/info/myOrder" not in TESTING_URIS, "skipping successful")
	def test_my_order(self):
		check_test_paramters(["order_id", "market_symbol"])
		order = self.private_api.get_my_order(MARKET_SYMBOL, ORDER_ID)
		print(order)
		self.assert_is_order_response_response(order)
		# self.assertIsInstance(order, dict)
		# self.assertIsInstance(order["market"], str)
		# self.assertIsInstance(order["orderId"], str)
		# self.assertIsInstance(order["owner"], str)
		# self.assert_is_number(order["price"])
		# self.assert_is_number(order["origQty"])
		# self.assert_is_number(order["origSndQty"])
		# self.assert_is_number(order["executedQty"])
		# self.assert_is_number(order["executedSndQty"])
		# self.assertIsInstance(order["type"], str)
		# self.assertIsInstance(order["side"], str)
		# self.assert_is_number(order["submitTime"])
		# self.assert_is_number(order["lastResponseTime"])
		# self.assertIsInstance(order["state"], str)
	# {
	# 	market : string - Market symbol - ETHBTC, BTCUSDT, BCHBTC, ...
	# 	orderId : string - Order Id
	# 	owner : string - Organisation Id
	# 	price : number - Order price
	# 	origQty : number - Base quantity in order
	# 	origSndQty : number - Quote quantity in order
	# 	executedQty : number - Executed base quantity in order
	# 	executedSndQty : number - Executed quote quantity in order
	# 	type : string - Order type - LIMIT, MARKET
	# 	side : string - Order side or direction - BUY, SELL
	# 	submitTime : integer - Order submission timestamp in microsecond since 1.1.1970
	# 	lastResponseTime : integer - The response time of order's last response in microsecond since 1.1.1970
	# 	state : string - State of the order - CREATED, RESERVED, RESERVED_ERROR, INSERTED, INSERTED_ERROR, RELEASED, RELEASED_ERROR, PARTIAL, ENTERED, FULL, PROCESSED_ERROR, CANCEL_REQUEST, CANCELLED, CANCELLED_ERROR, REJECTED
	# }


	# /exchange/api/v2/info/myOrders

	@unittest.skipIf("/exchange/api/v2/info/myOrders" not in TESTING_URIS, "skipping successful")
	@unittest.expectedFailure
	def test_my_orders(self):
		check_test_paramters(["market_symbol"])
		orders = self.private_api.get_my_orders(MARKET_SYMBOL)
		print(orders)
		self.assertIsInstance(orders, list)
		if len(orders) == 0:
			raise Exception("Empty return data for testing; must create orders to check")
		def test(order):
			self.assert_is_order_response_response(order)
		if TEST_LISTS:
			for order in orders:
				test(order)
		elif len(orders) > 0:
			test(orders[0])
		else: raise Exception("Empty return data for testing; missing orders")
	# [
	# 	{
	# 		market : string - Market symbol - ETHBTC, BTCUSDT, BCHBTC, ...
	# 		orderId : string - Order Id
	# 		owner : string - Organisation Id
	# 		price : number - Order price
	# 		origQty : number - Base quantity in order
	# 		origSndQty : number - Quote quantity in order
	# 		executedQty : number - Executed base quantity in order
	# 		executedSndQty : number - Executed quote quantity in order
	# 		type : string - Order type - LIMIT, MARKET
	# 		side : string - Order side or direction - BUY, SELL
	# 		submitTime : integer - Order submission timestamp in microsecond since 1.1.1970
	# 		lastResponseTime : integer - The response time of order's last response in microsecond since 1.1.1970
	# 		state : string - State of the order - CREATED, RESERVED, RESERVED_ERROR, INSERTED, INSERTED_ERROR, RELEASED, RELEASED_ERROR, PARTIAL, ENTERED, FULL, PROCESSED_ERROR, CANCEL_REQUEST, CANCELLED, CANCELLED_ERROR, REJECTED
	# 	}
	# ]

	# /exchange/api/v2/info/myTrades

	def assert_is_trade_response(self, trade):
		self.assertIsInstance(trade, dict)
		self.assertIsInstance(trade["id"], str)
		self.assertIsInstance(trade["dir"], str)
		self.assert_is_number(trade["price"])
		self.assert_is_number(trade["qty"])
		self.assert_is_number(trade["sndQty"])
		self.assert_is_number(trade["time"])
		self.assertIsInstance(trade["fee"], dict)
		self.assert_is_number(trade["isMaker"])
		self.assertIsInstance(trade["orderId"], str)

	@unittest.skipIf("/exchange/api/v2/info/myTrades" not in TESTING_URIS, "skipping successful")
	@unittest.expectedFailure
	def test_my_trades(self):
		check_test_paramters(["market_symbol"])
		trades = self.private_api.get_my_trades(MARKET_SYMBOL)
		print(trades)
		self.assertIsInstance(trades, list)
		if len(orders) == 0:
			raise Exception("Empty return data for testing; must create trades to check")
		def test(trade):
			self.assert_is_trade_response(trade)
		if TEST_LISTS:
			for trade in trades:
				test(trade)
		elif len(trades) > 0:
			test(trades[0])
		else: raise Exception("Empty return data for testing; missing trades")
	# [
	# 	{
	# 		id : string - Trade id
	# 		dir : string - Trade direction - BUY, SELL
	# 		price : number - Trade price
	# 		qty : number - Base volume of the trade
	# 		sndQty : number - Quote volume of the trade
	# 		time : integer - Timestamp in microseconds since 1.1.1970
	# 		fee : object - Fee payed for this trade. This field is only included in private response.
	# 		isMaker : integer - Is maker trade. This field is only included in private response.
	# 		orderId : string - Order id of the trade.
	# 	}
	# ]

	# /exchange/api/v2/info/orderTrades

	@unittest.skipIf("/exchange/api/v2/info/orderTrades" not in TESTING_URIS, "skipping successful")
	def test_trades_for_order(self):
		check_test_paramters(["order_id", "market_symbol"])
		order_trades = self.private_api.get_trades_for_order(MARKET_SYMBOL, ORDER_ID)
		# print(order_trades)
		self.assertIsInstance(order_trades, list)
		def test(trade):
			self.assert_is_trade_response(trade)
		if TEST_LISTS:
			for trade in order_trades:
				test(trade)
		elif len(order_trades) > 0:
			test(order_trades[0])
		else: raise Exception("Empty return data for testing; missing order trades")
	# [
	# 	{
	# 		id : string - Trade id
	# 		dir : string - Trade direction - BUY, SELL
	# 		price : number - Trade price
	# 		qty : number - Base volume of the trade
	# 		sndQty : number - Quote volume of the trade
	# 		time : integer - Timestamp in microseconds since 1.1.1970
	# 		fee : object - Fee payed for this trade. This field is only included in private response.
	# 		isMaker : integer - Is maker trade. This field is only included in private response.
	# 		orderId : string - Order id of the trade.
	# 	}
	# ]

	# /exchange/api/v2/order

	@unittest.skipIf("/exchange/api/v2/order" not in TESTING_URIS, "skipping successful")
	@unittest.expectedFailure
	# TODO
	# requires testing behind VPN
	def test_create_exchange_limit_order(self):
		check_test_paramters(["market_symbol", "price", "quantity", "side"])
		exchange_limit_order = self.private_api.create_exchange_limit_order(MARKET_SYMBOL, SIDE, QUANTITY, PRICE)
		# print(exchange_limit_order)
		self.assert_is_order_response_response(exchange_limit_order)  

	@unittest.skipIf("/exchange/api/v2/order" not in TESTING_URIS, "skipping successful")
	@unittest.expectedFailure
	def test_create_exchange_buy_market_order(self):
		check_test_paramters(["market_symbol", "quantity", "sec_quantity"])
		exchange_buy_market_order = self.private_api.create_exchange_buy_market_order(MARKET_SYMBOL, QUANTITY, SEC_QUANTITY)
		# print(exchange_buy_market_order)
		self.assert_is_order_response_response(exchange_buy_market_order)  

	@unittest.skipIf("/exchange/api/v2/order" not in TESTING_URIS, "skipping successful")
	@unittest.expectedFailure
	def test_create_exchange_sell_market_order(self):
		check_test_paramters(["market_symbol", "quantity", "min_sec_quantity"])
		exchange_sell_market_order = self.private_api.create_exchange_sell_market_order(MARKET_SYMBOL, QUANTITY, min_SEC_QUANTITY)
		# print(exchange_sell_market_order)
		self.assert_is_order_response_response(exchange_sell_market_order)  
	# {
	# 	market : string - Market symbol - ETHBTC, BTCUSDT, BCHBTC, ...
	# 	orderId : string - Order Id
	# 	owner : string - Organisation Id
	# 	price : number - Order price
	# 	origQty : number - Base quantity in order
	# 	origSndQty : number - Quote quantity in order
	# 	executedQty : number - Executed base quantity in order
	# 	executedSndQty : number - Executed quote quantity in order
	# 	type : string - Order type - LIMIT, MARKET
	# 	side : string - Order side or direction - BUY, SELL
	# 	submitTime : integer - Order submission timestamp in microsecond since 1.1.1970
	# 	lastResponseTime : integer - The response time of order's last response in microsecond since 1.1.1970
	# 	state : string - State of the order - CREATED, RESERVED, RESERVED_ERROR, INSERTED, INSERTED_ERROR, RELEASED, RELEASED_ERROR, PARTIAL, ENTERED, FULL, PROCESSED_ERROR, CANCEL_REQUEST, CANCELLED, CANCELLED_ERROR, REJECTED
	# }

	# /exchange/api/v2/order

	@unittest.skipIf("/exchange/api/v2/order" not in TESTING_URIS, "skipping successful")
	def test_cancel_exchange_order(self):
		check_test_paramters(["market_symbol", "order_id"])
		canceled_order = self.private_api.cancel_exchange_order(MARKET_SYMBOL, ORDER_ID)
		# print(canceled_order)
		self.assert_is_order_response_response(canceled_order)  
	# {
	# 	market : string - Market symbol - ETHBTC, BTCUSDT, BCHBTC, ...
	# 	orderId : string - Order Id
	# 	owner : string - Organisation Id
	# 	price : number - Order price
	# 	origQty : number - Base quantity in order
	# 	origSndQty : number - Quote quantity in order
	# 	executedQty : number - Executed base quantity in order
	# 	executedSndQty : number - Executed quote quantity in order
	# 	type : string - Order type - LIMIT, MARKET
	# 	side : string - Order side or direction - BUY, SELL
	# 	submitTime : integer - Order submission timestamp in microsecond since 1.1.1970
	# 	lastResponseTime : integer - The response time of order's last response in microsecond since 1.1.1970
	# 	state : string - State of the order - CREATED, RESERVED, RESERVED_ERROR, INSERTED, INSERTED_ERROR, RELEASED, RELEASED_ERROR, PARTIAL, ENTERED, FULL, PROCESSED_ERROR, CANCEL_REQUEST, CANCELLED, CANCELLED_ERROR, REJECTED
	# }

############################################################################################

if __name__ == '__main__':
	unittest.main()
