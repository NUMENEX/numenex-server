from web3 import Web3

w3 = Web3(Web3.WebsocketProvider("wss://bsc-rpc.publicnode.com"))


def get_txn(txn_hash):
    txn_details = w3.eth.get_transaction(txn_hash)
    print(txn_details)
