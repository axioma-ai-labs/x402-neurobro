#!/usr/bin/env python3
"""
CLI query — ask the API a question from your terminal.

Requires WALLET_PRIVATE_KEY in .env and USDC on Base mainnet.

Usage:
    python 03_cli_query.py "Your question"

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


# Example output:
#
# $ python 03_cli_query.py "What is Ethereum?"
# Q: What is Ethereum?
# --------------------------------------------------
# Ethereum is a programmable blockchain launched in 2015 that introduced
# smart contracts — self-executing code deployed onchain. Its native asset
# ETH pays for transaction fees ("gas"). Ethereum hosts the majority of
# DeFi, NFTs, and L2 rollups, and runs on proof-of-stake consensus since
# the 2022 Merge.
