#!/usr/bin/env python3
"""
CLI Query — ask the Neurobro x402 API a question from your terminal.

One-liner interface. Pays $1 USDC per call, prints the answer.

Prereqs:
    WALLET_PRIVATE_KEY in .env, wallet funded with USDC on Base mainnet.

Usage:
    python 03_cli_query.py "Your question here"

Examples:
    python 03_cli_query.py "What is Ethereum?"
    python 03_cli_query.py "Analyze BTC price action this week"
"""

import asyncio
import sys

from neurobro_client import quick_query


async def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python 03_cli_query.py \"Your question\"")
        print("\nExamples:")
        print('  python 03_cli_query.py "What is Ethereum?"')
        print('  python 03_cli_query.py "Top DeFi trends right now"')
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])
    print(f"Q: {prompt}")
    print("-" * 50)

    try:
        # One-shot: initializes client, pays via x402, returns text.
        response = await quick_query(prompt)
        print(response)
    except ValueError as e:
        print(f"Setup error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Query failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())


# ---------------------------------------------------------------------------
# Sample output (illustrative — real responses will vary)
# ---------------------------------------------------------------------------
# $ python 03_cli_query.py "What is Ethereum?"
# Q: What is Ethereum?
# --------------------------------------------------
# Ethereum is a programmable blockchain that launched in 2015 and introduced
# smart contracts — self-executing code deployed onchain. Its native asset,
# ETH, is used to pay for transaction fees ("gas"). Ethereum is the largest
# platform for DeFi, NFTs, and L2 rollups, and has been running on a
# proof-of-stake consensus since the 2022 Merge.
