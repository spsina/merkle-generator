from web3 import Web3


def get_web3_object() -> Web3:

    url = "https://rpc.ankr.com/fantom"

    w3 = Web3(Web3.HTTPProvider(url))
    if w3.isConnected():
        print("Connected to Fantom")
        return w3
    else:
        raise Exception("Could not connect to provider ", url)
