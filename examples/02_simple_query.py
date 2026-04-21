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
        print(f"Model: {result.model}")
        print(f"Request ID: {result.request_id}")
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
# Model: grok-4
# Request ID: 8f3c2a91-2e04-4b6d-9f1c-7c0d6b3e8d21
#
# Response:
# Bitcoin (BTC) is a decentralized digital currency launched in 2009 by the
# pseudonymous Satoshi Nakamoto. It runs on a peer-to-peer network secured
# by proof-of-work mining, with a fixed supply cap of 21 million coins. It
# is the largest crypto asset by market cap and is widely used as a store
# of value and settlement layer.
