import unittest
import os
import time
from dotenv import load_dotenv
load_dotenv()
#
from python import nicehash

ADDRESS = os.environ.get("TEST_ADDRESS")
HOST = os.environ.get("TEST_HOST")
# HOST = os.environ.get("HOST")
ORGANIZATION_ID = os.environ.get("TEST_ORGANIZATION_ID")
# ORGANIZATION_ID = os.environ.get("ORGANIZATION_ID")
KEY = os.environ.get("TEST_KEY")
# KEY = os.environ.get("KEY")
SECRET = os.environ.get("TEST_SECRET")
# SECRET = os.environ.get("SECRET")
###
# Parameters for testing
###
ACTIVITY_TYPES = nicehash.ACTIVITY_TYPES[0]
ADDRESS = None
ALGORITHM = nicehash.ALGORITHMS[0]
CURRENCY = "TBTC"
MARKET = nicehash.MARKETS[0]
RESOLUTION = nicehash.RESOLUTIONS[0]
MARKET_SYMBOLS = ["TETHTBTC", "TBTCTUSDT", "TBCHTBTC"]
MARKET_SYMBOL = MARKET_SYMBOLS[0]
OP = nicehash.OPS[0]
# ORDER_RELATION = nicehash.ORDER_RELATION[0]
SORT_PARAMETER = nicehash.SORT_PARAMETERS[0]
SORT_DIRECTION = nicehash.SORT_DIRECTIONS[0]
SORT_OPTION = nicehash.SORT_OPTIONS[0]
SIDE = nicehash.SIDES[0]
STATUS = nicehash.STATUSES[0]
# TRANSACTION_TYPE = nicehash.TX_TYPES[0]
# WALLET_TYPE = nicehash.WALLET_TYPES[0]
#
FROM_S = int(time.time()) - 300
TO_S = FROM_S
TIMESTAMP = int(time.time())
###

# test values in lists
TEST_LISTS = False

# For selectively mass testing, ignoring tests that fail because parameters don't exist with to check
TESTING_URIS = [
	"/main/api/v2/mining/external/{btcAddress}/rigs/activeWorkers",
	"/main/api/v2/mining/external/{btcAddress}/rigs/stats/algo",
	"/main/api/v2/mining/external/{btcAddress}/rigs/stats/unpaid",
	"/main/api/v2/mining/external/{btcAddress}/rigs/withdrawals",
	"/main/api/v2/mining/external/{btcAddress}/rigs2",
	"/main/api/v2/hashpower/orderBook",
	"/main/api/v2/hashpower/orders/fixedPrice",
	"/main/api/v2/hashpower/orders/summaries",
	"/main/api/v2/hashpower/orders/summary",
	"/main/api/v2/public/algo/history",
	"/main/api/v2/public/buy/info",
	"/main/api/v2/public/orders",
	"/main/api/v2/public/simplemultialgo/info",
	"/main/api/v2/public/stats/global/24h",
	"/main/api/v2/public/stats/global/current",
	"/main/api/v2/mining/algorithms",
	"/main/api/v2/public/currencies",
	"/main/api/v2/public/service/fee/info",
	"/api/v2/enum/countries",
	"/api/v2/enum/kmCountries",
	"/api/v2/enum/permissions",
	"/api/v2/enum/xchCountries",
	"/api/v2/system/flags",
	"/api/v2/time",
	"/exchange/api/v2/info/candlesticks",
	"/exchange/api/v2/info/marketStats",
	"/exchange/api/v2/info/prices",
	"/exchange/api/v2/info/status",
	"/exchange/api/v2/info/trades",
	"/exchange/api/v2/orderbook"
]
VERBOSE = True

def check_test_paramters(parameters):
	for p in parameters:
		if "algorithm_code" in str(p):
			if not MARKET_SYMBOLS or len(MARKET_SYMBOLS) == 0 or not MARKET_SYMBOL:
				raise Exception("Missing test value: {}".format(p))
		if not globals()[p.upper()]: raise Exception("Missing test value: {}".format(p))

