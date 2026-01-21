# Neurobro x402 Examples

Python examples for the Neurobro x402 API.

## Setup

```bash
pip install -r requirements.txt

cp .env.example .env
# Edit .env: WALLET_PRIVATE_KEY=0x...
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
| `05_error_handling.py` | Handle errors gracefully | Free/USDC |
| `06_batch_queries.py` | Send multiple queries | USDC |
| `07_custom_config.py` | Custom URL and timeout | Free |
| `08_retry_logic.py` | Retry on transient failures | USDC |

### Quick Start

```bash
# Health check (free)
python 01_health_check.py

# Simple query (paid)
python 02_simple_query.py

# CLI query (paid)
python 03_cli_query.py "What is Ethereum?"
```

## Client Library

### Basic Usage

```python
from neurobro_client import NeurobroClient

client = NeurobroClient()  # reads WALLET_PRIVATE_KEY from .env

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
```

### Standalone Health Check

```python
from neurobro_client import check_health

status = check_health()  # no wallet needed
print(status.is_healthy)
```

## API Reference

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

## Response Models

### HealthStatus

```python
@dataclass
class HealthStatus:
    status: str      # "healthy"
    version: str     # "1.0.0"
    service: str     # "neurobro-x402"

    @property
    def is_healthy(self) -> bool: ...
```

### QueryResult

```python
@dataclass
class QueryResult:
    text: str        # AI response
    model: str       # "grok-4"
    request_id: str  # unique ID
```

## Troubleshooting

**"Private key required"**
→ Set `WALLET_PRIVATE_KEY` in `.env`

**Payment fails**
→ Ensure wallet has USDC on Base mainnet

**Connection error**
→ Run `01_health_check.py` to verify API
