#!/usr/bin/env python3
"""
Async Usage - Full async workflow example.

Demonstrates:
    - Async client initialization
    - Health check before queries
    - Multiple async queries

Requires:
    - WALLET_PRIVATE_KEY in .env or environment
    - USDC balance on Base mainnet

Usage:
    python 04_async_usage.py
"""

import asyncio
import sys

from neurobro_client import NeurobroClient


async def main() -> None:
    # Initialize client
    try:
        client = NeurobroClient()
    except ValueError as e:
        print(f"Setup error: {e}")
        sys.exit(1)

    print(f"Wallet: {client.wallet_address}")
    print("=" * 50)

    # Step 1: Health check (free)
    print("\n[1] Health Check")
    print("-" * 30)
    status = await client.health_async()
    print(f"Status: {status.status}")
    print(f"Version: {status.version}")

    if not status.is_healthy:
        print("API is not healthy. Exiting.")
        sys.exit(1)

    # Step 2: Send query (paid)
    print("\n[2] Query (paid)")
    print("-" * 30)

    prompt = "Explain DeFi in one paragraph."
    print(f"Prompt: {prompt}\n")

    try:
        result = await client.query_async(prompt)
        print(f"Model: {result.model}")
        print(f"Request ID: {result.request_id}")
        print(f"\nResponse:\n{result.text}")

    except Exception as e:
        print(f"Query failed: {e}")
        print("\nEnsure your wallet has USDC on Base mainnet.")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
