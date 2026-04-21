#!/usr/bin/env python3
"""
Batch Queries — run multiple queries sequentially or concurrently.

Each prompt costs $1 USDC. Three prompts = $3 USDC total.
Switch to `concurrent=True` to fire all queries in parallel.

Prereqs:
    WALLET_PRIVATE_KEY in .env, wallet funded with enough USDC
    to cover every prompt in the batch.

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
        concurrent: If True, fire all queries in parallel.

    Returns:
        List of BatchResult with results or errors.
    """
    results: list[BatchResult] = []

    if concurrent:
        tasks = [client.query_async(p) for p in prompts]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for prompt, response in zip(prompts, responses):
            if isinstance(response, Exception):
                results.append(BatchResult(prompt, None, str(response)))
            else:
                results.append(BatchResult(prompt, response, None))
    else:
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

    prompts = [
        "What is Bitcoin in one sentence?",
        "What is Ethereum in one sentence?",
        "What is Solana in one sentence?",
    ]

    # Sequential: one query after another. Safer, cheaper to reason about.
    # To run all three in parallel instead, swap to: concurrent=True.
    print("\n[Sequential Queries]")
    print("-" * 40)

    results = await run_batch(client, prompts, concurrent=False)

    for i, batch in enumerate(results, 1):
        print(f"\n{i}. {batch.prompt}")
        if batch.result:
            text = batch.result.text[:150].replace("\n", " ")
            print(f"   → {text}...")
        else:
            print(f"   → Error: {batch.error}")

    print("\n" + "=" * 60)
    success = sum(1 for r in results if r.result)
    print(f"Completed: {success}/{len(prompts)} queries")


if __name__ == "__main__":
    asyncio.run(main())


# ---------------------------------------------------------------------------
# Sample output (illustrative — real responses will vary)
# ---------------------------------------------------------------------------
# Wallet: 0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B
# ============================================================
#
# [Sequential Queries]
# ----------------------------------------
#
# 1. What is Bitcoin in one sentence?
#    → Bitcoin is a decentralized digital currency with a fixed supply of
#      21 million coins, secured by proof-of-work mining on a public...
#
# 2. What is Ethereum in one sentence?
#    → Ethereum is a programmable blockchain introduced in 2015 whose native
#      asset ETH powers a global network of smart contracts...
#
# 3. What is Solana in one sentence?
#    → Solana is a high-throughput proof-of-stake blockchain designed for
#      low-latency applications, using a Proof-of-History clock to...
#
# ============================================================
# Completed: 3/3 queries
