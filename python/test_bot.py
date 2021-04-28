import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

host = os.environ.get("HOST_TEST")
organisation_id = os.environ.get("ORGANIZATION_ID")
key = os.environ.get("KEY")
secret = os.environ.get("SECRET")

############################################
# PUBLIC FUNCTIONS


# External miner

# /main/api/v2/mining/external/{btcAddress}/rigs/activeWorkers

active_workers = public_api.get_active_workers(ADDRESS)
print(active_workers)

# /main/api/v2/mining/external/{btcAddress}/rigs/stats/algo

algo_statistics = public_api.get_algo_statistics(ADDRESS, ALGORITHM)
print(algo_statistics)

# /main/api/v2/mining/external/{btcAddress}/rigs/stats/unpaid

unpaid_statistics = public_api.get_unpaid_statistics(ADDRESS)
print(unpaid_statistics)

# /main/api/v2/mining/external/{btcAddress}/rigs/withdrawals

withdrawals = public_api.get_withdrawals(ADDRESS)
print(withdrawals)

# /main/api/v2/mining/external/{btcAddress}/rigs2

rig_statuses = public_api.get_rig_statuses(ADDRESS)
print(rig_statuses)


# Hashpower public

# /main/api/v2/hashpower/orderBook

hashpower_orderbook = public_api.get_hashpower_orderbook(ALGORITHM)
print(hashpower_orderbook)

# /main/api/v2/hashpower/orders/fixedPrice

price_request = public_api.fixed_price_request()
print(price_request)

# /main/api/v2/hashpower/orders/summaries

hashpower_summaries = public_api.get_hashpower_summaries()
print(hashpower_summaries)

# /main/api/v2/hashpower/orders/summary

hashpower_orders_summary = public_api.get_hashpower_orders_summary(ALGORITHM, MARKET)
print(hashpower_orders_summary)

# /main/api/v2/public/algo/history

algo_history = public_api.get_algo_history(ALGORITHM)
print(algo_history)

# /main/api/v2/public/buy/info

buy_info = public_api.buy_info()
print(buy_info)

# /main/api/v2/public/orders

orders = public_api.get_orders()
print(orders)

# /main/api/v2/public/simplemultialgo/info

multialgo_info = public_api.get_multialgo_info()
print(multialgo_info)

# /main/api/v2/public/stats/global/24h

global_stats_24 = public_api.get_global_stats_24()
print(global_stats_24)

# /main/api/v2/public/stats/global/current

current_global_stats = public_api.get_current_global_stats()
print(current_global_stats)


# Public

# /main/api/v2/mining/algorithms

algorithms = public_api.get_algorithms()
print(algorithms)

# /main/api/v2/public/currencies

currencies = public_api.get_currencies()
print(currencies)

# /main/api/v2/public/service/fee/info

fee_rules = public_api.get_fee_rules()
print(fee_rules)

# /api/v2/enum/countries

countries = public_api.get_countries()
print(countries)

# /api/v2/enum/kmCountries

km_countries = public_api.get_km_countries()
print(km_countries)

# /api/v2/enum/permissions

permissions = public_api.get_permissions()
print(permissions)

# /api/v2/enum/xchCountries

xch_countries = public_api.get_xch_countries()
print(xch_countries)

# /api/v2/system/flags

api_flags = public_api.get_api_flags()
print(api_flags)

public_api.print_api_flags()

# /api/v2/time

server_time = public_api.get_server_time()
print(server_time)


# Exchange public

# /exchange/api/v2/info/candlesticks

# TODO
# FROM_S, TO_S, RESOLUTION
candlesticks = public_api.get_candlesticks(MARKET, FROM_S, TO_S, RESOLUTION)
print(candlesticks)

# /exchange/api/v2/info/marketStats

exchange_statistics = public_api.get_exchange_statistics()
print(exchange_statistics)

# /exchange/api/v2/info/prices

current_prices = public_api.get_current_prices()
print(current_prices)

# /exchange/api/v2/info/status

exchange_markets_info = public_api.get_exchange_markets_info()
print(exchange_markets_info)

# /exchange/api/v2/info/trades

trades = public_api.get_trades(MARKET)
print(trades)

# /exchange/api/v2/orderbook

orderbook = public_api.get_exchange_orderbook(MARKET)
print(orderbook)



























############################################
# PRIVATE FUNCTIONS


# Accounting

# /main/api/v2/accounting/account2/{currency}

accounts_for_currency = public_api.get_accounts_for_currency(CURRENCY)
print(accounts_for_currency)

# /main/api/v2/accounting/accounts2

accounts = public_api.get_accounts()
print(accounts)

# /main/api/v2/accounting/activity/{currency}

account_activity = public_api.get_account_activity(CURRENCY)
print(account_activity)

# /main/api/v2/accounting/depositAddresses

deposit_addresses = public_api.get_deposit_addresses()
print(deposit_addresses)

# /main/api/v2/accounting/deposits/{currency}

deposits_for_currency = public_api.get_deposits_for_currency(CURRENCY)
print(deposits_for_currency)

