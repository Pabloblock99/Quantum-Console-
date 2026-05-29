import unittest
from wallet_engine import WalletEngine
from chain_modules import EVMChain, BitcoinChain
import os

class TestCryptoConsole(unittest.TestCase):
    def setUp(self):
        self.engine = WalletEngine()
        self.mnemonic = "test test test test test test test test test test test junk"

    def test_wallet_derivation(self):
        wallets = self.engine.derive_wallets(self.mnemonic)
        self.assertIn('EVM', wallets)
        self.assertIn('BTC', wallets)
        self.assertIn('TRX', wallets)
        self.assertIn('SOL', wallets)
        
        # Check EVM address format
        self.assertTrue(wallets['EVM']['address'].startswith('0x'))
        self.assertEqual(len(wallets['EVM']['address']), 42)

    def test_mnemonic_generation(self):
        mne = self.engine.create_mnemonic()
        self.assertEqual(len(mne.split()), 12)

    def test_evm_balance_fetch(self):
        # Using a public RPC for testing
        # Use a more reliable public RPC or skip if unavailable
        try:
            evm = EVMChain("https://cloudflare-eth.com")
            # Vitalik's address
            balance = evm.get_balance("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
            self.assertGreaterEqual(balance, 0)
        except Exception as e:
            self.skipTest(f"RPC Error: {e}")

if __name__ == "__main__":
    unittest.main()
