"""
Neurobro x402 API Client.

A minimal Python client for the Neurobro x402 API with automatic USDC payments.

Installation:
    pip install x402 httpx eth-account python-dotenv

Example:
    from neurobro_client import NeurobroClient

    client = NeurobroClient(private_key="0x...")
    response = client.query("What is Bitcoin?")
    print(response.text)
"""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass

import httpx
from dotenv import load_dotenv
from eth_account import Account
from eth_account.signers.local import LocalAccount
from x402.clients import x402_payment_hooks

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

API_BASE_URL = "https://x402.neurobro.ai"
API_HEALTH_PATH = "/api/v1/health"
API_QUERY_PATH = "/api/v1/query"
DEFAULT_TIMEOUT = 60.0

# ---------------------------------------------------------------------------
# Response Models
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class HealthStatus:
    """API health check response."""

    status: str
    version: str
    service: str

    @property
    def is_healthy(self) -> bool:
        return self.status == "healthy"


@dataclass(frozen=True, slots=True)
class QueryResult:
    """AI query response."""

    text: str
    model: str
    request_id: str


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


class NeurobroClient:
    """
    Client for the Neurobro x402 API.

    Handles automatic USDC payments via the x402 protocol on Base mainnet.

    Args:
        private_key: Ethereum private key for signing payments.
            Falls back to WALLET_PRIVATE_KEY environment variable.
        base_url: API base URL. Defaults to production.
        timeout: Request timeout in seconds.

    Raises:
        ValueError: If no private key is provided.

    Example:
        client = NeurobroClient()
        result = client.query("Analyze BTC market sentiment")
        print(result.text)
    """

    def __init__(
        self,
        private_key: str | None = None,
        base_url: str = API_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        key = private_key or os.getenv("WALLET_PRIVATE_KEY")
        if not key:
            raise ValueError(
                "Private key required. "
                "Pass private_key argument or set WALLET_PRIVATE_KEY env var."
            )

        self._account: LocalAccount = Account.from_key(key)
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    @property
    def wallet_address(self) -> str:
        """Return the wallet address derived from the private key."""
        return self._account.address

    # -----------------------------------------------------------------------
    # Async API
    # -----------------------------------------------------------------------

    async def health_async(self) -> HealthStatus:
        """
        Check API health (async). Free endpoint - no payment required.

        Returns:
            HealthStatus with service status information.
        """
        async with httpx.AsyncClient(
            base_url=self._base_url, timeout=self._timeout
        ) as client:
            resp = await client.get(API_HEALTH_PATH)
            resp.raise_for_status()
            data = resp.json()

        return HealthStatus(
            status=data["status"],
            version=data["version"],
            service=data["service"],
        )

    async def query_async(
        self,
        prompt: str,
        client_id: str | None = None,
    ) -> QueryResult:
        """
        Send a crypto analysis query (async). Requires USDC payment.

        Args:
            prompt: Your question or analysis request.
            client_id: Optional identifier for request tracking.

        Returns:
            QueryResult with AI-generated response.

        Raises:
            httpx.HTTPStatusError: On request failure.
        """
        payload = {"prompt": prompt}
        if client_id:
            payload["client_id"] = client_id

        async with httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._timeout,
            event_hooks=x402_payment_hooks(self._account),
        ) as client:
            resp = await client.post(API_QUERY_PATH, json=payload)
            resp.raise_for_status()
            data = resp.json()

        return QueryResult(
            text=data["response"],
            model=data["model"],
            request_id=data["request_id"],
        )

    # -----------------------------------------------------------------------
    # Sync API (convenience wrappers)
    # -----------------------------------------------------------------------

    def health(self) -> HealthStatus:
        """Check API health (sync). Free endpoint - no payment required."""
        return asyncio.run(self.health_async())

    def query(self, prompt: str, client_id: str | None = None) -> QueryResult:
        """Send a crypto analysis query (sync). Requires USDC payment."""
        return asyncio.run(self.query_async(prompt, client_id))


# ---------------------------------------------------------------------------
# Standalone Functions
# ---------------------------------------------------------------------------


def check_health(base_url: str = API_BASE_URL) -> HealthStatus:
    """
    Quick health check without wallet setup.

    Args:
        base_url: API base URL.

    Returns:
        HealthStatus with service information.
    """
    resp = httpx.get(f"{base_url}{API_HEALTH_PATH}", timeout=DEFAULT_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    return HealthStatus(
        status=data["status"],
        version=data["version"],
        service=data["service"],
    )


async def quick_query(prompt: str, private_key: str | None = None) -> str:
    """
    Send a single query with minimal setup.

    Args:
        prompt: Your question.
        private_key: Wallet private key (or set WALLET_PRIVATE_KEY env var).

    Returns:
        AI response text.
    """
    client = NeurobroClient(private_key=private_key)
    result = await client.query_async(prompt)
    return result.text
