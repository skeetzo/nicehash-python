import unittest
import os
import time
from dotenv import load_dotenv
load_dotenv()
#
from python import nicehash

HOST = os.environ.get("TEST_WEBSOCKETS_HOST")
ORGANIZATION_ID = os.environ.get("TEST_ORGANIZATION_ID")
KEY = os.environ.get("TEST_KEY")
SECRET = os.environ.get("TEST_SECRET")

if not HOST or not ORGANIZATION_ID or not KEY or not SECRET:
	raise Exception("missing environment keys")
	
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
MARKET_SYMBOL = MARKET_SYMBOLS[1]
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

PRICE = None
MESSAGE_ID = None

QUANTITY = None
QUANTITY_QUOTE = None

VERBOSE = False
TEST_LISTS = False
# TODO
# add loop for testing each market
HOST = HOST.replace("$MARKET", MARKET_SYMBOL.lower())
# HOST = HOST.replace("$MARKET", "btcusd")
TEST_MARKETS = False


from unittest import IsolatedAsyncioTestCase


class TestNiceHashWebsockets(IsolatedAsyncioTestCase):

	def setUp(self):
		self.websockets_api = nicehash.websockets_api(HOST, ORGANIZATION_ID, KEY, SECRET, verbose=VERBOSE)
		
	def tearDown(self):
		self.websockets_api.close()

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

	##########################################

	def test_subscribe_candlestick_stream(self):
		if not RESOLUTION: raise Exception("Missing test value: resolution")
		sub_candlestick_stream = self.websockets_api.subscribe_candlestick_stream(RESOLUTION)
		print(sub_candlestick_stream)
		self.assertIsInstance(sub_candlestick_stream, dict)
		self.assertIsInstance(sub_candlestick_stream.m, str)
		self.assertIsInstance(sub_candlestick_stream.r, float)
		self.assertIsInstance(sub_candlestick_stream.c, dict)
		self.assertIsInstance(sub_candlestick_stream.c.t, int)
		self.assertIsInstance(sub_candlestick_stream.c.o, float)
		self.assertIsInstance(sub_candlestick_stream.c.c, float)
		self.assertIsInstance(sub_candlestick_stream.c.l, float)
		self.assertIsInstance(sub_candlestick_stream.c.h, float)
		self.assertIsInstance(sub_candlestick_stream.c.v, float)
		# TODO
		# add part that is received / updated
	# {
	#     m : string - Method is always c.s
	#     r : number - Resolution: 1, 60, 1440
	#     c : {
	#         t : integer - Interval start time in sec
	#         o : number - Open price
	#         c : number - Close price
	#         l : number - Lowest price
	#         h : number - Highest price
	#         v : number - Volume
	#     }
	# }
	# {
	#     m : string - Method is always c.u
	#     r : number - Resolution: 1, 60, 1440
	#     c : [
	#         {
	#             t : integer - Interval start time in sec
	#             o : number - Open price
	#             c : number - Close price
	#             l : number - Lowest price
	#             h : number - Highest price
	#             v : number - Volume
	#         }
	#     ]
	# }
	def test_unsubscribe_candlestick_stream(self):
		unsub_candlestick_stream = self.websockets_api.unsubscribe_candlestick_stream()
		print(unsub_candlestick_stream)
		self.assertEqual(unsub_candlestick_stream, dict)

	def test_subscribe_trade_stream(self):
		sub_trade_stream = self.websockets_api.subscribe_trade_stream(MARKET, ORDER_ID)
		print(sub_trade_stream)
		self.assertIsInstance(sub_trade_stream, dict)
		self.assertIsInstance(sub_trade_stream.m, str)
		self.assertIsInstance(sub_trade_stream.t, list)
		def test(o):
			self.assertIsInstance(o.i, str)
			self.assertIsInstance(o.d, str)
			self.assertIsInstance(o.p, float)
			self.assertIsInstance(o.q, float)
			self.assertIsInstance(o.sq, float)
			self.assertIsInstance(o.ts, int)
			self.assertIsInstance(o.f, float)
			self.assertIsInstance(o.m, int)
		if TEST_LISTS:
			for o in sub_trade_stream.t:
				test(o)
		elif len(sub_trade_stream.t) > 0:
			test(sub_trade_stream.t[0])
		# TODO
		# add updated responses
	# {
	#     m : string - Method is always mt.s
	#     t : [
	#         {
	#             i : string - Trade id
	#             d : string - Trade direction - BUY, SELL
	#             p : number - Price
	#             q : number - Quantity
	#             sq : number - Secondary quantity
	#             ts : integer - Timestamp
	#             f : number - Fee ammount
	#             m : integer - Is maker
	#         }
	#     ]
	# }
	# {
	#     m : string - Method is always mt.u
	#     t : [
	#         {
	#             i : string - Trade id
	#             d : string - Trade direction - BUY, SELL
	#             p : number - Price
	#             q : number - Quantity
	#             sq : number - Secondary quantity
	#             ts : integer - Timestamp
	#             f : number - Fee ammount
	#             m : integer - Is maker
	#         }
	#     ]
	# }

	def test_unsubscribe_trade_stream(self):
		unsub_trade_stream = self.websockets_api.unsubscribe_trade_stream()
		print(unsub_trade_stream)
		self.assertEqual(unsub_trade_stream, dict)

	async def test_cancel_all_orders(self):
		# canceled_orders = await self.websockets_api.cancel_all_orders()
		# print(canceled_orders)

		def test(message):
			print(message)
			self.assertIsInstance(message, dict)
			self.assertIsInstance(message.m, str)
			self.assertIsInstance(message.i, str)
			self.assertIsInstance(message.o, list)
			def test(o):
				self.assertIsInstance(o.i, str)
				self.assertIsInstance(o.p, float)
				self.assertIsInstance(o.oq, float)
				self.assertIsInstance(o.osq, float)
				self.assertIsInstance(o.eq, float)
				self.assertIsInstance(o.esq, float)
				self.assertIsInstance(o.t, str)
				self.assertIsInstance(o.d, str)
				self.assertIsInstance(o.sts, int)
				self.assertIsInstance(o.uts, int)
				self.assertIsInstance(o.s, str)
			if TEST_LISTS:
				for o in message.o:
					test(o)
			elif len(message.o) > 0:
				test(message.o[0])

		websocket = await self.websockets_api.cancel_all_orders()

		websocket.on_message = test


	# {
	#     m : string - Method is always o.ca.all
	#     i : string - Message id, the same as in a request
	#     o : [
	#         {
	#             i : string - Order id
	#             p : number - Price
	#             oq : number - Original quantity
	#             osq : number - Original secondary quantity
	#             eq : number - Executed quantity
	#             esq : number - Executed secondary quantity
	#             t : string - Order type - MARKET, LIMIT
	#             d : string - Order side - BUY, SELL
	#             sts : integer - Order submission timestamp
	#             uts : integer - Response time of order's last response
	#             s : string - Order state - CREATED, RESERVED, RESERVATION_ERROR, INSERTED, INSERTED_ERROR, RELEASED, RELEASED_ERROR, PARTIAL, ENTERED, FULL, PROCESSED_ERROR, CANCEL_REQUEST, CANCELLED, CANCELLED_ERROR, REJECTED
	#         }
	#     ]
	# }

	def test_cancel_order(self):
		canceled_order = self.websockets_api.cancel_order()
		print(canceled_order)
		self.assertIsInstance(canceled_order, dict)
		self.assertIsInstance(canceled_order.m, str)
		self.assertIsInstance(canceled_order.i, str)
		self.assertIsInstance(canceled_order.o, dict)
		self.assertIsInstance(canceled_order.o.i, str)
		self.assertIsInstance(canceled_order.o.p, float)
		self.assertIsInstance(canceled_order.o.oq, float)
		self.assertIsInstance(canceled_order.o.osq, float)
		self.assertIsInstance(canceled_order.o.eq, float)
		self.assertIsInstance(canceled_order.o.esq, float)
		self.assertIsInstance(canceled_order.o.t, str)
		self.assertIsInstance(canceled_order.o.d, str)
		self.assertIsInstance(canceled_order.o.sts, int)
		self.assertIsInstance(canceled_order.o.uts, int)
		self.assertIsInstance(canceled_order.o.s, str)
	# {
	#     m : string - Method is o.ca
	#     i : string - Message id, the same as in a request
	#     o : {
	#         i : string - Order id
	#         p : number - Price
	#         oq : number - Original quantity
	#         osq : number - Original secondary quantity
	#         eq : number - Executed quantity
	#         esq : number - Executed secondary quantity
	#         t : string - Order type - MARKET, LIMIT
	#         d : string - Order side - BUY, SELL
	#         sts : integer - Order submission timestamp
	#         uts : integer - Response time of order's last response
	#         s : string - Order state - CREATED, RESERVED, RESERVATION_ERROR, INSERTED, INSERTED_ERROR, RELEASED, RELEASED_ERROR, PARTIAL, ENTERED, FULL, PROCESSED_ERROR, CANCEL_REQUEST, CANCELLED, CANCELLED_ERROR, REJECTED
	#     }
	# }

	def assert_is_order(self, order):
		self.assertIsInstance(order, dict)
		self.assertIsInstance(order.m, str)
		self.assertIsInstance(order.i, str)
		self.assertIsInstance(order.o, dict)
		self.assertIsInstance(order.o.i, str)
		self.assertIsInstance(order.o.p, float)
		self.assertIsInstance(order.o.oq, float)
		self.assertIsInstance(order.o.osq, float)
		self.assertIsInstance(order.o.eq, float)
		self.assertIsInstance(order.o.esq, float)
		self.assertIsInstance(order.o.t, str)
		self.assertIsInstance(order.o.d, str)
		self.assertIsInstance(order.o.sts, int)
		self.assertIsInstance(order.o.uts, int)
		self.assertIsInstance(order.o.s, str)

	def test_create_limit_order(self):
		limit_order = self.websockets_api.create_limit_order(MESSAGE_ID, SIDE, QUANTITY, PRICE)
		print(limit_order)
		self.assert_is_order(order)

	def test_create_buy_market_order(self):
		market_buy_order = self.websockets_api.create_buy_market_order(MESSAGE_ID, QUANTITY_QUOTE)
		print(market_order)
		self.assert_is_order(order)

	def test_create_sell_market_order(self):
		market_sell_order = self.websockets_api.create_sell_market_order(MESSAGE_ID, QUANTITY)
		print(market_sell_order)
		self.assert_is_order(order)
	# {
	#     m : string - Method is o.cr
	#     i : string - Message id, the same as in a request
	#     o : {
	#         i : string - Order id
	#         p : number - Price
	#         oq : number - Original quantity
	#         osq : number - Original secondary quantity
	#         eq : number - Executed quantity
	#         esq : number - Executed secondary quantity
	#         t : string - Order type - MARKET, LIMIT
	#         d : string - Order side - BUY, SELL
	#         sts : integer - Order submission timestamp
	#         uts : integer - Response time of order's last response
	#         s : string - Order state - CREATED, RESERVED, RESERVATION_ERROR, INSERTED, INSERTED_ERROR, RELEASED, RELEASED_ERROR, PARTIAL, ENTERED, FULL, PROCESSED_ERROR, CANCEL_REQUEST, CANCELLED, CANCELLED_ERROR, REJECTED
	#     }
	# }

	def test_subscribe_order_stream(self):
		sub_order_stream = self.websockets_api.subscribe_order_stream()
		print(sub_order_stream)
		self.assertIsInstance(sub_order_stream, dict)
		self.assertIsInstance(sub_order_stream.m, str)
		self.assertIsInstance(sub_order_stream.i, str)
		self.assertIsInstance(sub_order_stream.o, dict)
		self.assertIsInstance(sub_order_stream.o.i, str)
		self.assertIsInstance(sub_order_stream.o.p, float)
		self.assertIsInstance(sub_order_stream.o.oq, float)
		self.assertIsInstance(sub_order_stream.o.osq, float)
		self.assertIsInstance(sub_order_stream.o.eq, float)
		self.assertIsInstance(sub_order_stream.o.esq, float)
		self.assertIsInstance(sub_order_stream.o.t, str)
		self.assertIsInstance(sub_order_stream.o.d, str)
		self.assertIsInstance(sub_order_stream.o.sts, int)
		self.assertIsInstance(sub_order_stream.o.uts, int)
		self.assertIsInstance(sub_order_stream.o.s, str)
		# TODO
		# add further updated responses
	# {
	#     m : string - Method is o.s
	#     o : {
	#         i : string - Order id
	#         p : number - Price
	#         oq : number - Original quantity
	#         osq : number - Original secondary quantity
	#         eq : number - Executed quantity
	#         esq : number - Executed secondary quantity
	#         t : string - Order type - MARKET, LIMIT
	#         d : string - Order side - BUY, SELL
	#         sts : integer - Order submission timestamp
	#         uts : integer - Response time of order's last response
	#         s : string - Order state - CREATED, RESERVED, RESERVATION_ERROR, INSERTED, INSERTED_ERROR, RELEASED, RELEASED_ERROR, PARTIAL, ENTERED, FULL, PROCESSED_ERROR, CANCEL_REQUEST, CANCELLED, CANCELLED_ERROR, REJECTED
	#     }
	# }
	# {
	#     m : string - Method is o.u
	#     o : [
	#         {
	#             i : string - Order id
	#             p : number - Price
	#             oq : number - Original quantity
	#             osq : number - Original secondary quantity
	#             eq : number - Executed quantity
	#             esq : number - Executed secondary quantity
	#             t : string - Order type - MARKET, LIMIT
	#             d : string - Order side - BUY, SELL
	#             sts : integer - Order submission timestamp
	#             uts : integer - Response time of order's last response
	#             s : string - Order state - CREATED, RESERVED, RESERVATION_ERROR, INSERTED, INSERTED_ERROR, RELEASED, RELEASED_ERROR, PARTIAL, ENTERED, FULL, PROCESSED_ERROR, CANCEL_REQUEST, CANCELLED, CANCELLED_ERROR, REJECTED
	#         }
	#     ]
	# }

	def test_unsubscribe_order_stream(self):
		unsub_order_stream = self.websockets_api.unsubscribe_order_stream()
		print(unsub_order_stream)
		self.assertEqual(unsub_order_stream, dict)

	def test_subscribe_order_book_stream(self):
		sub_order_book_stream = self.websockets_api.subscribe_order_book_stream()
		print(sub_order_book_stream)
		self.assertIsInstance(sub_order_book_stream, dict)
		self.assertIsInstance(sub_order_book_stream.m, str)
		self.assertIsInstance(sub_order_book_stream.t, float)
		def test(b):
			self.assertIsInstance(b.p, float)
			self.assertIsInstance(b.q, float)
		if TEST_LISTS:
			for b in sub_order_book_stream.b:
				test(b)
		elif len(sub_order_book_stream.b) > 0:
			test(sub_order_book_stream.b[0])
		def test2(s):
			self.assertIsInstance(s.p, float)
			self.assertIsInstance(s.q, float)
		if TEST_LISTS:
			for s in sub_order_book_stream.s:
				test2(s)
		elif len(sub_order_book_stream.s) > 0:
			test2(sub_order_book_stream.s[0])
		# TODO
		# add updated responses
	# {
	#     m : string - Method is ob.s
	#     t : number - Order book tick number
	#     b : [
	#         {
	#             p : number - Price
	#             q : number - Quantity
	#         }
	#     ]
	#     s : [
	#         {
	#             p : number - Price
	#             q : number - Quantity
	#         }
	#     ]
	# }
	# {
	#     m : string - Method is ob.u
	#     t : number - Order book tick number
	#     b : [
	#         {
	#             p : number - Price
	#             q : number - Quantity
	#         }
	#     ]
	#     s : [
	#         {
	#             p : number - Price
	#             q : number - Quantity
	#         }
	#     ]
	# }

	def test_unsubscribe_order_book_stream(self):
		unsub_order_book_stream = self.websockets_api.unsubscribe_order_book_stream()
		print(unsub_order_book_stream)
		self.assertEqual(unsub_order_book_stream, dict)

	def test_subscribe_trade_stream(self):
		sub_trade_stream = self.websockets_api.subscribe_trade_stream()
		print(sub_trade_stream)
		self.assertIsInstance(sub_trade_stream, dict)
		self.assertIsInstance(sub_trade_stream.m, str)
		self.assertIsInstance(sub_trade_stream.t, list)
		def test(t):
			self.assertIsInstance(t.d, str)
			self.assertIsInstance(t.p, float)
			self.assertIsInstance(t.q, float)
			self.assertIsInstance(t.sq, float)
			self.assertIsInstance(t.ts, int)
		if TEST_LISTS:
			for t in sub_trade_stream.t:
				test(t)
		elif len(sub_trade_stream.t) > 0:
			test(sub_trade_stream.t[0])

	# {
	#     m : string - Method is t.s
	#     t : [
	#         {
	#             d : string - Trade direction - BUY, SELL
	#             p : number - Price
	#             q : number - Quantity
	#             sq : number - Secondary quantity
	#             ts : integer - Timestamp
	#         }
	#     ]
	# }
	# {
	#     m : string - Method is t.u
	#     t : [
	#         {
	#             d : string - Trade direction - BUY, SELL
	#             p : number - Price
	#             q : number - Quantity
	#             sq : number - Secondary quantity
	#             ts : integer - Timestamp
	#         }
	#     ]
	# }

	def test_unsubscribe_order_stream(self):
		unsub_trade_stream = self.websockets_api.unsubscribe_order_stream()
		print(unsub_trade_stream)
		self.assertEqual(unsub_trade_stream, dict)


############################################################################################

if __name__ == '__main__':
	unittest.main()
