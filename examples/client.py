"""
Neurobro x402 API Client

A clean, minimalistic Python client for interacting with the Neurobro x402 API.
Handles automatic payment via the x402 protocol using httpx.

Requirements:
    pip install x402 httpx eth-account python-dotenv

Usage:
    from client import NeuроbroClient

    client = NeurobroClient(private_key="0x...")
    response = client.query("What is the current sentiment on Bitcoin?")
    print(response)
"""

import os
from dataclasses import dataclass
from typing import Any

import httpx
from dotenv import load_dotenv
from eth_account import Account
from x402.clients import x402_payment_hooks

# Load environment variables
load_dotenv()

# API Configuration
BASE_URL = "https://x402.neurobro.ai"
QUERY_ENDPOINT = "/api/v1/query"
HEALTH_ENDPOINT = "/api/v1/health"


@dataclass
class QueryResponse:
    """Response from a query to the Neurobro API."""

    response: str
    model: str
    request_id: str


@dataclass
class HealthResponse:
    """Health check response from the API."""

    status: str
    version: str
    service: str


class NeurobroClient:
    """
    Client for the Neurobro x402 API.

    This client handles automatic USDC payments via the x402 protocol.
    Each query costs a small amount of USDC on Base mainnet.

    Example:
        client = NeurobroClient(private_key="0x...")
        result = client.query("Analyze the current crypto market trends")
        print(result.response)
    """

    def __init__(
        self,
        private_key: str | None = None,
        base_url: str = BASE_URL,
        timeout: float = 60.0,
    ):
        """
        Initialize the Neurobro client.

        Args:
            private_key: Ethereum private key for signing payments.
                        If not provided, will read from WALLET_PRIVATE_KEY env var.
            base_url: Base URL of the Neurobro API.
            timeout: Request timeout in seconds.

        Raises:
            ValueError: If no private key is provided or found in environment.
        """
        self.private_key = private_key or os.getenv("WALLET_PRIVATE_KEY")
        if not self.private_key:
            raise ValueError(
                "Private key required. Pass it directly or set WALLET_PRIVATE_KEY env var."
            )

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._account = Account.from_key(self.private_key)

    def _create_client(self) -> httpx.AsyncClient:
        """Create an httpx client with x402 payment hooks."""
        client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        client.event_hooks = x402_payment_hooks(self._account)
        return client

    async def query_async(
        self,
        prompt: str,
        client_id: str | None = None,
    ) -> QueryResponse:
        """
        Send a query to the Neurobro API (async).

        This endpoint is protected by x402 - payment is handled automatically.

        Args:
            prompt: Your crypto analysis question or request.
            client_id: Optional identifier for tracking your requests.

        Returns:
            QueryResponse containing the AI-generated analysis.

        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        payload: dict[str, Any] = {"prompt": prompt}
        if client_id:
            payload["client_id"] = client_id

        async with self._create_client() as client:
            response = await client.post(QUERY_ENDPOINT, json=payload)
            response.raise_for_status()
            data = response.json()

        return QueryResponse(
            response=data["response"],
            model=data["model"],
            request_id=data["request_id"],
        )

    async def health_async(self) -> HealthResponse:
        """
        Check the API health status (async).

        This endpoint is free - no payment required.

        Returns:
            HealthResponse with the current service status.
        """
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            response = await client.get(HEALTH_ENDPOINT)
            response.raise_for_status()
            data = response.json()

        return HealthResponse(
            status=data["status"],
            version=data["version"],
            service=data["service"],
        )

    def query(self, prompt: str, client_id: str | None = None) -> QueryResponse:
        """
        Send a query to the Neurobro API (sync wrapper).

        Args:
            prompt: Your crypto analysis question or request.
            client_id: Optional identifier for tracking your requests.

        Returns:
            QueryResponse containing the AI-generated analysis.
        """
        import asyncio

        return asyncio.run(self.query_async(prompt, client_id))

    def health(self) -> HealthResponse:
        """
        Check the API health status (sync wrapper).

        Returns:
            HealthResponse with the current service status.
        """
        import asyncio

        return asyncio.run(self.health_async())


# Convenience function for quick queries
async def query(prompt: str, private_key: str | None = None) -> str:
    """
    Quick helper to send a single query.

    Args:
        prompt: Your crypto analysis question.
        private_key: Ethereum private key (or set WALLET_PRIVATE_KEY env var).

    Returns:
        The AI-generated response text.

    Example:
        response = await query("What's the outlook for ETH this week?")
        print(response)
    """
    client = NeurobroClient(private_key=private_key)
    result = await client.query_async(prompt)
    return result.response
