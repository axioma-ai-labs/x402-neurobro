#!/usr/bin/env python3
"""
Health Check Example

Check if the Neurobro x402 API is online and operational.
This endpoint is FREE - no wallet or payment required.

Run:
    pip install httpx
    python health_check.py
"""

import httpx

BASE_URL = "https://x402.neurobro.ai"
HEALTH_ENDPOINT = "/api/v1/health"


def check_health() -> None:
    """Check the API health status."""
    print("Checking Neurobro x402 API health...")
    print(f"URL: {BASE_URL}{HEALTH_ENDPOINT}")
    print("-" * 40)

    try:
        response = httpx.get(f"{BASE_URL}{HEALTH_ENDPOINT}", timeout=10.0)
        response.raise_for_status()

        data = response.json()
        print(f"Status:  {data['status']}")
        print(f"Version: {data['version']}")
        print(f"Service: {data['service']}")
        print("-" * 40)
        print("API is online and operational.")

    except httpx.ConnectError:
        print("Error: Could not connect to the API")
    except httpx.HTTPStatusError as e:
        print(f"Error: HTTP {e.response.status_code}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    check_health()
