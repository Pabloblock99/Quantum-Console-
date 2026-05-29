# Multi-Chain Crypto Console

A production-ready CLI console for managing wallets, processing smart contracts, and sending/receiving cryptocurrency across multiple blockchains.

## Features
- **Multi-Chain Support**: EVM (Ethereum, BSC, Polygon), Bitcoin, Tron, Solana.
- **HD Wallet Engine**: Create and import wallets using BIP39 mnemonics.
- **Smart Contract Processing**: Deploy and interact with EVM smart contracts.
- **Transaction Engine**: Send and receive crypto across supported chains.
- **Secure**: Local private key management (never leaves your machine).

## Installation
```bash
pip install web3 bip-utils base58 mnemonic cryptography requests tronpy bit solana monero pycryptodome eth-account
```

## Usage
Run the console:
```bash
python3 main.py
```

## Testing
Run the test suite:
```bash
python3 test_suite.py
```
