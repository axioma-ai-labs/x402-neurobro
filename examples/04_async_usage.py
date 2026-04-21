#!/usr/bin/env python3
"""
Async workflow — health check, then one paid query, all async.

For agents, FastAPI handlers, and existing event loops.

Requires WALLET_PRIVATE_KEY in .env and USDC on Base mainnet.

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

    print("\n[1] Health Check")
    print("-" * 30)
    status = await client.health_async()
    print(f"Status: {status.status}")
    print(f"Version: {status.version}")

    if not status.is_healthy:
        print("API is not healthy. Exiting.")
        sys.exit(1)

    print("\n[2] Query (paid)")
    print("-" * 30)

    prompt = "What are the top crypto narratives driving the market right now?"
    print(f"Prompt: {prompt}\n")

    try:
        result = await client.query_async(prompt)
        print(f"\nResponse:\n{result.text}")

    except Exception as e:
        print(f"Query failed: {e}")
        print("\nEnsure your wallet has USDC on Base mainnet.")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())


# Example output:
#
# Wallet: 0xA1b2C3d4E5F67890a1b2c3D4e5f6789012345678
# ==================================================
#
# [1] Health Check
# ------------------------------
# Status: healthy
# Version: 1.0.0
#
# [2] Query (paid)
# ------------------------------
# Prompt: What are the top crypto narratives driving the market right now?
#
# Response:
# Three narratives are pulling flows this cycle: (1) Solana and Base
# ecosystems absorbing retail activity with cheap, fast execution and a
# growing memecoin + consumer-app flywheel; (2) AI-adjacent tokens
# riding the agentic-infrastructure wave; and (3) real-world assets
# (RWAs) — tokenized treasuries and credit — attracting institutional
# desks looking for onchain yield.
#
# ==================================================
# Done.
