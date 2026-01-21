# Neurobro x402 Cookbook

Python examples for the **Neurobro API** with **x402** micropayments.

![Neurobro Logo][neurobro-img]

[neurobro-img]: ./assets/neurobro.png

## Overview

This repository provides working Python examples for calling the Neurobro x402 API. The API offers AI-powered crypto analysis with automatic USDC payments via the x402 protocol.

**Production API:** https://x402.neurobro.ai

## What is x402?

[x402](https://x402.org) is an open payment protocol for APIs:

- No accounts or API keys
- Pay-per-request with USDC
- Automatic payment handling

Flow: `Request → 402 Payment Required → Pay → Response`

## Quick Start

```bash
cd examples
pip install -r requirements.txt

# Configure wallet
cp .env.example .env
# Edit .env: WALLET_PRIVATE_KEY=0x...
```

### Run Examples

```bash
# Health check (free)
python 01_health_check.py

# Query (paid)
python 02_simple_query.py

# CLI query
python 03_cli_query.py "What is Bitcoin?"
```

### Use as Library

```python
from neurobro_client import NeurobroClient

client = NeurobroClient()

# Free
status = client.health()
print(status.is_healthy)

# Paid
result = client.query("Analyze ETH price action")
print(result.text)
```

## API Endpoints

| Endpoint | Method | Cost |
|----------|--------|------|
| `/api/v1/health` | GET | Free |
| `/api/v1/query` | POST | USDC |

## Files

```
examples/
├── neurobro_client.py   # Client library
├── 01_health_check.py   # Health check (free)
├── 02_simple_query.py   # Basic query example
├── 03_cli_query.py      # CLI one-liner
├── 04_async_usage.py    # Async workflow
├── requirements.txt
└── .env.example
```

## Links

- [x402 Protocol](https://x402.org)
- [x402 Python Package](https://pypi.org/project/x402/)
- [Coinbase x402 Docs](https://docs.cdp.coinbase.com/x402/quickstart-for-buyers)

## License

MIT
