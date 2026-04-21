#!/usr/bin/env python3
"""
Retry logic — transparent retries for transient failures.

Uses exponential backoff on connection errors, timeouts, and 5xx
responses. 4xx errors are not retried — they signal a real problem.

Requires WALLET_PRIVATE_KEY in .env and USDC on Base mainnet.

Usage:
    python 08_retry_logic.py
"""

import asyncio
import sys
from typing import TypeVar

import httpx

from neurobro_client import NeurobroClient, QueryResult

T = TypeVar("T")


async def with_retry(
    func,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
) -> T:
    """Execute an async function with exponential backoff retry."""
    last_error: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            return await func()

        except (httpx.ConnectError, httpx.TimeoutException) as e:
            last_error = e
            if attempt == max_attempts:
                break

            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            print(f"  Attempt {attempt} failed: {type(e).__name__}")
            print(f"  Retrying in {delay:.1f}s...")
            await asyncio.sleep(delay)

        except httpx.HTTPStatusError as e:
            if e.response.status_code >= 500:
                last_error = e
                if attempt == max_attempts:
                    break

                delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                print(f"  Attempt {attempt} failed: HTTP {e.response.status_code}")
                print(f"  Retrying in {delay:.1f}s...")
                await asyncio.sleep(delay)
            else:
                raise

    raise last_error  # type: ignore


async def query_with_retry(
    client: NeurobroClient,
    prompt: str,
    max_attempts: int = 3,
) -> QueryResult:
    """Send a query with automatic retry on transient failures."""
    return await with_retry(
        lambda: client.query_async(prompt),
        max_attempts=max_attempts,
    )


async def main() -> None:
    try:
        client = NeurobroClient()
    except ValueError as e:
        print(f"Setup error: {e}")
        sys.exit(1)

    print(f"Wallet: {client.wallet_address}")
    print("=" * 50)

    prompt = "What's the current alpha on the markets?"
    print(f"\nQuery: {prompt}")
    print("-" * 50)

    try:
        result = await query_with_retry(client, prompt, max_attempts=3)
        print(f"\nResponse:\n{result.text}")

    except httpx.HTTPStatusError as e:
        print(f"\nFailed: HTTP {e.response.status_code}")
        if e.response.status_code == 402:
            print("Ensure wallet has USDC on Base mainnet")
        sys.exit(1)

    except Exception as e:
        print(f"\nFailed after retries: {e}")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("Done")


if __name__ == "__main__":
    asyncio.run(main())


# Example output:
#
# Wallet: 0xA1b2C3d4E5F67890a1b2c3D4e5f6789012345678
# ==================================================
#
# Query: What's the current alpha on the markets?
# --------------------------------------------------
#
# Response:
# Markets are hot around the Solana and Base ecosystems — memecoin flows
# and onchain consumer apps are driving most of the retail activity.
# AI-adjacent tokens and restaking names remain the other two corners
# of attention. Majors (BTC, ETH) are range-bound, so the alpha is in
# rotations across these narratives rather than beta exposure.
#
# ==================================================
# Done
#
# Example with a transient 503 on the first attempt:
#
#   Attempt 1 failed: HTTP 503
#   Retrying in 1.0s...
#   Attempt 2 failed: HTTP 503
#   Retrying in 2.0s...
# (succeeds on third attempt)
