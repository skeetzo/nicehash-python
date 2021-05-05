**nicehash-python**
fork of nicehash/rest-clients-demo with updated python client

# rest-clients-demo

### Source

- [python](https://github.com/nicehash/rest-clients-demo/blob/master/python/nicehash.py)

### TEST environment

Generate Api key and Secret for test platform on:

https://test.nicehash.com (User / Settings / API Keys)
Organization ID is displayed just above "+ Create new API key" button.

Use https://api-test.nicehash.com for API domain.

The entire platform runs on testnet. This means that you don’t have to use your own funds to test the platform. This is the opportunity to familiarize yourself with the new system, place hash-power orders and try trading without spending any real money.

![](https://raw.githubusercontent.com/nicehash/rest-clients-demo/master/generate_key.gif)

### PRODUCTION environment

To use production just generate key the same way on https://www.nicehash.com and use https://api2.nicehash.com for API domain.

### API docs
Can be found here: https://docs.nicehash.com/

### DEV environment

Tested using python3.8. More notes on testing in changelog. Package is still under development as some API functionality is incomplete. 

Install test dependencies: `python3.8 setup.py install -e [.dev]`
Run some tests: `python3.8 -m unittest tests.test_nicehash_public`
Run all tests: `python3.8 -m unittest discover -s ./tests`