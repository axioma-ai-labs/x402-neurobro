#!/usr/bin/env python3
"""
Health check — verify the API is online.

Free. No wallet, no USDC.

Usage:
    python 01_health_check.py
"""

from neurobro_client import check_health


def main() -> None:
    print("Checking Neurobro x402 API...")
    print("-" * 40)

    try:
        status = check_health()
        print(f"Status:  {status.status}")
        print(f"Version: {status.version}")
        print(f"Service: {status.service}")
        print("-" * 40)

        if status.is_healthy:
            print("API is online.")
        else:
            print("API returned unhealthy status.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()


# Example output:
#
# Checking Neurobro x402 API...
# ----------------------------------------
# Status:  healthy
# Version: 1.0.0
# Service: neurobro-x402
# ----------------------------------------
# API is online.
