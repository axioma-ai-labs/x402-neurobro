#!/usr/bin/env python3
"""
Custom Configuration - Configure client for different environments.

Demonstrates:
    - Custom base URL
    - Custom timeout
    - Environment-based configuration

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

    # Show defaults
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

    # Read from environment with fallbacks
    env = os.getenv("NEUROBRO_ENV", "production")
    base_url = os.getenv("NEUROBRO_API_URL", API_BASE_URL)
    timeout = float(os.getenv("NEUROBRO_TIMEOUT", str(DEFAULT_TIMEOUT)))

    print(f"Environment: {env}")
    print(f"API URL:     {base_url}")
    print(f"Timeout:     {timeout}s")

    # Test connection to configured URL
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
