#!/usr/bin/env python3
"""
Retry Logic - Handle transient failures with retries.

Demonstrates:
    - Exponential backoff
    - Configurable retry attempts
    - Handling transient errors

Requires:
    - WALLET_PRIVATE_KEY in .env
    - USDC balance on Base mainnet

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
    """
    Execute async function with exponential backoff retry.

    Args:
        func: Async function to execute.
        max_attempts: Maximum retry attempts.
        base_delay: Initial delay between retries (seconds).
        max_delay: Maximum delay between retries (seconds).

    Returns:
        Result of the function.

    Raises:
        Last exception if all retries fail.
    """
    last_error: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            return await func()

        except (httpx.ConnectError, httpx.TimeoutException) as e:
            # Retry on network errors
            last_error = e
            if attempt == max_attempts:
                break

            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            print(f"  Attempt {attempt} failed: {type(e).__name__}")
            print(f"  Retrying in {delay:.1f}s...")
            await asyncio.sleep(delay)

        except httpx.HTTPStatusError as e:
            # Only retry on server errors (5xx)
            if e.response.status_code >= 500:
                last_error = e
                if attempt == max_attempts:
                    break

                delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                print(f"  Attempt {attempt} failed: HTTP {e.response.status_code}")
                print(f"  Retrying in {delay:.1f}s...")
                await asyncio.sleep(delay)
            else:
                # Don't retry client errors (4xx)
                raise

    raise last_error  # type: ignore


async def query_with_retry(
    client: NeurobroClient,
    prompt: str,
    max_attempts: int = 3,
) -> QueryResult:
    """Send query with automatic retry on transient failures."""
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

    prompt = "What is DeFi in one sentence?"
    print(f"\nQuery: {prompt}")
    print("-" * 50)

    try:
        result = await query_with_retry(client, prompt, max_attempts=3)
        print(f"\nModel: {result.model}")
        print(f"Request ID: {result.request_id}")
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
