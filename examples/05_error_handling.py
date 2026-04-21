#!/usr/bin/env python3
"""
Error handling — every failure mode, handled gracefully.

Covers unreachable API, timeouts, missing or malformed private keys,
and the common HTTP errors (402, 429, 5xx).

The final scenario sends a paid query; everything before it is free.

Usage:
    python 05_error_handling.py
"""

import sys

import httpx

from neurobro_client import NeurobroClient, check_health


def main() -> None:
    print("Error Handling Examples")
    print("=" * 50)

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

    print("\n[2] Missing private key")
    print("-" * 30)

    try:
        client = NeurobroClient(private_key=None)
        print(f"Client initialized: {client.wallet_address}")
    except ValueError as e:
        print(f"Expected error: {e}")

    print("\n[3] Invalid private key format")
    print("-" * 30)

    try:
        client = NeurobroClient(private_key="not-a-valid-key")
    except Exception as e:
        print(f"Expected error: {type(e).__name__}")

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

    print("\n" + "=" * 50)
    print("Error handling complete")


if __name__ == "__main__":
    main()


# Example output:
#
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
# Wallet: 0xA1b2C3d4E5F67890a1b2c3D4e5f6789012345678
# Success: Bitcoin (BTC) is a decentralized digital currency launched in...
#
# ==================================================
# Error handling complete
