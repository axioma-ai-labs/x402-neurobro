#!/usr/bin/env python3
"""
Basic Usage Example

Demonstrates how to use the Neurobro x402 API client for crypto analysis queries.

Before running:
    1. Install dependencies: pip install x402 httpx eth-account python-dotenv
    2. Create a .env file with: WALLET_PRIVATE_KEY=0x_your_private_key_here
    3. Ensure your wallet has USDC on Base mainnet

Run:
    python basic_usage.py
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

from client import NeurobroClient

load_dotenv()


async def main() -> None:
    """Run basic API usage examples."""
    # Check for private key
    private_key = os.getenv("WALLET_PRIVATE_KEY")
    if not private_key:
        print("Error: WALLET_PRIVATE_KEY not set in environment")
        print("Create a .env file with: WALLET_PRIVATE_KEY=0x_your_key_here")
        sys.exit(1)

    # Initialize client
    client = NeurobroClient(private_key=private_key)
    print("Neurobro x402 Client initialized")
    print(f"Wallet: {client._account.address}")
    print("-" * 50)

    # Check API health (free endpoint)
    print("\n[1] Checking API health...")
    health = await client.health_async()
    print(f"    Status: {health.status}")
    print(f"    Version: {health.version}")
    print(f"    Service: {health.service}")

    # Send a paid query
    print("\n[2] Sending query (requires USDC payment)...")
    prompt = "What is the current market sentiment for Bitcoin? Give a brief analysis."

    try:
        result = await client.query_async(prompt)
        print(f"    Request ID: {result.request_id}")
        print(f"    Model: {result.model}")
        print(f"\n    Response:\n{result.response}")
    except Exception as e:
        print(f"    Error: {e}")
        print("\n    Make sure your wallet has sufficient USDC on Base mainnet.")


if __name__ == "__main__":
    asyncio.run(main())