# /main/api/v2/accounting/deposits2/{currency}/{id}

deposits_for_currency_by_id = public_api.get_deposits_for_currency_by_id(CURRENCY, ID)
print(deposits_for_currency_by_id)

# /main/api/v2/accounting/exchange/{id}/trades

order_transactions_by_id = public_api.get_order_transactions_by_id(ID, MARKET)
print(order_transactions_by_id)

# /main/api/v2/accounting/hashpower/{id}/transactions

hashpower_order_transactions_by_id = public_api.get_hashpower_order_transactions_by_id(ID)
print(hashpower_order_transactions_by_id)

# /main/api/v2/accounting/hashpowerEarnings/{currency}

hashpower_earnings_for_currency = public_api.get_hashpower_earnings_for_currency(CURRENCY)
print(hashpower_earnings_for_currency)

# /main/api/v2/accounting/transaction/{currency}/{transactionId}

transaction_for_currency_by_id = public_api.get_transaction_for_currency_by_id(CURRENCY, ID)
print(transaction_for_currency_by_id)

# /main/api/v2/accounting/transactions/{currency}

transactions_for_currency = public_api.get_transactions_for_currency(CURRENCY)
print(transactions_for_currency)

# /main/api/v2/accounting/withdrawal

withdrawal = public_api.withdraw_request(CURRENCY, WITHDRAWAL_AMOUNT, WHITELISTED_WITHDRAWAL_ADDRESS_ID)
print(withdrawal)

# /main/api/v2/accounting/withdrawal/{currency}/{id}

delete_withdrawal = public_api.delete_withdrawal(WITHDRAWAL_ID)
print(delete_withdrawal)

# /main/api/v2/accounting/withdrawal2/{currency}/{id}

withdrawal_for_currency_by_id = public_api.get_withdrawal_for_currency_by_id(CURRENCY, WITHDRAWAL_ID)
print(withdrawal_for_currency_by_id)

# /main/api/v2/accounting/withdrawalAddress/{id}

withdrawal_address_by_id = public_api.get_withdrawal_address_by_id(WITHDRAWAL_ID)
print(withdrawal_address_by_id)

# /main/api/v2/accounting/withdrawalAddresses

withdrawal_addresses = public_api.get_withdrawal_addresses(CURRENCY)
print(withdrawal_addresses)

# /main/api/v2/accounting/withdrawals/{currency}

withdrawals_for_currency = public_api.get_withdrawals_for_currency(CURRENCY, STATUSES, OP, TIMESTAMP, PAGE, SIZE)
print(withdrawals_for_currency)


# Hashpower private

# /main/api/v2/hashpower/myOrders

active_orders = private_api.get_my_active_orders(ALGORITHM, MARKET, LIMIT)
print(active_orders)
# TODO
ORDER_ID = None

# /main/api/v2/hashpower/order

standard_hashpower_order = private_api.create_standard_hashpower_order(MARKET, ALGORITHM, PRICE, LIMIT, AMOUNT, POOL_ID)
print(standard_hashpower_order)

fixed_hashpower_order = private_api.create_fixed_hashpower_order(MARKET, ALGORITHM, PRICE, LIMIT, AMOUNT, POOL_ID)
print(fixed_hashpower_order)

# /main/api/v2/hashpower/order/{id}

order_details = private_api.get_order_details(ORDER_ID)
print(order_details)

# /main/api/v2/hashpower/order/{id}

hashpower_order = private_api.cancel_hashpower_order(ORDER_ID)
print(hashpower_order)

# /main/api/v2/hashpower/order/{id}/refill

hashpower_order = private_api.refill_hashpower_order(ORDER_ID, AMOUNT)
print(hashpower_order)

# /main/api/v2/hashpower/order/{id}/stats

order_statistics = private_api.get_order_statistics(ORDER_ID)
print(order_statistics)

# /main/api/v2/hashpower/order/{id}/updatePriceAndLimit

set_order = private_api.set_price_hashpower_order(ORDER_ID, PRICE, ALGORITHM)
print(set_order)
set_order = private_api.set_limit_hashpower_order(ORDER_ID, LIMIT, ALGORITHM)
print(set_order)
set_order = private_api.set_price_and_limit_hashpower_order(ORDER_ID, PRICE, LIMIT, ALGORITHM)
print(set_order)

# /main/api/v2/hashpower/orders/calculateEstimateDuration

order_duration = private_api.estimate_order_duration(ALGORITHM, order_type=ORDER_TYPE, price=PRICE, limit=LIMIT, amount=AMOUNT)
print(order_duration)


# Miner private

# /main/api/v2/mining/groups/list

groups = private_api.get_groups()
print(groups)
# TODO
RIG_ID = None

# /main/api/v2/mining/miningAddress

mining_address = private_api.get_mining_address()
print(mining_address)

# /main/api/v2/mining/rig/stats/algo

rig_algo_stats = private_api.get_rig_algo_stats()
print(rig_algo_stats)

# /main/api/v2/mining/rig/stats/unpaid

rig_unpaid_stats = private_api.get_rig_unpaid_stats()
print(rig_unpaid_stats)

