#!/usr/bin/env python3
"""
Simple Query - Send a paid query to the API.

Requires:
    - WALLET_PRIVATE_KEY in .env or environment
    - USDC balance on Base mainnet

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
