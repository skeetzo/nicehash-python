#!/usr/bin/env bash
python3.8 -m unittest tests.test_nicehash_public
python3.8 -m unittest tests.test_nicehash_private
python3.8 -m unittest tests.test_nicehash_websockets

python3.8 -m unittest tests.test_nicehash_websockets.TestNiceHashWebsockets.test_cancel_all_orders