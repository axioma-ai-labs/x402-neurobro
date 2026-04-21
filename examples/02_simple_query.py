#!/usr/bin/env python3
"""
Simple query — the smallest working paid integration.

Asks one question, pays $1 USDC, prints the answer.

Requires WALLET_PRIVATE_KEY in .env and USDC on Base mainnet.

Usage:
    python 02_simple_query.py
"""

import sys

from neurobro_client import NeurobroClient


def main() -> None:
    try:
        client = NeurobroClient()
    except ValueError as e:
        print(f"Setup error: {e}")
        print("\nCreate .env file with: WALLET_PRIVATE_KEY=0x...")
        sys.exit(1)

    print(f"Wallet: {client.wallet_address}")
    print("-" * 50)

    prompt = "What is Bitcoin? Give a brief explanation."
    print(f"Query: {prompt}\n")

    try:
        result = client.query(prompt)
        print(f"\nResponse:\n{result.text}")

    except Exception as e:
        print(f"Query failed: {e}")
        print("\nEnsure your wallet has USDC on Base mainnet.")
        sys.exit(1)


if __name__ == "__main__":
    main()


# Example output:
#
# Wallet: 0xA1b2C3d4E5F67890a1b2c3D4e5f6789012345678
# --------------------------------------------------
# Query: What is Bitcoin? Give a brief explanation.
#
# Response:
# Bitcoin (BTC) is a decentralized digital currency launched in 2009 by the
# pseudonymous Satoshi Nakamoto. It runs on a peer-to-peer network secured
# by proof-of-work mining, with a fixed supply cap of 21 million coins. It
# is the largest crypto asset by market cap and is widely used as a store
# of value and settlement layer.