class TestNiceHashPublic(unittest.TestCase):

	def setUp(self):
		self.public_api = nicehash.public_api(HOST, verbose=VERBOSE)

	def tearDown(self):
		self.public_api.close()

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

	def assert_is_order_response(self, order):
		# print(order)
		self.assertIsInstance(order, dict)
		self.assertIsInstance(order["id"], str)
		try:
			self.assertIsInstance(order["createdTs"], str)
		except KeyError: pass
		try:
			self.assertIsInstance(order["updatedTs"], str)
		except KeyError: pass
		try:
			self.assertIsInstance(order["requestId"], str)
		except KeyError: pass
		try:
			self.assertIsInstance(order["type"], dict)
			self.assertIsInstance(order["type"]["code"], str)
			self.assertIsInstance(order["type"]["description"], str)
		except KeyError: pass
		try:
			self.assertIsInstance(order["algorithm"], dict)
			self.assertIsInstance(order["algorithm"]["algorithm"], str)
			self.assertIsInstance(order["algorithm"]["title"], str)
			self.assertIsInstance(order["algorithm"]["enabled"], bool)
			self.assertIsInstance(order["algorithm"]["order"], int)
		except KeyError: pass
		try:
			self.assertIsInstance(order["market"], str)
		except KeyError: pass
		try:
			self.assertIsInstance(order["status"], dict)
			self.assertIsInstance(order["status"]["code"], str)
			self.assertIsInstance(order["status"]["description"], str)
		except KeyError: pass
		try:
			self.assert_is_number(order["price"])
		except KeyError: pass
		try:
			self.assert_is_number(order["limit"])
		except KeyError: pass
		try:
			self.assert_is_number(order["amount"])
		except KeyError: pass
		try:
			self.assert_is_number(order["availableAmount"])
		except KeyError: pass
		try:
			self.assert_is_number(order["payedAmount"])
		except KeyError: pass
		try:
			self.assertIsInstance(order["alive"], bool)
		except KeyError: pass
		try:
			self.assertIsInstance(order["startTs"], str)
		except KeyError: pass
		try:
			self.assertIsInstance(order["endTs"], str)
		except KeyError: pass
		try:
			self.assertIsInstance(order["pool"], dict)
			self.assertIsInstance(order["pool"]["id"], str)
			self.assertIsInstance(order["pool"]["name"], str)
			self.assertIsInstance(order["pool"]["algorithm"], str)
			self.assertIsInstance(order["pool"]["stratumHostname"], str)
			self.assertIsInstance(order["pool"]["stratumPort"], int)
			self.assertIsInstance(order["pool"]["username"], str)
			self.assertIsInstance(order["pool"]["password"], str)
			self.assertIsInstance(order["pool"]["status"], str)
			self.assertIsInstance(order["pool"]["updatedTs"], str)
			self.assertIsInstance(order["pool"]["inMoratorium"], bool)
		except KeyError: pass
		try:
			self.assertIsInstance(order["organizationId"], str)
		except KeyError: pass
		try:
			self.assertIsInstance(order["creatorUserId"], str)
		except KeyError: pass
		try:
			self.assertIsInstance(order["rigsCount"], int)
		except KeyError: pass
		try:
			self.assert_is_number(order["acceptedCurrentSpeed"])
		except KeyError: pass
		try:
			self.assert_is_number(order["miningStatus"])
		except KeyError: pass
		try:
			self.assertIsInstance(order["displayMarketFactor"], str)
		except KeyError: pass
		try:
			self.assert_is_number(order["marketFactor"])
		except KeyError: pass
		try:
			self.assertIsInstance(order["estimateDurationInSeconds"], int)
		except KeyError: pass
		try:
			self.assertIsInstance(order["bridges"], list)
			for bridge in order["bridges"]:
				self.assertIsInstance(bridge["rigsCount"], int)
				self.assert_is_number(bridge["speedAccepted"])
				self.assert_is_number(bridge["speedRewarded"])
				self.assert_is_number(bridge["difficulty"])
				self.assertIsInstance(bridge["status"], str)
		except KeyError: pass
		try:
			self.assertIsInstance(order["liquidation"], str)
		except KeyError: pass

	# External miner

	# /main/api/v2/mining/external/{btcAddress}/rigs/activeWorkers

	@unittest.skipIf("/main/api/v2/mining/external/{btcAddress}/rigs/activeWorkers" not in TESTING_URIS, "skipping successful")
	def test_active_workers(self):
		check_test_paramters(["address"])
		active_workers = self.public_api.get_active_workers(ADDRESS)
		# print(active_workers)
		self.assertIsInstance(active_workers, dict)
		self.assertIsInstance(active_workers["size"], int)
		self.assertIsInstance(active_workers["page"], int)
		self.assertIsInstance(active_workers["totalPageCount"], int)
		self.assertIsInstance(active_workers["workers"], list)
		def test(worker):
			self.assertIsInstance(worker["statsTime"], int)
			self.assertIsInstance(worker["market"], str)
			self.assertIsInstance(worker["algorithm"], dict)
			self.assertIsInstance(worker["algorithm"]["enumName"], str)
			self.assertIsInstance(worker["algorithm"]["description"], str)
			self.assert_is_number(worker["unpaidAmount"])
			self.assert_is_number(worker["difficulty"])
			self.assertIsInstance(worker["proxyId"], int)
			self.assertIsInstance(worker["timeConnected"], int)
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
		else: raise Exception("Empty return data for testing; missing workers")
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

	# /main/api/v2/mining/external/{btcAddress}/rigs/stats/algo

	@unittest.skipIf("/main/api/v2/mining/external/{btcAddress}/rigs/stats/algo" not in TESTING_URIS, "skipping successful")
	def test_algo_statistics(self):
		check_test_paramters(["address", "algorithm"])
		algo_statistics = self.public_api.get_algo_statistics(ADDRESS, ALGORITHM)
		# print(algo_statistics)
		self.assertIsInstance(algo_statistics, dict)
		def test(col):
			self.assertIsInstance(col, str)
		if TEST_LISTS:
			for col in algo_statistics["columns"]:
				test(col)
		elif len(algo_statistics["columns"]) > 0:
			test(algo_statistics["columns"][0])
		else: raise Exception("Empty return data for testing; missing algo statistics columns")
		def test2(data):
			def test3(stat):
				self.assertIsInstance(stat, dict)
			self.assertIsInstance(data, list)
			if TEST_LISTS:
				for stat in algo_statistics["data"]:
					test3(stat)
			elif len(algo_statistics["data"]) > 0:
				test3(algo_statistics["data"][0])
			else: raise Exception("Empty return data for testing; missing algo statistics data sets")
		if TEST_LISTS:
			for data in algo_statistics["data"]:
				test2(data)
		elif len(algo_statistics["data"]) > 0:
			test(algo_statistics["data"][0])
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

	# /main/api/v2/mining/external/{btcAddress}/rigs/stats/unpaid

	@unittest.skipIf("/main/api/v2/mining/external/{btcAddress}/rigs/stats/unpaid" not in TESTING_URIS, "skipping successful")
	def test_unpaid_statistics(self):
		check_test_paramters(["address"])
		unpaid_statistics = self.public_api.get_unpaid_statistics(ADDRESS)
		# print(unpaid_statistics)
		self.assertIsInstance(unpaid_statistics, dict)
		self.assertIsInstance(unpaid_statistics["columns"], list)
		def test(col):
			self.assertIsInstance(col, str)
		if TEST_LISTS:
			for col in unpaid_statistics["columns"]:
				test(col)
		elif len(unpaid_statistics["columns"]) > 0:
			test(unpaid_statistics["columns"][0])
		else: raise Exception("Empty return data for testing; missing unpaid statistics columns")
		self.assertIsInstance(unpaid_statistics["data"], list)
		def test2(data):
			self.assertIsInstance(data, list)
			def test3(stat):
				self.assertIsInstance(stat, dict)
			if TEST_LISTS:
				for stat in data:
					test3(stat)
			else:
				test3(data[0])
		if TEST_LISTS:
			for data in unpaid_statistics["data"]:
				test2(data)
		elif len(unpaid_statistics["data"]) > 0:
			test2(unpaid_statistics["data"][0])
		else: raise Exception("Empty return data for testing; missing unpaid statistics data")
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

	# /main/api/v2/mining/external/{btcAddress}/rigs/withdrawals

	@unittest.skipIf("/main/api/v2/mining/external/{btcAddress}/rigs/withdrawals" not in TESTING_URIS, "skipping successful")
	def test_withdrawals(self):
		check_test_paramters(["address"])
		withdrawals = self.public_api.get_withdrawals(ADDRESS)
		# print(withdrawals)
		self.assertIsInstance(withdrawals, dict)
		self.assertIsInstance(withdrawals["list"], list)
		def test(withdrawal):
			self.assertIsInstance(withdrawal, dict)
			self.assertIsInstance(withdrawal["id"], str)
			self.assertIsInstance(withdrawal["created"], int)
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
			for withdrawal in withdrawals["list"]:
				test(withdrawal)
		elif len(withdrawals["list"]) > 0:
			test(withdrawals["list"][0])
		else: raise Exception("Empty return data for testing; missing withdrawals")
		self.assertIsInstance(withdrawals["pagination"], dict)
		self.assertIsInstance(withdrawals["pagination"]["size"], int)
		self.assertIsInstance(withdrawals["pagination"]["page"], int)
		self.assertIsInstance(withdrawals["pagination"]["totalPageCount"], int)
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

	# /main/api/v2/mining/external/{btcAddress}/rigs2

	@unittest.skipIf("/main/api/v2/mining/external/{btcAddress}/rigs2" not in TESTING_URIS, "skipping successful")
	def test_rig_statuses(self):
		check_test_paramters(["address"])
		rig_statuses = self.public_api.get_rig_statuses(ADDRESS)
		# print(rig_statuses)
		self.assertIsInstance(rig_statuses, dict)
		self.assertIsInstance(rig_statuses["address"], str)
	# {
	# 	address : string - BTC mining address
	# }

	# Hashpower public

	# /main/api/v2/hashpower/orderBook

	@unittest.skipIf("/main/api/v2/hashpower/orderBook" not in TESTING_URIS, "skipping successful")
	def test_hashpower_orderbook(self):
		check_test_paramters(["algorithm"])
		hashpower_orderbook = self.public_api.get_hashpower_orderbook(ALGORITHM)
		# print(hashpower_orderbook)
		self.assertIsInstance(hashpower_orderbook, dict)
		self.assertIsInstance(hashpower_orderbook["stats"], dict)
		try:
			self.assertIsInstance(hashpower_orderbook["stats"]["updatedTs"], str)
		except KeyError: pass
		try:
			self.assert_is_number(hashpower_orderbook["stats"]["totalSpeed"])
		except KeyError: pass
		try:
			self.assert_is_number(hashpower_orderbook["stats"]["marketFactor"])
		except KeyError: pass
		try:
			self.assertIsInstance(hashpower_orderbook["stats"]["displayMarketFactor"], str)
		except KeyError: pass
		try:
			self.assertIsInstance(hashpower_orderbook["stats"]["orders"], list)
			for order in hashpower_orderbook["stats"]["orders"]:
				self.assert_is_order_response(order)
		except KeyError: pass
		try:
			self.assertIsInstance(hashpower_orderbook["stats"]["pagination"], dict)
			self.assertIsInstance(hashpower_orderbook["stats"]["pagination"]["size"], int)
			self.assertIsInstance(hashpower_orderbook["stats"]["pagination"]["page"], int)
			self.assertIsInstance(hashpower_orderbook["stats"]["pagination"]["totalPageCount"], int)
		except KeyError: pass
	# {
	# 	stats : {
	# 		{
	# 			updatedTs : string - Timestamp of the order book in ISO format.
	# 			totalSpeed : number - Total speed of the market [TH/Sol/G]/s.
	# 			marketFactor : number - Market factor for the algorithm
	# 			displayMarketFactor : string - Market unit for the algorithm
	# 			orders : [
	# 				{
	# 					id : string - Order ID
	# 					type : string - Order type - STANDARD, FIXED
	# 					price : number - Price in BTC/factor[TH/Sol/G]/day
	# 					limit : number - Speed limit [TH/Sol/G]/s
	# 					rigsCount : integer - Rigs mining for order
	# 					acceptedSpeed : number - Current accepted speed [TH/Sol/G]/s
	# 					payingSpeed : number - Current paying speed [TH/Sol/G]/s
	# 					miningStatus : string - Mining status - INACTIVE, LIVE, DEAD_POOL
	# 					alive : boolean - Is order alive?
	# 					myOrder : boolean - Set to true if user is users order, otherwise is not set
	# 					availableAmount : number - Available total amount
	# 					payedAmount : number - Payed amount
	# 					amount : number - Amount
	# 					poolName : string - Pool name
	# 					endTs : string - End timestamp
	# 					updatedTs : string - Order last updated timestamp
	# 					estimateDurationInSeconds : integer - Estimated duration in seconds
	# 				}
	# 			]
	# 			pagination : {
	# 				size : integer - Page size
	# 				page : integer - Page number (first page is 0)
	# 				totalPageCount : integer - Total page count
	# 			}
	# 		}
	# 	}
	# }

	# /main/api/v2/hashpower/orders/fixedPrice

	@unittest.skipIf("/main/api/v2/hashpower/orders/fixedPrice" not in TESTING_URIS, "skipping successful")
	@unittest.expectedFailure
	def test_price_request(self):
		check_test_paramters(["markets", "market"])
		# TODO
		# fix, notes in changelog
		buy_info = self.public_api.buy_info()
		# print(buy_info)
		def test(algo_info):
			def test2(market):
				try:
					price_request = self.public_api.fixed_price_request(algo_info["name"], market, algo_info["min_limit"])
					# print(price_request)
					self.assertIsInstance(price_request, dict)
					self.assert_is_number(price_request["fixedMax"])
					self.assert_is_number(price_request["fixedPrice"])
				except Exception as e:
					print(e)
					raise Exception
			if TEST_LISTS:
				for market in nicehash.MARKETS:
					test2(market)
			else:
				test2(MARKET)
		if TEST_LISTS:
			for algo_info in buy_info["miningAlgorithms"]:
				test(algo_info)
		elif len(buy_info["miningAlgorithms"]) > 0:
			test(buy_info["miningAlgorithms"][0])
		else: raise Exception("Empty return data for testing; missing mining algorithms")
	# {
	# 	fixedMax : number - Maximal allowed speed limit for fixed order [TH/Sol/G]/s
	# 	fixedPrice : number - Current price for fixed order in BTC/factor[TH/Sol/G]/day
	# }

	# /main/api/v2/hashpower/orders/summaries

	@unittest.skipIf("/main/api/v2/hashpower/orders/summaries" not in TESTING_URIS, "skipping successful")
	def test_hashpower_summaries(self):
		check_test_paramters(["algorithm", "market"])
		hashpower_summaries = self.public_api.get_hashpower_summaries()
		# print(hashpower_summaries)
		self.assertIsInstance(hashpower_summaries, dict)
		self.assertIsInstance(hashpower_summaries["summaries"], dict)
		def test(key):
			self.assertIsInstance(hashpower_summaries["summaries"][key]["profs"], list)
			def test2(prof):
				self.assertIsInstance(prof["type"], str)
				self.assert_is_number(prof["speed"])
				self.assert_is_number(prof["price"])
				self.assertIsInstance(prof["rigCount"], int)
				self.assertIsInstance(prof["orderCount"], int)
			if TEST_LISTS:
				for prof in hashpower_summaries["summaries"][key]["profs"]:
					test2(prof)
			else:
				test2(hashpower_summaries["summaries"][key]["profs"][0])
			self.assert_is_number(hashpower_summaries["summaries"][key]["acceptedPoolSpeed"])
			self.assert_is_number(hashpower_summaries["summaries"][key]["acceptedRigSpeed"])
			self.assert_is_number(hashpower_summaries["summaries"][key]["payingPrice"])
			self.assert_is_number(hashpower_summaries["summaries"][key]["rejectedPoolSpeed"])
			self.assert_is_number(hashpower_summaries["summaries"][key]["rejectedRigSpeed"])
		for key in hashpower_summaries["summaries"].keys():
			test(key)
			if not TEST_LISTS: break
		#
		hashpower_summaries = self.public_api.get_hashpower_summaries(algorithm=ALGORITHM, market=MARKET)
		# print(hashpower_summaries)
		self.assertIsInstance(hashpower_summaries, dict)
		self.assertIsInstance(hashpower_summaries["summaries"], dict)
		def test(key):
			self.assertIsInstance(hashpower_summaries["summaries"][key]["profs"], list)
			def test2(prof):
				self.assertIsInstance(prof["type"], str)
				self.assert_is_number(prof["speed"])
				self.assert_is_number(prof["price"])
				self.assertIsInstance(prof["rigCount"], int)
				self.assertIsInstance(prof["orderCount"], int)
			if TEST_LISTS:
				for prof in hashpower_summaries["summaries"][key]["profs"]:
					test2(prof)
			else:
				test2(hashpower_summaries["summaries"][key]["profs"][0])
			self.assert_is_number(hashpower_summaries["summaries"][key]["acceptedPoolSpeed"])
			self.assert_is_number(hashpower_summaries["summaries"][key]["acceptedRigSpeed"])
			self.assert_is_number(hashpower_summaries["summaries"][key]["payingPrice"])
			self.assert_is_number(hashpower_summaries["summaries"][key]["rejectedPoolSpeed"])
			self.assert_is_number(hashpower_summaries["summaries"][key]["rejectedRigSpeed"])
		for key in hashpower_summaries["summaries"].keys():
			test(key)
			if not TEST_LISTS: break
	# {
	# 	summaries : {
	# 		{
	# 			profs : [
	# 				{
	# 					type : string - Type of orders
	# 					speed : number - Speed [H/Sol/G]/s
	# 					price : number - Average price in satoshi/factor[H/Sol/G]/sec
	# 					rigCount : integer - Number of rigs
	# 					orderCount : integer - Number of orders
	# 				}
	# 			]
	# 			acceptedPoolSpeed : number - Accepted pool speed [H/Sol/G]/s
	# 			acceptedRigSpeed : number - Accepted rig speed [H/Sol/G]/s
	# 			payingPrice : number - Price paying for speed in satoshi/factor[H/Sol/G]/sec
	# 			rejectedPoolSpeed : number - Rejected pool speed [H/Sol/G]/s
	# 			rejectedRigSpeed : number - Rejected rig speed [H/Sol/G]/s
	# 		}
	# 	}
	# }

	# /main/api/v2/hashpower/orders/summary

	@unittest.skipIf("/main/api/v2/hashpower/orders/summary" not in TESTING_URIS, "skipping successful")
	def test_hashpower_orders_summary(self):
		check_test_paramters(["algorithm", "market"])
		hashpower_orders_summary = self.public_api.get_hashpower_orders_summary(ALGORITHM, MARKET)
		# print(hashpower_orders_summary)
		self.assertIsInstance(hashpower_orders_summary, dict)
		self.assertIsInstance(hashpower_orders_summary["profs"], list)
		def test(prof):
			self.assertIsInstance(prof["type"], str)
			self.assert_is_number(prof["speed"])
			self.assert_is_number(prof["price"])
			self.assertIsInstance(prof["rigCount"], int)
			self.assertIsInstance(prof["orderCount"], int)	
		if TEST_LISTS:
			for prof in hashpower_orders_summary["profs"]:
				test(prof)
		elif len(hashpower_orders_summary["profs"]) > 0:
			test(hashpower_orders_summary["profs"][0])
		else: raise Exception("Empty return data for testing; missing order summary profs")
		self.assert_is_number(hashpower_orders_summary["acceptedPoolSpeed"])
		self.assert_is_number(hashpower_orders_summary["acceptedRigSpeed"])
		self.assert_is_number(hashpower_orders_summary["payingPrice"])
		self.assert_is_number(hashpower_orders_summary["rejectedPoolSpeed"])
		self.assert_is_number(hashpower_orders_summary["rejectedRigSpeed"])
	# {
	# 	profs : [
	# 		{
	# 			type : string - Type of orders
	# 			speed : number - Speed [H/Sol/G]/s
	# 			price : number - Average price in satoshi/factor[H/Sol/G]/sec
	# 			rigCount : integer - Number of rigs
	# 			orderCount : integer - Number of orders
	# 		}
	# 	]
	# 	acceptedPoolSpeed : number - Accepted pool speed [H/Sol/G]/s
	# 	acceptedRigSpeed : number - Accepted rig speed [H/Sol/G]/s
	# 	payingPrice : number - Price paying for speed in satoshi/factor[H/Sol/G]/sec
	# 	rejectedPoolSpeed : number - Rejected pool speed [H/Sol/G]/s
	# 	rejectedRigSpeed : number - Rejected rig speed [H/Sol/G]/s
	# }

	# /main/api/v2/public/algo/history

	@unittest.skipIf("/main/api/v2/public/algo/history" not in TESTING_URIS, "skipping successful")
	def test_algo_history(self):
		check_test_paramters(["algorithm"])
		if not ALGORITHM: return
		algo_history = self.public_api.get_algo_history(ALGORITHM)
		# print(algo_history)
		self.assertIsInstance(algo_history, list)
		def test(history):
			self.assertIsInstance(history, list)
			def test2(algo):
				self.assert_is_number(algo)
			if TEST_LISTS:
				for algo in history:
					test2(algo)
			elif len(history) > 0:
				test2(history[0])
		if TEST_LISTS:
			for history in algo_history:
				test(history)
		elif len(algo_history) > 0:
			test(algo_history[0])
		else: raise Exception("Empty return data for testing; missing algo history")
	# [
	# 	[
	# 		number - History of algorithm, list with 3 items: timestamp, speed [TH/Sol/G]/s, price in satoshi/factor[H/Sol/G]/sec
	# 	]
	# ]

	# /main/api/v2/public/buy/info

	@unittest.skipIf("/main/api/v2/public/buy/info" not in TESTING_URIS, "skipping successful")
	def test_buy_info(self):
		buy_info = self.public_api.buy_info()
		# print(buy_info)
		self.assertIsInstance(buy_info, dict)
		self.assertIsInstance(buy_info["miningAlgorithms"], list)
		def test(algo):
			self.assertIsInstance(algo, dict)
			self.assert_is_number(algo["down_step"])
			self.assert_is_number(algo["min_diff_working"])
			self.assert_is_number(algo["min_limit"])
			self.assert_is_number(algo["max_limit"])
			self.assertIsInstance(algo["speed_text"], str)
			self.assert_is_number(algo["min_diff_initial"])
			self.assertIsInstance(algo["name"], str)
			self.assertIsInstance(algo["algo"], int)
			self.assert_is_number(algo["multi"])
			self.assert_is_number(algo["min_price"])
			self.assert_is_number(algo["max_price"])
			self.assert_is_number(algo["min_amount"])			
		if TEST_LISTS:
			for algo in buy_info["miningAlgorithms"]:
				test(algo)
		elif len(buy_info["miningAlgorithms"]) > 0:
			test(buy_info["miningAlgorithms"][0])
		else: raise Exception("Empty return data for testing; missing mining algorithms")
	# {
	# 	miningAlgorithms : [
	# 		{
	# 			down_step : number - Maximal allowed down step for price
	# 			min_diff_working : number - Minimal working difficulty
	# 			min_limit : number - Minimal value for speed limit
	# 			max_limit : number - Maximal value for speed limit
	# 			speed_text : string - Speed unit
	# 			min_diff_initial : number - Minimal initial difficulty
	# 			name : string - Algorithm name
	# 			algo : integer - Algorithm code
	# 			multi : number - Unit factor
	# 			min_price : number - Minimal value for price in BTC/factor[TH/Sol/G]/day
	# 			max_price : number - Maximal value for price in BTC/factor[TH/Sol/G]/day
	# 			min_amount : number - Minimal allowed amount
	# 		}
	# 	]
	# }

	# /main/api/v2/public/orders

	@unittest.skipIf("/main/api/v2/public/orders" not in TESTING_URIS, "skipping successful")
	def test_orders(self):
		orders = self.public_api.get_orders()
		# print(orders)
		self.assertIsInstance(orders, dict)
		self.assertIsInstance(orders["list"], list)
		def test(order):
			self.assert_is_order_response(order)
		if TEST_LISTS:
			for order in orders["list"]:
				test(order)
		elif len(orders["list"]) > 0:
			test(orders["list"][0])
		else: raise Exception("Empty return data for testing; missing hashpower orders")
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
	# 			code : string - Enum code - STANDARD, FIXED
	# 			description : string - Translated enum
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
	# 				stratumHostname : string - Hostname or ip of the pool
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

	# /main/api/v2/public/simplemultialgo/info

	@unittest.skipIf("/main/api/v2/public/simplemultialgo/info" not in TESTING_URIS, "skipping successful")
	def test_multialgo_info(self):
		multialgo_info = self.public_api.get_multialgo_info()
		# print(multialgo_info)
		self.assertIsInstance(multialgo_info, dict)
		self.assertIsInstance(multialgo_info["miningAlgorithms"], list)
		def test(algo):
			self.assertIsInstance(algo, dict)
			self.assertIsInstance(algo["algorithm"], str)
			self.assertIsInstance(algo["title"], str)
			self.assert_is_number(algo["speed"])
			self.assert_is_number(algo["paying"])
		if TEST_LISTS:
			for algo in multialgo_info["miningAlgorithms"]:
				test(algo)
		elif len(multialgo_info["miningAlgorithms"]) > 0:
			test(multialgo_info["miningAlgorithms"][0])
		else: raise Exception("Empty return data for testing; missing mining algorithms")
	# {
	# 	miningAlgorithms : [
	# 		{
	# 			algorithm : string - Algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 			title : string - Title
	# 			speed : number - Mining algorithm speed [H/Sol/G]/s
	# 			paying : number - Mining algorithm price in satoshi/factor[H/Sol/G]/sec
	# 		}
	# 	]
	# }

	# /main/api/v2/public/stats/global/24h

	@unittest.skipIf("/main/api/v2/public/stats/global/24h" not in TESTING_URIS, "skipping successful")
	def test_global_stats_24(self):
		global_stats_24 = self.public_api.get_global_stats_24()
		# print(global_stats_24)
		self.assertIsInstance(global_stats_24, dict)
		self.assertIsInstance(global_stats_24["algos"], list)
		def test(algo):
			self.assertIsInstance(algo, dict)
			self.assertIsInstance(algo["a"], int)
			self.assert_is_number(algo["p"])
			self.assert_is_number(algo["s"])
			self.assertIsInstance(algo["r"], int)
			self.assertIsInstance(algo["o"], int)
		if TEST_LISTS:
			for algo in global_stats_24["algos"]:
				test(algo)
		elif len(global_stats_24["algos"]) > 0:
			test(global_stats_24["algos"][0])
		else: raise Exception("Empty return data for testing; missing algos")
	# {
	# 	algos : [
	# 		{
	# 			a : integer - Algorithem code
	# 			p : number - Paying price in satoshi/factor[H/Sol/G]/sec
	# 			s : number - Total speed [H/Sol/G]/s
	# 			r : integer - Number of rigs on the algorithm
	# 			o : integer - Number active orders
	# 		}
	# 	]
	# }

	# /main/api/v2/public/stats/global/current

	@unittest.skipIf("/main/api/v2/public/stats/global/current" not in TESTING_URIS, "skipping successful")
	def test_current_global_stats(self):
		current_global_stats = self.public_api.get_current_global_stats()
		# print(current_global_stats)
		self.assertIsInstance(current_global_stats, dict)
		self.assertIsInstance(current_global_stats["algos"], list)
		def test(algo):
			self.assertIsInstance(algo, dict)
			self.assertIsInstance(algo["a"], int)
			self.assert_is_number(algo["p"])
			self.assert_is_number(algo["s"])
			self.assertIsInstance(algo["r"], int)
			self.assertIsInstance(algo["o"], int)
		if TEST_LISTS:
			for algo in current_global_stats["algos"]:
				test(algo)
		elif len(current_global_stats["algos"]) > 0:
			test(current_global_stats["algos"][0])
		else: raise Exception("Empty return data for testing; missing algos")
	# {
	# 	algos : [
	# 		{
	# 			a : integer - Algorithem code
	# 			p : number - Paying price in satoshi/factor[H/Sol/G]/sec
	# 			s : number - Total speed [H/Sol/G]/s
	# 			r : integer - Number of rigs on the algorithm
	# 			o : integer - Number active orders
	# 		}
	# 	]
	# }

	# Public

	# /main/api/v2/mining/algorithms

	@unittest.skipIf("/main/api/v2/mining/algorithms" not in TESTING_URIS, "skipping successful")
	def test_algorithms(self):
		algorithms = self.public_api.get_algorithms()
		# print(algorithms)
		self.assertIsInstance(algorithms, dict)
		self.assertIsInstance(algorithms["miningAlgorithms"], list)
		def test(algo):
			self.assertIsInstance(algo, dict)
			self.assertIsInstance(algo["algorithm"], str)
			self.assertIsInstance(algo["title"], str)
			self.assertIsInstance(algo["enabled"], bool)
			self.assertIsInstance(algo["order"], int)
			self.assertIsInstance(algo["displayMiningFactor"], str)
			self.assert_is_number(algo["miningFactor"])
			self.assertIsInstance(algo["displayMarketFactor"], str)
			self.assert_is_number(algo["marketFactor"])
			self.assert_is_number(algo["minimalOrderAmount"])
			self.assert_is_number(algo["minSpeedLimit"])
			self.assert_is_number(algo["maxSpeedLimit"])
			self.assert_is_number(algo["priceDownStep"])
			self.assert_is_number(algo["minimalPoolDifficulty"])
			self.assertIsInstance(algo["port"], int)
			self.assertIsInstance(algo["color"], str)
			self.assertIsInstance(algo["ordersEnabled"], bool)
		if TEST_LISTS:
			for algo in algorithms["miningAlgorithms"]:
				test(algo)
		elif len(algorithms["miningAlgorithms"]) > 0:
			test(algorithms["miningAlgorithms"][0])
		else: raise Exception("Empty return data for testing; missing mining algorithms")
	# {
	# 	miningAlgorithms : [
	# 		{
	# 			algorithm : string - Algorithm - SCRYPT, SHA256, SCRYPTNF, X11, X13, KECCAK, X15, NIST5, NEOSCRYPT, LYRA2RE, WHIRLPOOLX, QUBIT, QUARK, AXIOM, LYRA2REV2, SCRYPTJANENF16, BLAKE256R8, BLAKE256R14, BLAKE256R8VNL, HODL, DAGGERHASHIMOTO, DECRED, CRYPTONIGHT, LBRY, EQUIHASH, PASCAL, X11GOST, SIA, BLAKE2S, SKUNK, CRYPTONIGHTV7, CRYPTONIGHTHEAVY, LYRA2Z, X16R, CRYPTONIGHTV8, SHA256ASICBOOST, ZHASH, BEAM, GRINCUCKAROO29, GRINCUCKATOO31, LYRA2REV3, CRYPTONIGHTR, CUCKOOCYCLE, GRINCUCKAROOD29, BEAMV2, X16RV2, RANDOMXMONERO, EAGLESONG, CUCKAROOM, GRINCUCKATOO32, HANDSHAKE, KAWPOW, CUCKAROO29BFC, BEAMV3, CUCKAROOZ29, OCTOPUS
	# 			title : string - Title of the algorithm
	# 			enabled : boolean - Is the algorithm Enabled
	# 			order : integer - Algorithm order number
	# 			displayMiningFactor : string - Unit for mining factor
	# 			miningFactor : number - Mining factor
	# 			displayMarketFactor : string - Unit for market factor
	# 			marketFactor : number - Market factor
	# 			minimalOrderAmount : number - Minimal amount in BTC to create order
	# 			minSpeedLimit : number - Minimal allowed speed limit
	# 			maxSpeedLimit : number - Maximal allowed speed limit
	# 			priceDownStep : number - Maximal hashpower order down step
	# 			minimalPoolDifficulty : number - Minimal required pool difficulty
	# 			port : integer - TCP port for algorithm
	# 			color : string - Color in charts for algorithm
	# 			ordersEnabled : boolean - Are hashpower orders enabled
	# 		}
	# 	]
	# }

	# /main/api/v2/public/currencies

	@unittest.skipIf("/main/api/v2/public/currencies" not in TESTING_URIS, "skipping successful")
	def test_currencies(self):
		currencies = self.public_api.get_currencies()
		# print(currencies)
		self.assertIsInstance(currencies, dict)
		self.assertIsInstance(currencies["currencies"], list)
		def test(currency):
			self.assertIsInstance(currency, dict)
			self.assertIsInstance(currency["symbol"], str)
			self.assertIsInstance(currency["name"], str)
			self.assertIsInstance(currency["transactionInfoUrl"], str)
			if currency["addressInfoUrl"]:
				self.assertIsInstance(currency["addressInfoUrl"], str)
			self.assertIsInstance(currency["wallets"], list)
			def test2(wallet):
				self.assertIsInstance(wallet, str)
			if TEST_LISTS:
				for wallet in currency["wallets"]:
					test2(wallet)
			else:
				test2(currency["wallets"][0])
			self.assertIsInstance(currency["order"], int)
			self.assertIsInstance(currency["base"], str)
			self.assertIsInstance(currency["subunits"], int)
		if TEST_LISTS:
			for currency in currencies["currencies"]:
				test(currency)
		elif len(currencies["currencies"]) > 0:
			test(currencies["currencies"][0])
	# {
	# 	currencies : [
	# 		{
	# 			symbol : string - Symbol - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 			name : string - Name
	# 			transactionInfoUrl : string - Url for transactions
	# 			addressInfoUrl : string - Url for addresses
	# 			wallets : [
	# 				string - List of wallet types - BITGO, COINBASE, PAYEER, EXTERNAL, FEES, KRIPTOMAT, BLOCKCHAIN, LIGHTNING, INTERNAL, MULTISIG
	# 			]
	# 			order : integer - Currency order number
	# 			base : string - Base currency - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 			subunits : integer - Subunit decimal size
	# 		}
	# 	]
	# }

	def assert_is_fee_response(self, fee_response):
		self.assertIsInstance(fee_response, dict)
		try:
			if fee_response["coin"]: self.assertIsInstance(fee_response["coin"], str)
		except KeyError: pass
		try:
			self.assertIsInstance(fee_response["intervals"], list)
			def test(interval):
				self.assertIsInstance(interval, dict)
				self.assert_is_number(interval["start"])
				self.assert_is_number(interval["end"])
				self.assertIsInstance(interval["element"], dict)
				self.assert_is_number(interval["element"]["value"])
				self.assertIsInstance(interval["element"]["type"], str)
				self.assert_is_number(interval["element"]["sndValue"])
				if interval["element"]["sndType"]:
					self.assertIsInstance(interval["element"]["sndType"], str)
			if TEST_LISTS:
				for interval in fee_response["intervals"]:
					test(interval)
			elif len(fee_response["intervals"]) > 0:
				test(fee_response["intervals"][0])
		except KeyError: pass
	# {
	# 	coin : string - Currency symbol - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 	intervals : [
	# 		{
	# 			start : number - Start of the interval
	# 			end : number - End of the interval
	# 			element : {
	# 				value : number - Base fee value
	# 				type : string - Base fee type - ABSOLUTE, PERCENTAGE
	# 				sndValue : number - Second fee value
	# 				sndType : string - Second fee type - ABSOLUTE, PERCENTAGE
	# 			}
	# 		}
	# 	]
	# }

	# /main/api/v2/public/service/fee/info

	@unittest.skipIf("/main/api/v2/public/service/fee/info" not in TESTING_URIS, "skipping successful")
	def test_fee_rules(self):
		fee_rules = self.public_api.get_fee_rules()
		# print(fee_rules)
		self.assertIsInstance(fee_rules, dict)
		self.assertIsInstance(fee_rules["deposit"], dict)
		def test(key):
			if fee_rules["deposit"][key]["rules"]:
				self.assert_is_fee_response(fee_rules["deposit"][key]["rules"])
		for key in fee_rules["deposit"].keys():
			test(key)
			if not TEST_LISTS: break
		self.assertIsInstance(fee_rules["withdrawal"], dict)
		def test2(key):
			if fee_rules["withdrawal"][key]["rules"]:
				self.assert_is_fee_response(fee_rules["withdrawal"][key]["rules"])
		for key in fee_rules["deposit"].keys():
			test2(key)
			if not TEST_LISTS: break
		self.assert_is_fee_response(fee_rules["exchangeMaker"])
		self.assert_is_fee_response(fee_rules["buyingNonRefundableFee"])
		self.assert_is_fee_response(fee_rules["buyingSpentFee"])
		self.assert_is_fee_response(fee_rules["sellFee"])
	# {
	# 	deposit : {
	# 		{
	# 			rules : {
	# 				{
	# 					coin : string - Currency symbol - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 					intervals : [
	# 						{
	# 							start : number - Start of the interval
	# 							end : number - End of the interval
	# 							element : {
	# 								value : number - Base fee value
	# 								type : string - Base fee type - ABSOLUTE, PERCENTAGE
	# 								sndValue : number - Second fee value
	# 								sndType : string - Second fee type - ABSOLUTE, PERCENTAGE
	# 							}
	# 						}
	# 					]
	# 				}
	# 			}
	# 		}
	# 	}
	# 	withdrawal : {
	# 		{
	# 			rules : {
	# 				{
	# 					coin : string - Currency symbol - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 					intervals : [
	# 						{
	# 							start : number - Start of the interval
	# 							end : number - End of the interval
	# 							element : {
	# 								value : number - Base fee value
	# 								type : string - Base fee type - ABSOLUTE, PERCENTAGE
	# 								sndValue : number - Second fee value
	# 								sndType : string - Second fee type - ABSOLUTE, PERCENTAGE
	# 							}
	# 						}
	# 					]
	# 				}
	# 			}
	# 		}
	# 	}
	# 	exchangeTaker : {
	# 		coin : string - Currency symbol - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 		intervals : [
	# 			{
	# 				start : number - Start of the interval
	# 				end : number - End of the interval
	# 				element : {
	# 					value : number - Base fee value
	# 					type : string - Base fee type - ABSOLUTE, PERCENTAGE
	# 					sndValue : number - Second fee value
	# 					sndType : string - Second fee type - ABSOLUTE, PERCENTAGE
	# 				}
	# 			}
	# 		]
	# 	}
	# 	exchangeMaker : {
	# 		coin : string - Currency symbol - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 		intervals : [
	# 			{
	# 				start : number - Start of the interval
	# 				end : number - End of the interval
	# 				element : {
	# 					value : number - Base fee value
	# 					type : string - Base fee type - ABSOLUTE, PERCENTAGE
	# 					sndValue : number - Second fee value
	# 					sndType : string - Second fee type - ABSOLUTE, PERCENTAGE
	# 				}
	# 			}
	# 		]
	# 	}
	# 	buyingNonRefundableFee : {
	# 		coin : string - Currency symbol - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 		intervals : [
	# 			{
	# 				start : number - Start of the interval
	# 				end : number - End of the interval
	# 				element : {
	# 					value : number - Base fee value
	# 					type : string - Base fee type - ABSOLUTE, PERCENTAGE
	# 					sndValue : number - Second fee value
	# 					sndType : string - Second fee type - ABSOLUTE, PERCENTAGE
	# 				}
	# 			}
	# 		]
	# 	}
	# 	buyingSpentFee : {
	# 		coin : string - Currency symbol - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 		intervals : [
	# 			{
	# 				start : number - Start of the interval
	# 				end : number - End of the interval
	# 				element : {
	# 					value : number - Base fee value
	# 					type : string - Base fee type - ABSOLUTE, PERCENTAGE
	# 					sndValue : number - Second fee value
	# 					sndType : string - Second fee type - ABSOLUTE, PERCENTAGE
	# 				}
	# 			}
	# 		]
	# 	}
	# 	sellFee : {
	# 		coin : string - Currency symbol - BTC, ETH, XRP, BCH, LTC, ZEC, DASH, XLM, EOS, USDT, BSV, LINK, BAT, PAX, ZRX, HOT, OMG, REP, NEXO, BTG, EURKM, ENJ, MATIC, ELF, SNT, BNT, KNC, MTL, POLY, POWR, GTO, LOOM, CVC, AST, PPT, LRC, KEY, STORJ, STORM, TNT, DATA, AOA, RDN, USDC, FET, ANT, AERGO, LBA, XMR, MITH, BAND, SXP, EURS, WBTC, RVN, UNI, AAVE, FTM, YFI, DOGE, ONEINCH, SUSHI, TBTC, TETH, TXRP, TBCH, TLTC, TZEC, TDASH, TXLM, TEOS, TERC, TBSV, TBTG, TEURKM, TXMR, TRVN, TDOGE
	# 		intervals : [
	# 			{
	# 				start : number - Start of the interval
	# 				end : number - End of the interval
	# 				element : {
	# 					value : number - Base fee value
	# 					type : string - Base fee type - ABSOLUTE, PERCENTAGE
	# 					sndValue : number - Second fee value
	# 					sndType : string - Second fee type - ABSOLUTE, PERCENTAGE
	# 				}
	# 			}
	# 		]
	# 	}
	# }

	# /api/v2/enum/countries

	@unittest.skipIf("/api/v2/enum/countries" not in TESTING_URIS, "skipping successful")
	def test_countries(self):
		countries = self.public_api.get_countries()
		# print(countries)
		self.assertIsInstance(countries, dict)
		def test(country):
			self.assertIsInstance(country, dict)
			self.assertIsInstance(country["code"], str)
			self.assertIsInstance(country["name"], str)
			self.assertIsInstance(country["flag"], str)
			self.assertIsInstance(country["dialCode"], str)
			self.assertIsInstance(country["continent"], str)
		self.assertIsInstance(countries["countries"], list)
		if TEST_LISTS:
			for country in countries["countries"]:
				test(country)
		elif len(countries["countries"]) > 0:
			test(countries["countries"][0])
		else: raise Exception("Empty return data for testing; missing countries")
		def test2(continent):
			self.assertIsInstance(continent, dict)
			self.assertIsInstance(continent["code"], str)
			self.assertIsInstance(continent["name"], str)
		self.assertIsInstance(countries["continents"], list)
		if TEST_LISTS:
			for continent in countries["continents"]:
				test2(continent)
		elif len(countries["continents"]) > 0:
			test2(countries["continents"][0])
		else: raise Exception("Empty return data for testing; missing continents")
		def test3(statePerCountry):
			self.assertIsInstance(statePerCountry, dict)
			self.assertIsInstance(statePerCountry["country"], str)
			self.assertIsInstance(statePerCountry["states"], list)
			def test4(state):
				self.assertIsInstance(state["code"], str)
				self.assertIsInstance(state["name"], str)
			if TEST_LISTS:
				for state in statePerCountry["states"]:
					test4(state)
			elif len(statePerCountry["states"]) > 0:
				test4(statePerCountry["states"][0])
			else: raise Exception("Empty return data for testing; missing states")
		self.assertIsInstance(countries["statesPerCountry"], list)
		if TEST_LISTS:
			for statePerCountry in countries["statesPerCountry"]:
				test3(statePerCountry)
		elif len(countries["statesPerCountry"]) > 0:
			test3(countries["statesPerCountry"][0])
		else: raise Exception("Empty return data for testing; missing states per country")
	# {
	# 	countries : [
	# 		{
	# 			code : string
	# 			name : string
	# 			flag : string
	# 			dialCode : string
	# 			continent : string
	# 		}
	# 	]
	# 	continents : [
	# 		{
	# 			code : string
	# 			name : string
	# 		}
	# 	]
	# 	statesPerCountry : [
	# 		{
	# 			country : string
	# 			states : [
	# 				{
	# 					code : string
	# 					name : string
	# 				}
	# 			]
	# 		}
	# 	]
	# }

	# /api/v2/enum/kmCountries

	@unittest.skipIf("/api/v2/enum/kmCountries" not in TESTING_URIS, "skipping successful")
	def test_km_countries(self):
		km_countries = self.public_api.get_km_countries()
		# print(km_countries)
		self.assertIsInstance(km_countries, list)
		def test(km):
			self.assertIsInstance(km, str)
		if TEST_LISTS:
			for km in km_countries:
				test(km)
		elif len(km_countries) > 0:
			test(km_countries[0])
		else: raise Exception("Empty return data for testing; missing km countries")
	# [
	# 	object
	# ]

	# /api/v2/enum/permissions

	@unittest.skipIf("/api/v2/enum/permissions" not in TESTING_URIS, "skipping successful")
	def test_permissions(self):
		permissions = self.public_api.get_permissions()
		# print(permissions)
		self.assertIsInstance(permissions, dict)
		self.assertIsInstance(permissions["permissionSettings"], list)
		def test(setting):
			self.assertIsInstance(setting, dict)
			self.assertIsInstance(setting["permission"], dict)
			self.assertIsInstance(setting["permission"]["type"], str)
			self.assertIsInstance(setting["permission"]["title"], str)
			self.assertIsInstance(setting["permission"]["description"], str)
			self.assertIsInstance(setting["permission"]["order"], int)
			self.assertIsInstance(setting["permission"]["group"], dict)
			self.assertIsInstance(setting["permission"]["group"]["type"], str)
			self.assertIsInstance(setting["permission"]["group"]["title"], str)
			self.assertIsInstance(setting["permission"]["group"]["order"], int)
			self.assertIsInstance(setting["enabled"], bool)
		if TEST_LISTS:
			for setting in permissions["permissionSettings"]:
				test(setting)
		elif len(permissions["permissionSettings"]) > 0:
			test(permissions["permissionSettings"][0])
		else: raise Exception("Empty return data for testing; missing permission settings")
	# {
	# 	permissionSettings : [
	# 		{
	# 			permission : {
	# 				type : string - Code - VBTD, WIFU, WNWA, VHOR, PRCO, ELCO, MAPO, EXOR, VITR, VMDS, MARI, VIUS, MAUS
	# 				title : string - Title
	# 				description : string - Description
	# 				order : integer - Order (inside group)
	# 				group : {
	# 					type : string - Permission group type - WALLET_PERMISSION, MARKETPLACE_PERMISSION, EXCHANGE_PERMISSION, MINING_PERMISSION, USER_MANAGEMENT_SECURITY_PERMISSION
	# 					title : string - Group title
	# 					order : integer - Group order number
	# 				}
	# 			}
	# 			enabled : boolean
	# 		}
	# 	]
	# }

	# /api/v2/enum/xchCountries

	@unittest.skipIf("/api/v2/enum/xchCountries" not in TESTING_URIS, "skipping successful")
	def test_xch_countries(self):
		xch_countries = self.public_api.get_xch_countries()
		# print(xch_countries)
		self.assertIsInstance(xch_countries, list)
		def test(c):
			self.assertIsInstance(c, str)
		if TEST_LISTS:
			for c in xch_countries:
				test(c)
		elif len(xch_countries) > 0:
			test(xch_countries[0])
		else: raise Exception("Empty return data for testing; missing xch countries")
	# [
	# 	object
	# ]

	# /api/v2/system/flags

	@unittest.skipIf("/api/v2/system/flags" not in TESTING_URIS, "skipping successful")
	def test_api_flags(self):
		api_flags = self.public_api.get_api_flags()
		# print(api_flags)
		self.assertIsInstance(api_flags, dict)
		self.assertIsInstance(api_flags["list"], list)
		def test(flag):
			self.assertIsInstance(flag, dict)
			self.assertIsInstance(flag["flagName"], str)
			self.assertIsInstance(flag["flagValue"], bool)
		if TEST_LISTS:
			for flag in api_flags["list"]:
				test(flag)
		elif len(api_flags["list"]) > 0:
			test(api_flags["list"][0])
		else: raise Exception("Empty return data for testing; missing api flags list")
	# {
	# 	list : [
	# 		{
	# 			flagName : string - IS_MAINTENANCE, SYSTEM_UNAVAILABLE, DISABLE_REGISTRATION, IS_KM_MAINTENANCE, IS_PERSONAL_KYC_AVAILABLE, TEST
	# 			flagValue : boolean
	# 		}
	# 	]
	# }

	# /api/v2/time

	@unittest.skipIf("/api/v2/time" not in TESTING_URIS, "skipping successful")
	def test_server_time(self):
		server_time = self.public_api.get_server_time()
		# print(server_time)
		self.assertIsInstance(server_time, dict)
		self.assertIsInstance(server_time["serverTime"], int)
	# {
	# 	serverTime : integer - Time in millis since 1.1.1970 00:00:00 UTC
	# }

	# Exchange public

	# /exchange/api/v2/info/candlesticks

	@unittest.skipIf("/exchange/api/v2/info/candlesticks" not in TESTING_URIS, "skipping successful")
	def test_candlesticks(self):
		check_test_paramters(["market_symbols", "from_s", "to_s", "resolution"])
		candlesticks = self.public_api.get_candlesticks(MARKET_SYMBOLS[0], FROM_S, TO_S, RESOLUTION)
		# print(candlesticks)
		self.assertIsInstance(candlesticks, list)
		def test(candlestick):
			self.assertIsInstance(candlestick, dict)
			self.assertIsInstance(candlestick["time"], int)
			self.assert_is_number(candlestick["open"])
			self.assert_is_number(candlestick["close"])
			self.assert_is_number(candlestick["low"])
			self.assert_is_number(candlestick["high"])
			self.assert_is_number(candlestick["volume"])
			self.assert_is_number(candlestick["quote_volume"])
			self.assertIsInstance(candlestick["count"], int)
		if TEST_LISTS:
			for candlestick in candlesticks:
				test(candlestick)
		elif len(candlesticks) > 0:
			test(candlesticks[0])
		else: raise Exception("Empty return data for testing; missing candlesticks")
	# [
	# 	{
	# 		time : integer - Start time
	# 		open : number - Opening price (first trade)
	# 		close : number - Closing price (last trade)
	# 		low : number - Lowest price
	# 		high : number - Highest price
	# 		volume : number - Base volume of trading activity
	# 		quote_volume : number - Quote volume of trading activity
	# 		count : integer - Number of trades
	# 	}
	# ]

	# /exchange/api/v2/info/marketStats

	@unittest.skipIf("/exchange/api/v2/info/marketStats" not in TESTING_URIS, "skipping successful")
	def test_exchange_statistics(self):
		check_test_paramters(["market_symbols"])
		exchange_statistics = self.public_api.get_exchange_statistics()
		# print(exchange_statistics)
		self.assertIsInstance(exchange_statistics, dict)
		def test(market):
			try:
				market = exchange_statistics[market]
				self.assertIsInstance(market, dict)
				self.assert_is_number(market["l24"])
				self.assert_is_number(market["h24"])
				self.assert_is_number(market["v24"])
				self.assert_is_number(market["v24b"])
				self.assert_is_number(market["v24q"])
				self.assertIsInstance(market["t24"], int)
				self.assert_is_number(market["c24"])
				self.assertIsInstance(market["csjs"], list)
				for dv in market["csjs"]:
					self.assertIsInstance(dv, dict)
					self.assertIsInstance(dv["d"], int)
					self.assert_is_number(dv["v"])
			except KeyError:
				pass
		if TEST_LISTS:
			for market in MARKET_SYMBOLS:
				test(market)
		else:
			test(MARKET_SYMBOLS[0])
	# {
	# {
	# 	Market symbol ["ETHBTC", "BTCUSDT", "BCHBTC", "..."] : {
	# 		{
	# 			l24 : number - Lowest price in 24 hours
	# 			h24 : number - Highest price in 24 hours
	# 			v24 : number - Volume in BTC in 24 hours
	# 			v24b : number - Volume in base currency in 24 hours
	# 			v24q : number - Volume in quote currency in 24 hours
	# 			t24 : integer - Number of trades in 24 hours
	# 			c24 : number - Change as a factor in 24 hours
	# 			csjs : [
	# 				{
	# 					d : integer - Timestamp in seconds since 1.1.1970
	# 					v : number - Price
	# 				}
	# 			]
	# 		}
	# 	}
	# }

	# /exchange/api/v2/info/prices

	@unittest.skipIf("/exchange/api/v2/info/prices" not in TESTING_URIS, "skipping successful")
	def test_current_prices(self):
		check_test_paramters(["market_symbols"])
		current_prices = self.public_api.get_current_prices()
		# print(current_prices)
		self.assertIsInstance(current_prices, dict)
		def test(market):
			try:
				self.assert_is_number(current_prices[market])
			except KeyError:
				pass
		if TEST_LISTS:
			for market in MARKET_SYMBOLS:
				test(market)
		else:
			test(MARKET_SYMBOLS[0])
	# {
	# 	Market symbol [ETHBTC, BTCUSDT, BCHBTC, ...] : {
	# 		number
	# 	}
	# }

	# /exchange/api/v2/info/status

	@unittest.skipIf("/exchange/api/v2/info/status" not in TESTING_URIS, "skipping successful")
	def test_exchange_markets_info(self):
		exchange_markets_info = self.public_api.get_exchange_markets_info()
		# print(exchange_markets_info)
		self.assertIsInstance(exchange_markets_info, dict)
		self.assertIsInstance(exchange_markets_info["symbols"], list)
		def test(symbol):
			self.assertIsInstance(symbol, dict)
			self.assertIsInstance(symbol["symbol"], str)
			self.assertIsInstance(symbol["status"], str)
			self.assertIsInstance(symbol["orderTypes"], list)
			def test2(oT):
				self.assertIsInstance(oT, str)
			if TEST_LISTS:
				for oT in symbol["orderTypes"]:
					test2(oT)
			elif len(symbol["orderTypes"]) > 0:
				test2(symbol["orderTypes"][0])
			self.assertIsInstance(symbol["baseAssetPrecision"], int)
			self.assertIsInstance(symbol["quoteAssetPrecision"], int)
			self.assertIsInstance(symbol["priceAssetPrecision"], int)
			self.assertIsInstance(symbol["priceStep"], int)
			self.assert_is_number(symbol["priMinAmount"])
			self.assert_is_number(symbol["priMaxAmount"])
			self.assert_is_number(symbol["secMinAmount"])
			self.assert_is_number(symbol["secMaxAmount"])
			self.assert_is_number(symbol["minPrice"])
			self.assert_is_number(symbol["maxPrice"])
			self.assertIsInstance(symbol["baseAsset"], str)
			self.assertIsInstance(symbol["quoteAsset"], str)
		if TEST_LISTS:
			for symbol in exchange_markets_info["symbols"]:
				test(symbol)
		elif len(exchange_markets_info["symbols"]) > 0:
			test(exchange_markets_info["symbols"][0])
		else: raise Exception("Empty return data for testing; missing market symbols")
	# {
	# 	symbols : [
	# 		{
	# 			symbol : string - Market symbol
	# 			status : string - Status of the market - UNKNOWN, CLOSED, TRADING, READONLY, UNAVAILABLE, REMOVED
	# 			orderTypes : [
	# 				string - List of orders available on the market - LIMIT, MARKET, STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT, LIMIT_MAKER
	# 			]
	# 			baseAssetPrecision : integer - Precision of base assets
	# 			quoteAssetPrecision : integer - Precision of quote assets
	# 			priceAssetPrecision : integer - Precision of the price
	# 			priceStep : integer - Price step
	# 			priMinAmount : number - Minimal allowed amount for base assets
	# 			priMaxAmount : number - Maximal allowed amount for base assets
	# 			secMinAmount : number - Minimal allowed amount for quote assets
	# 			secMaxAmount : number - Maximal allowed amount for quote assets
	# 			minPrice : number - Minimal allowed price
	# 			maxPrice : number - Maximal allowed amount for quote assets
	# 			baseAsset : string - Base asset currency symbol
	# 			quoteAsset : string - Quote asset currency symbol
	# 		}
	# 	]
	# }

	# /exchange/api/v2/info/trades

	@unittest.skipIf("/exchange/api/v2/info/trades" not in TESTING_URIS, "skipping successful")
	def test_trades(self):
		check_test_paramters(["market_symbols"])
		trades = self.public_api.get_trades(MARKET_SYMBOLS[0])
		# print(trades)
		self.assertIsInstance(trades, list)
		def test(trade):
			self.assertIsInstance(trade, dict)
			self.assertIsInstance(trade["id"], str)
			self.assertIsInstance(trade["dir"], str)
			self.assert_is_number(trade["price"])
			self.assert_is_number(trade["qty"])
			self.assert_is_number(trade["sndQty"])
			self.assertIsInstance(trade["time"], int)
			self.assertIsInstance(trade["fee"], dict)
			self.assertIsInstance(trade["isMaker"], int)
			self.assertIsInstance(trade["orderId"], str)
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

	# /exchange/api/v2/orderbook

	@unittest.skipIf("/exchange/api/v2/orderbook" not in TESTING_URIS, "skipping successful")
	def test_orderbook(self):
		check_test_paramters(["market_symbols"])
		orderbook = self.public_api.get_exchange_orderbook(MARKET_SYMBOLS[0])
		# print(orderbook)
		self.assertIsInstance(orderbook, dict)
		self.assertIsInstance(orderbook["tick"], int)
		try:
			self.assertIsInstance(orderbook["sell"], list)
			def test(sell):
				self.assertIsInstance(sell, list)
				def test2(bid):
					self.assertIsInstance(bid, int)
				if TEST_LISTS:
					for bid in sell:
						test2(bid)
				elif len(sell) > 0:
					test2(sell[0])
			if TEST_LISTS:
				for sell in orderbook["sell"]:
					test(sell)
			elif len(orderbook["sell"]) > 0:
				test(orderbook["sell"][0])
			else: raise Exception("Empty return data for testing; missing orderbook sells")
		except KeyError: pass
		try:
			self.assertIsInstance(orderbook["buys"], list)
			def test(buy):
				self.assertIsInstance(buy, list)
				def test2(ask):
					self.assertIsInstance(ask, int)
				if TEST_LISTS:
					for ask in buy:
						test2(ask)
				elif len(buy) > 0:
					test2(buy[0])
			if TEST_LISTS:
				for buy in orderbook["buys"]:
					test(buy)
			elif len(orderbook["buys"]) > 0:
				test(orderbook["buys"][0])
			else: raise Exception("Empty return data for testing; missing orderbook buys")
		except KeyError: pass
	# {
	# 	tick : integer - Order book tick number
	# 	sell : [
	# 		[
	# 			number - List of bids. Each bid is one element in the list, where first element is price and second volume.
	# 		]
	# 	]
	# 	buys : [
	# 		[
	# 			number - List of asks. Each aks is one element in the list, where first element is price and second volume.
	# 		]
	# 	]
	# }

############################################################################################

if __name__ == '__main__':
	unittest.main()
