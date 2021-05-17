# Changelog

**0.1.0 : Testing : 4/22/2021**
	- test_bot.py -> updated original
	**4/25**
	- python unittests: test_nicehash_*public, private, websockets.py
	**0.1.1 : 5/3/2021**
	- package fix
	- public & private client tests mostly OK
	- i totally know semantic versioning
	**0.1.2 : 5/16/2021**
	- start websocket tests


## Dev Notes

Currently integrating with the (NiceHash REST API)[https://www.nicehash.com/docs/rest]

websockets require ssl?

### Bugs:

**/main/api/v2/hashpower/orders/fixedPrice**
5/3/2021
returns: `400: Bad Request b'{"error_id":"c071d84e-86c7-4508-93f5-109435a6c076","errors":[{"code":5012,"message":"Hashpower order fixed speed limit is too big"}]}'`

API values tested at test.nicehash API site return mostly green (accepted) values and then sometimes still the same numbers used again 5 minutes later nothing works at all. Requires further eliminating of variables.


**fucking /main/api/v2/accounting/account2/{currency}**
5/3/2021
the query parameter string needs empty lists to be turned into "" aka empty space for proper responses
doing a .replace at the request method does not fucking work for whatever reason as it turns the query string into the exact same
string as doing the check at the source function ergo:

GET https://api-test.nicehash.com/main/api/v2/accounting/deposits/TBTC?statuses=&op=LT&timestamp=1620173924485&page=0&size=100
query: statuses=&op=LT&timestamp=&page=0&size=100
{'list': [], 'pagination': {'size': 100, 'page': 0, 'totalPageCount': 1}}

GET https://api-test.nicehash.com/main/api/v2/accounting/deposits/TBTC?statuses=&op=LT&timestamp=1620174158976&page=0&size=100
query: statuses=&op=LT&timestamp=&page=0&size=100

just doing the check at the source and moving on

