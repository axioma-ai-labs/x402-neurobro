#!/usr/bin/env python3
"""
Batch Queries - Send multiple queries efficiently.

Demonstrates:
    - Sequential queries
    - Concurrent queries with asyncio
    - Result aggregation

Requires:
    - WALLET_PRIVATE_KEY in .env
    - Sufficient USDC for all queries

Usage:
    python 06_batch_queries.py
"""

import asyncio
import sys
from dataclasses import dataclass

from neurobro_client import NeurobroClient, QueryResult


@dataclass
class BatchResult:
    """Result of a batch query."""

    prompt: str
    result: QueryResult | None
    error: str | None


async def run_batch(
    client: NeurobroClient,
    prompts: list[str],
    concurrent: bool = False,
) -> list[BatchResult]:
    """
    Run multiple queries.

    Args:
        client: Initialized NeurobroClient.
        prompts: List of prompts to query.
        concurrent: If True, run all queries concurrently.

    Returns:
        List of BatchResult with results or errors.
    """
    results: list[BatchResult] = []

    if concurrent:
        # Run all queries at once
        tasks = [client.query_async(p) for p in prompts]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for prompt, response in zip(prompts, responses):
            if isinstance(response, Exception):
                results.append(BatchResult(prompt, None, str(response)))
            else:
                results.append(BatchResult(prompt, response, None))
    else:
        # Run queries one at a time
        for prompt in prompts:
            try:
                result = await client.query_async(prompt)
                results.append(BatchResult(prompt, result, None))
            except Exception as e:
                results.append(BatchResult(prompt, None, str(e)))

    return results


async def main() -> None:
    try:
        client = NeurobroClient()
    except ValueError as e:
        print(f"Setup error: {e}")
        sys.exit(1)

    print(f"Wallet: {client.wallet_address}")
    print("=" * 60)

    # Define queries
    prompts = [
        "What is Bitcoin in one sentence?",
        "What is Ethereum in one sentence?",
        "What is Solana in one sentence?",
    ]

    # Sequential execution
    print("\n[Sequential Queries]")
    print("-" * 40)

    results = await run_batch(client, prompts, concurrent=False)

    for i, batch in enumerate(results, 1):
        print(f"\n{i}. {batch.prompt}")
        if batch.result:
            # Show first 150 chars of response
            text = batch.result.text[:150].replace("\n", " ")
            print(f"   → {text}...")
        else:
            print(f"   → Error: {batch.error}")

    # Summary
    print("\n" + "=" * 60)
    success = sum(1 for r in results if r.result)
    print(f"Completed: {success}/{len(prompts)} queries")


if __name__ == "__main__":
    asyncio.run(main())
