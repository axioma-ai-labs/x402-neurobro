# Neurobro x402 Cookbook

Python examples for the **Neurobro API** with **x402** micropayments.

![Neurobro Logo][neurobro-img]

[neurobro-img]: ./assets/neurobro.png

## Overview

Working Python examples for calling the Neurobro x402 API. AI-powered crypto analysis with automatic USDC payments via the x402 protocol.

**Production API:** https://x402.neurobro.ai

## What is x402?

[x402](https://x402.org) is an open payment protocol:

- No accounts or API keys
- Pay-per-request with USDC
- Automatic payment handling

Flow: `Request → 402 Payment Required → Pay → Response`

## Quick Start

```bash
cd examples
pip install -r requirements.txt

cp .env.example .env
# Edit .env: WALLET_PRIVATE_KEY=0x...
```

```bash
# Health check (free)
python 01_health_check.py

# Query (paid)
python 03_cli_query.py "What is Bitcoin?"
```

## Use as Library

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

## Examples

| File | Description |
|------|-------------|
| `01_health_check.py` | Check API status (free) |
| `02_simple_query.py` | Basic paid query |
| `03_cli_query.py` | CLI one-liner |
| `04_async_usage.py` | Async workflow |
| `05_error_handling.py` | Error handling patterns |
| `06_batch_queries.py` | Multiple queries |
| `07_custom_config.py` | Custom configuration |
| `08_retry_logic.py` | Retry with backoff |

See [`examples/README.md`](./examples/README.md) for details.

## API

| Endpoint | Method | Cost |
|----------|--------|------|
| `/api/v1/health` | GET | Free |
| `/api/v1/query` | POST | USDC |

## Links

- [x402 Protocol](https://x402.org)
- [x402 Python Package](https://pypi.org/project/x402/)
- [Coinbase x402 Docs](https://docs.cdp.coinbase.com/x402/quickstart-for-buyers)

## License

MIT
