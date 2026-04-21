#!/usr/bin/env python3
"""
Custom Configuration — point the client at a different URL or timeout.

Useful for staging deployments, self-hosted instances, or slow networks.
No payment is made; only the free health endpoint is hit.

Usage:
    python 07_custom_config.py
"""

import os
import sys

from neurobro_client import (
    API_BASE_URL,
    DEFAULT_TIMEOUT,
    NeurobroClient,
    check_health,
)


def main() -> None:
    print("Custom Configuration Examples")
    print("=" * 50)

    # Defaults
    print("\n[1] Default configuration")
    print("-" * 30)
    print(f"Base URL: {API_BASE_URL}")
    print(f"Timeout:  {DEFAULT_TIMEOUT}s")

    # Custom timeout for slow connections
    print("\n[2] Custom timeout")
    print("-" * 30)

    try:
        client = NeurobroClient(timeout=120.0)  # 2 minutes
        print(f"Wallet: {client.wallet_address}")
        print("Timeout: 120s (for slow connections)")
    except ValueError as e:
        print(f"Setup error: {e}")

    # Environment-based configuration
    print("\n[3] Environment-based config")
    print("-" * 30)

    env = os.getenv("NEUROBRO_ENV", "production")
    base_url = os.getenv("NEUROBRO_API_URL", API_BASE_URL)
    timeout = float(os.getenv("NEUROBRO_TIMEOUT", str(DEFAULT_TIMEOUT)))

    print(f"Environment: {env}")
    print(f"API URL:     {base_url}")
    print(f"Timeout:     {timeout}s")

    # Probe the configured URL (free endpoint)
    print("\n[4] Test configured endpoint")
    print("-" * 30)

    try:
        status = check_health(base_url=base_url)
        print(f"Status:  {status.status}")
        print(f"Version: {status.version}")
        print(f"Service: {status.service}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("Configuration complete")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Sample output
# ---------------------------------------------------------------------------
# Custom Configuration Examples
# ==================================================
#
# [1] Default configuration
# ------------------------------
# Base URL: https://x402.neurobro.ai
# Timeout:  60.0s
#
# [2] Custom timeout
# ------------------------------
# Wallet: 0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B
# Timeout: 120s (for slow connections)
#
# [3] Environment-based config
# ------------------------------
# Environment: production
# API URL:     https://x402.neurobro.ai
# Timeout:     60.0s
#
# [4] Test configured endpoint
# ------------------------------
# Status:  healthy
# Version: 1.0.0
# Service: neurobro-x402
#
# ==================================================
# Configuration complete
