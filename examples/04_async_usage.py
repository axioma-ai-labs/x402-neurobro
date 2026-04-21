#!/usr/bin/env python3
"""
Async Usage — full async workflow for agents, FastAPI, and event loops.

Runs a free health check, then one paid query — all on the async client.

Prereqs:
    WALLET_PRIVATE_KEY in .env, wallet funded with USDC on Base mainnet.

Usage:
    python 04_async_usage.py
"""

import asyncio
import sys

from neurobro_client import NeurobroClient


async def main() -> None:
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

    # Step 2: Paid query
    print("\n[2] Query (paid)")
    print("-" * 30)

    prompt = "Explain DeFi in one paragraph."
    print(f"Prompt: {prompt}\n")

    try:
        # Pays $1 USDC via x402; awaits the full response.
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


# ---------------------------------------------------------------------------
# Sample output (illustrative — real responses will vary)
# ---------------------------------------------------------------------------
# Wallet: 0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B
# ==================================================
#
# [1] Health Check
# ------------------------------
# Status: healthy
# Version: 1.0.0
#
# [2] Query (paid)
# ------------------------------
# Prompt: Explain DeFi in one paragraph.
#
# Model: grok-4
# Request ID: 2a7c1e45-6b9f-4d11-8c3d-4e90fd2b1a08
#
# Response:
# DeFi ("decentralized finance") is a set of blockchain-based financial
# services — lending, trading, derivatives, yield — that run on public
# smart-contract platforms without traditional intermediaries. Protocols
# like Aave, Uniswap, and MakerDAO replace banks and exchanges with
# open, composable code, letting anyone with a wallet interact directly.
#
# ==================================================
# Done.
