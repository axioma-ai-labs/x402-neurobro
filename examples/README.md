# Neurobro x402 API Examples

Python examples for interacting with the Neurobro x402 API.

## Prerequisites

1. **Python 3.10+**
2. **USDC on Base mainnet** in your wallet
3. **Private key** for signing payments

## Installation

```bash
pip install x402 httpx eth-account python-dotenv
```

## Configuration

Create a `.env` file in this directory:

```env
WALLET_PRIVATE_KEY=0x_your_private_key_here
```

**Security:** Never commit your `.env` file or share your private key.

## Examples

### Health Check (Free)

Check if the API is online. No wallet required.

```bash
python health_check.py
```

### Basic Usage

Full example showing health check and paid query:

```bash
python basic_usage.py
```

### Quick Query

One-liner for quick questions:

```bash
python quick_query.py "What is the current sentiment on Ethereum?"
```

### Using the Client Library

```python
from client import NeurobroClient

# Initialize with private key
client = NeurobroClient(private_key="0x...")

# Or use environment variable
client = NeurobroClient()  # reads WALLET_PRIVATE_KEY

# Check health (free)
health = client.health()
print(health.status)

# Send a query (paid with USDC)
result = client.query("Analyze Bitcoin's price action this week")
print(result.response)
```

### Async Usage

```python
import asyncio
from client import NeurobroClient

async def main():
    client = NeurobroClient()

    # Async methods
    health = await client.health_async()
    result = await client.query_async("What are the top DeFi protocols?")
    print(result.response)

asyncio.run(main())
```

## API Reference

### Endpoints

| Endpoint | Method | Description | Cost |
|----------|--------|-------------|------|
| `/api/v1/health` | GET | Health check | Free |
| `/api/v1/query` | POST | AI query | USDC per query |

### Query Request

```json
{
  "prompt": "Your crypto analysis question",
  "client_id": "optional-tracking-id"
}
```

### Query Response

```json
{
  "response": "AI-generated analysis...",
  "model": "grok-4",
  "request_id": "uuid"
}
```

## How x402 Payments Work

1. Your request hits the `/api/v1/query` endpoint
2. Server returns `402 Payment Required` with payment details
3. The x402 library automatically:
   - Reads payment requirements from headers
   - Signs a USDC payment authorization
   - Retries the request with payment proof
4. Server verifies payment and returns the AI response

All payments are in USDC on Base mainnet. The x402 library handles everything automatically.

## Troubleshooting

### "Private key required"

Set `WALLET_PRIVATE_KEY` in your `.env` file or pass it directly to `NeurobroClient()`.

### "Insufficient USDC balance"

Ensure your wallet has USDC on **Base mainnet** (not testnet, not other chains).

### Connection errors

Check if the API is online using `health_check.py` first.

## Links

- [x402 Protocol Documentation](https://x402.org)
- [Coinbase x402 Guide](https://docs.cdp.coinbase.com/x402/quickstart-for-buyers)
- [x402 Python Package](https://pypi.org/project/x402/)
