from web3 import Web3
from tronpy import Tron
from bit import Key
import requests

class EVMChain:
    def __init__(self, rpc_url):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

    def get_balance(self, address):
        balance_wei = self.w3.eth.get_balance(address)
        return self.w3.from_wei(balance_wei, 'ether')

    def send_transaction(self, private_key, to_address, amount_ether):
        account = self.w3.eth.account.from_key(private_key)
        nonce = self.w3.eth.get_transaction_count(account.address)
        tx = {
            'nonce': nonce,
            'to': to_address,
            'value': self.w3.to_wei(amount_ether, 'ether'),
            'gas': 21000,
            'gasPrice': self.w3.eth.gas_price,
            'chainId': self.w3.eth.chain_id
        }
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return self.w3.to_hex(tx_hash)

class BitcoinChain:
    def __init__(self, network='testnet'):
        self.network = network

    def get_balance(self, wif):
        key = Key(wif)
        return key.get_balance('btc')

    def send_transaction(self, wif, to_address, amount_btc):
        key = Key(wif)
        return key.send([(to_address, amount_btc, 'btc')])

class TronChain:
    def __init__(self, network='nile'):
        self.client = Tron(network=network)

    def get_balance(self, address):
        return self.client.get_account_balance(address)

    def send_transaction(self, private_key, to_address, amount_trx):
        try:
            txn = (
                self.client.trx.transfer(self.client.get_address_from_private_key(private_key), to_address, int(amount_trx * 1_000_000))
                .build()
                .sign(private_key)
            )
            return txn.broadcast().wait()
        except Exception as e:
            return f"Error: {e}"

class SmartContractEngine:
    def __init__(self, w3_instance):
        self.w3 = w3_instance

    def deploy_contract(self, private_key, abi, bytecode, args=[]):
        account = self.w3.eth.account.from_key(private_key)
        contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        construct_txn = contract.constructor(*args).build_transaction({
            'from': account.address,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'gasPrice': self.w3.eth.gas_price
        })
        signed_txn = self.w3.eth.account.sign_transaction(construct_txn, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return self.w3.to_hex(tx_hash)

    def call_contract(self, contract_address, abi, function_name, args=[]):
        contract = self.w3.eth.contract(address=contract_address, abi=abi)
        return getattr(contract.functions, function_name)(*args).call()
