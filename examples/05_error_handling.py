#!/usr/bin/env python3
"""
Error Handling — handle every failure mode gracefully.

Covers:
    - Unreachable API / timeouts
    - Missing or malformed private key
    - Payment and HTTP errors (402, 429, 5xx)

Safe to run without USDC — most scenarios use the free health endpoint
or surface errors before spending. The final scenario sends a paid query.

Usage:
    python 05_error_handling.py
"""

import sys

import httpx

from neurobro_client import NeurobroClient, check_health


def main() -> None:
    print("Error Handling Examples")
    print("=" * 50)

    # 1. Health check with error handling
    print("\n[1] Health check with error handling")
    print("-" * 30)

    try:
        status = check_health()
        print(f"API is {status.status}")
    except httpx.ConnectError:
        print("Error: Cannot connect to API")
        print("Check your internet connection")
    except httpx.TimeoutException:
        print("Error: Request timed out")
    except httpx.HTTPStatusError as e:
        print(f"Error: HTTP {e.response.status_code}")
    # Sample: API is healthy

    # 2. Client initialization errors
    print("\n[2] Missing private key")
    print("-" * 30)

    try:
        # Forces a ValueError when WALLET_PRIVATE_KEY is not set.
        client = NeurobroClient(private_key=None)
        print(f"Client initialized: {client.wallet_address}")
    except ValueError as e:
        print(f"Expected error: {e}")
    # Sample: Expected error: Private key required. Pass private_key argument
    #         or set WALLET_PRIVATE_KEY env var.

    # 3. Invalid private key
    print("\n[3] Invalid private key format")
    print("-" * 30)

    try:
        client = NeurobroClient(private_key="not-a-valid-key")
    except Exception as e:
        print(f"Expected error: {type(e).__name__}")
    # Sample: Expected error: ValueError

    # 4. Query with full error handling
    print("\n[4] Query with full error handling")
    print("-" * 30)

    try:
        client = NeurobroClient()
        print(f"Wallet: {client.wallet_address}")

        result = client.query("What is Bitcoin?")
        print(f"Success: {result.text[:100]}...")

    except ValueError as e:
        print(f"Config error: {e}")
        sys.exit(1)

    except httpx.ConnectError:
        print("Network error: Cannot reach API")
        sys.exit(1)

    except httpx.TimeoutException:
        print("Timeout: Request took too long")
        sys.exit(1)

    except httpx.HTTPStatusError as e:
        status = e.response.status_code

        if status == 402:
            print("Payment required - check wallet USDC balance")
        elif status == 429:
            print("Rate limited - try again later")
        elif status >= 500:
            print("Server error - try again later")
        else:
            print(f"HTTP error: {status}")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        sys.exit(1)
    # Sample (success path):
    #   Wallet: 0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B
    #   Success: Bitcoin (BTC) is a decentralized digital currency launched...

    print("\n" + "=" * 50)
    print("Error handling complete")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Sample output (illustrative — real responses will vary)
# ---------------------------------------------------------------------------
# Error Handling Examples
# ==================================================
#
# [1] Health check with error handling
# ------------------------------
# API is healthy
#
# [2] Missing private key
# ------------------------------
# Expected error: Private key required. Pass private_key argument or set
# WALLET_PRIVATE_KEY env var.
#
# [3] Invalid private key format
# ------------------------------
# Expected error: ValueError
#
# [4] Query with full error handling
# ------------------------------
# Wallet: 0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B
# Success: Bitcoin (BTC) is a decentralized digital currency launched in...
#
# ==================================================
# Error handling complete
