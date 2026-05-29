import sys
import os
from wallet_engine import WalletEngine
from chain_modules import EVMChain, BitcoinChain, TronChain
import json

class CryptoConsole:
    def __init__(self):
        self.wallet_engine = WalletEngine()
        self.wallets = {}
        self.current_mnemonic = None

    def clear_screen(self):
        os.system('clear')

    def main_menu(self):
        while True:
            self.clear_screen()
            print("=== Multi-Chain Crypto Console ===")
            print("1. Create New Wallet")
            print("2. Import Wallet (Mnemonic)")
            print("3. View Wallets & Balances")
            print("4. Send Cryptocurrency")
            print("5. Smart Contract Operations")
            print("6. Exit")
            
            choice = input("\nSelect an option: ")
            
            if choice == '1':
                self.create_wallet()
            elif choice == '2':
                self.import_wallet()
            elif choice == '3':
                self.view_wallets()
            elif choice == '4':
                self.send_crypto()
            elif choice == '5':
                self.contract_ops()
            elif choice == '6':
                sys.exit()

    def create_wallet(self):
        self.current_mnemonic = self.wallet_engine.create_mnemonic()
        self.wallets = self.wallet_engine.derive_wallets(self.current_mnemonic)
        print(f"\nNew Mnemonic Created: {self.current_mnemonic}")
        print("\nDerived Addresses:")
        for chain, data in self.wallets.items():
            print(f"{chain}: {data['address']}")
        input("\nPress Enter to continue...")

    def import_wallet(self):
        mnemonic = input("\nEnter your mnemonic phrase: ")
        try:
            self.wallets = self.wallet_engine.derive_wallets(mnemonic)
            self.current_mnemonic = mnemonic
            print("\nWallet Imported Successfully!")
            input("\nPress Enter to continue...")
        except Exception as e:
            print(f"Error: {e}")
            input("\nPress Enter to continue...")

    def view_wallets(self):
        if not self.wallets:
            print("\nNo wallet loaded.")
        else:
            print("\nYour Wallets:")
            for chain, data in self.wallets.items():
                print(f"{chain}: {data['address']}")
                # In a real app, we would fetch balances here
        input("\nPress Enter to continue...")

    def send_crypto(self):
        if not self.wallets:
            print("\nNo wallet loaded.")
            input("\nPress Enter to continue...")
            return
        
        print("\n--- Send Crypto ---")
        print("1. EVM (ETH/BSC/Polygon)")
        print("2. Bitcoin")
        print("3. Tron")
        choice = input("Select chain: ")
        
        to_address = input("Enter recipient address: ")
        amount = float(input("Enter amount: "))
        
        try:
            if choice == '1':
                rpc = input("Enter RPC URL (default: https://cloudflare-eth.com): ") or "https://cloudflare-eth.com"
                chain = EVMChain(rpc)
                tx_hash = chain.send_transaction(self.wallets['EVM']['private_key'], to_address, amount)
                print(f"Transaction Sent! Hash: {tx_hash}")
            elif choice == '2':
                chain = BitcoinChain()
                tx_hash = chain.send_transaction(self.wallets['BTC']['private_key'], to_address, amount)
                print(f"Transaction Sent! Hash: {tx_hash}")
            elif choice == '3':
                chain = TronChain()
                result = chain.send_transaction(self.wallets['TRX']['private_key'], to_address, amount)
                print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPress Enter to continue...")

    def contract_ops(self):
        if not self.wallets:
            print("\nNo wallet loaded.")
            input("\nPress Enter to continue...")
            return
            
        print("\n--- Smart Contract Operations ---")
        print("1. Deploy Contract")
        print("2. Call Function (Read)")
        choice = input("Select option: ")
        
        rpc = input("Enter RPC URL: ") or "https://cloudflare-eth.com"
        from chain_modules import SmartContractEngine
        from web3 import Web3
        w3 = Web3(Web3.HTTPProvider(rpc))
        engine = SmartContractEngine(w3)
        
        if choice == '1':
            abi = json.loads(input("Enter ABI (JSON): "))
            bytecode = input("Enter Bytecode: ")
            tx_hash = engine.deploy_contract(self.wallets['EVM']['private_key'], abi, bytecode)
            print(f"Deployment Sent! Hash: {tx_hash}")
        elif choice == '2':
            address = input("Enter Contract Address: ")
            abi = json.loads(input("Enter ABI (JSON): "))
            func = input("Enter Function Name: ")
            result = engine.call_contract(address, abi, func)
            print(f"Result: {result}")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    console = CryptoConsole()
    console.main_menu()
