#!/usr/bin/env python3
"""
Quick Query Example

A minimal example showing the simplest way to query the Neurobro API.

Before running:
    1. pip install x402 httpx eth-account python-dotenv
    2. Set WALLET_PRIVATE_KEY in .env or environment

Run:
    python quick_query.py "Your question here"
"""

import asyncio
import sys

from client import query


async def main() -> None:
    """Run a quick query from command line argument."""
    if len(sys.argv) < 2:
        print("Usage: python quick_query.py \"Your crypto question here\"")
        print()
        print("Example:")
        print('  python quick_query.py "What are the top DeFi trends right now?"')
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])
    print(f"Query: {prompt}")
    print("-" * 50)

    try:
        response = await query(prompt)
        print(response)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