# /main/api/v2/mining/rig2/{rigId}

rig_by_id = private_api.get_rig_by_id(RIG_ID)
print(rig_by_id)

# /main/api/v2/mining/rigs/activeWorkers

active_workers = private_api.get_active_workers()
print(active_workers)

# /main/api/v2/mining/rigs/payouts

payouts = private_api.get_payouts()
print(payouts)

# /main/api/v2/mining/rigs/stats/algo

algo_statistics = private_api.get_algo_statistics()
print(algo_statistics)

# /main/api/v2/mining/rigs/stats/unpaid

unpaid_statistics = private_api.get_unpaid_statistics()
print(unpaid_statistics)

# /main/api/v2/mining/rigs/status2

status = private_api.update_status(RIG_ACTION, rig_id=RIG_ID)
print(status)
status = private_api.update_status(RIG_ACTION, group_name="test")
print(status)

# /main/api/v2/mining/rigs2

rigs = private_api.get_rigs()
print(rigs)


# Pools

# /main/api/v2/pool

pool = private_api.create_pool(POOL_NAME, ALGORITHM, pool_host=POOL_HOST, pool_port=POOL_PORT, username=POOL_USERNAME, password=POOL_PASSWORD)
print(pool)
# TODO
POOL_ID = None

# /main/api/v2/pool/{poolId}

pool = private_api.get_pool(POOL_ID)
print(pool)

# /main/api/v2/pool/{poolId}

delete_pool = private_api.delete_pool(POOL_ID)
print(delete_pool)

# /main/api/v2/pools

my_pools = private_api.get_my_pools()
print(my_pools)

# /main/api/v2/pools/verify

verify_pools = private_api.verify_pool(market=MARKET, algorithm=ALGORITHM, pool_host=POOL_HOST, pool_port=POOL_PORT, username=USERNAME, password=PASSWORD)
print(verify_pools)


# Exchange private

# /exchange/api/v2/info/cancelAllOrders

canceled_orders = private_api.cancel_all_orders(market=MARKET, side=SIDE)
print(canceled_orders)

# /exchange/api/v2/info/fees/status

fee_status = private_api.get_fee_status()
print(fee_status)

# TODO
ORDER_ID = None

# /exchange/api/v2/info/myOrder

order = private_api.get_my_order(MARKET, ORDER_ID)
print(order)

# /exchange/api/v2/info/myOrders

orders = private_api.get_my_orders(MARKET)
print(orders)

# /exchange/api/v2/info/myTrades

trades = private_api.get_my_trades(MARKET)
print(trades)

# /exchange/api/v2/info/orderTrades

order_trades = private_api.get_trades_for_order(MARKET, ORDER_ID)
print(order_trades)

# /exchange/api/v2/order

exchange_limit_order = private_api.create_exchange_limit_order(MARKET, SIDE, QUANTITY, PRICE)
print(exchange_limit_order)
exchange_buy_market_order = private_api.create_exchange_buy_market_order(MARKET, QUANTITY, SEC_QUANTITY)
print(exchange_buy_market_order)
exchange_sell_market_order = private_api.create_exchange_sell_market_order(MARKET, QUANTITY, min_SEC_QUANTITY)
print(exchange_sell_market_order)

# /exchange/api/v2/order

canceled_order = private_api.cancel_exchange_order(MARKET, ORDER_ID)
print(canceled_order)




# websockets

sub_candlestick_stream = private_api.subscribe_candlestick_stream(RESOLUTION)
print(sub_candlestick_stream)

unsub_candlestick_stream = private_api.unsubscribe_candlestick_stream(RESOLUTION)
print(canceled_order)

sub_trade_stream = private_api.subscribe_trade_stream(MARKET, ORDER_ID)
print(sub_trade_stream)

unsub_trade_stream = private_api.unsubscribe_trade_stream(RESOLUTION)
print(unsub_trade_stream)

canceled_orders = private_api.cancel_all_orders()
print(canceled_orders)

canceled_order = private_api.cancel_order()
print(canceled_order)

# TODO
MESSAGE_ID = None

limit_order = private_api.create_limit_order(MESSAGE_ID, SIDE, QUANTITY, PRICE)
print(limit_order)

market_buy_order = private_api.create_buy_market_order(MESSAGE_ID, QUANTITY_QUOTE)
print(market_order)

market_sell_order = private_api.create_sell_market_order(MESSAGE_ID, QUANTITY)
print(market_sell_order)

sub_order_stream = private_api.subscribe_order_stream()
print(sub_order_stream)

unsub_order_stream = private_api.unsubscribe_order_stream()
print(unsub_order_stream)

sub_order_book_stream = private_api.subscribe_order_book_stream()
print(sub_order_book_stream)

unsub_order_book_stream = private_api.unsubscribe_order_book_stream()
print(unsub_order_book_stream)

sub_trade_stream = private_api.subscribe_trade_stream()
print(sub_trade_stream)

unsub_trade_stream = private_api.unsubscribe_order_stream()
print(unsub_trade_stream)

