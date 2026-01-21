#!/usr/bin/env python3
"""
Error Handling - Gracefully handle API errors.

Demonstrates:
    - Connection errors
    - Payment failures
    - Invalid responses
    - Timeout handling

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

    # 2. Client initialization errors
    print("\n[2] Missing private key")
    print("-" * 30)

    try:
        # This will fail if WALLET_PRIVATE_KEY is not set
        client = NeurobroClient(private_key=None)
        print(f"Client initialized: {client.wallet_address}")
    except ValueError as e:
        print(f"Expected error: {e}")

    # 3. Invalid private key
    print("\n[3] Invalid private key format")
    print("-" * 30)

    try:
        client = NeurobroClient(private_key="not-a-valid-key")
    except Exception as e:
        print(f"Expected error: {type(e).__name__}")

    # 4. Query with proper error handling
    print("\n[4] Query with full error handling")
    print("-" * 30)

    try:
        client = NeurobroClient()
        print(f"Wallet: {client.wallet_address}")

        result = client.query("What is Bitcoin?")
        print(f"Success: {result.text[:100]}...")

    except ValueError as e:
        # Missing or invalid private key
        print(f"Config error: {e}")
        sys.exit(1)

    except httpx.ConnectError:
        # Network issues
        print("Network error: Cannot reach API")
        sys.exit(1)

    except httpx.TimeoutException:
        # Request took too long
        print("Timeout: Request took too long")
        sys.exit(1)

    except httpx.HTTPStatusError as e:
        # HTTP errors (402, 500, etc.)
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
        # Catch-all for unexpected errors
        print(f"Unexpected error: {type(e).__name__}: {e}")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("Error handling complete")


if __name__ == "__main__":
    main()
