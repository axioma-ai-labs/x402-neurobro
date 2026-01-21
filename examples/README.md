# Neurobro x402 Examples

Python examples for the Neurobro x402 API.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure wallet
cp .env.example .env
# Edit .env and add your private key
```

**Requirements:**
- Python 3.10+
- USDC on Base mainnet (for paid queries)

## Examples

| File | Description | Payment |
|------|-------------|---------|
| `01_health_check.py` | Check if API is online | Free |
| `02_simple_query.py` | Send a basic query | USDC |
| `03_cli_query.py` | CLI one-liner queries | USDC |
| `04_async_usage.py` | Full async workflow | USDC |

### Run Examples

```bash
# Health check (free, no wallet needed)
python 01_health_check.py

# Simple query
python 02_simple_query.py

# CLI query
python 03_cli_query.py "What is Ethereum?"

# Async example
python 04_async_usage.py
```

## Using the Client

```python
from neurobro_client import NeurobroClient

# Initialize (reads WALLET_PRIVATE_KEY from .env)
client = NeurobroClient()

# Health check (free)
status = client.health()
print(status.is_healthy)

# Query (paid)
result = client.query("Analyze BTC sentiment")
print(result.text)
```

### Async Usage

```python
import asyncio
from neurobro_client import NeurobroClient

async def main():
    client = NeurobroClient()
    result = await client.query_async("What are top DeFi protocols?")
    print(result.text)

asyncio.run(main())
```

### Quick One-Liner

```python
import asyncio
from neurobro_client import quick_query

response = asyncio.run(quick_query("What is Bitcoin?"))
print(response)
```

## API Reference

### Endpoints

| Endpoint | Method | Cost |
|----------|--------|------|
| `/api/v1/health` | GET | Free |
| `/api/v1/query` | POST | USDC |

### Request

```json
{
  "prompt": "Your question",
  "client_id": "optional-id"
}
```

### Response

```json
{
  "response": "AI answer...",
  "model": "grok-4",
  "request_id": "uuid"
}
```

## Troubleshooting

**"Private key required"**
- Set `WALLET_PRIVATE_KEY` in `.env`

**Payment fails**
- Ensure wallet has USDC on Base mainnet (not testnet)

**Connection error**
- Run `01_health_check.py` to verify API is online
