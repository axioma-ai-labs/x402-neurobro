# Neurobro x402 — Examples

Runnable Python examples for the Neurobro x402 API. Start here to go from
an empty folder to a working paid query in a few minutes.

> For the full overview, pricing, and protocol walkthrough, see the
> [top-level README](../README.md).

---

## Setup

```bash
pip install -r requirements.txt

cp .env.example .env
# Edit .env → WALLET_PRIVATE_KEY=0x...
```

**Requirements**

- Python 3.10+
- An EVM wallet with **USDC on Base mainnet** for any paid example
- No account, no API key

New to funding a wallet on Base? See
[Get started](../README.md#get-started-in-5-minutes) in the top README.

---

## Examples at a glance

| # | File | What it teaches | Paid? | Est. cost |
|---|------|-----------------|-------|-----------|
| 01 | `01_health_check.py` | Verify the API is reachable | Free | $0 |
| 02 | `02_simple_query.py` | Smallest working paid integration | Paid | $1 USDC |
| 03 | `03_cli_query.py` | Ask anything from the terminal | Paid | $1 USDC |
| 04 | `04_async_usage.py` | Full async workflow for agents / FastAPI | Paid | $1 USDC |
| 05 | `05_error_handling.py` | Every failure mode, with clear error text | Mixed | ~$1 USDC |
| 06 | `06_batch_queries.py` | Sequential + concurrent batches | Paid | $3 USDC |
| 07 | `07_custom_config.py` | Custom URL, timeout, env vars | Free | $0 |
| 08 | `08_retry_logic.py` | Exponential backoff on transient failures | Paid | $1 USDC |

Each file ends with an **example output** block so you see what to expect
before running it.

### Quick run

```bash
# Free
python 01_health_check.py

# Paid — make sure your wallet is funded on Base mainnet
python 03_cli_query.py "What is Ethereum?"
```

---

## Funding checklist

| You want to run | Keep in wallet (USDC on Base) |
|-----------------|-------------------------------|
| 01, 07 | $0 (free) |
| 02, 03, 04, 08 | at least $1 |
| 05 | at least $1 (final scenario is paid) |
| 06 | at least $3 (one $1 payment per prompt) |
| All eight | $6–$7 to be safe |

You don't need ETH on Base — x402 payments are handled by the facilitator.

---

## Use the client as a library

### Sync

```python
from neurobro_client import NeurobroClient

client = NeurobroClient()          # reads WALLET_PRIVATE_KEY from .env

status = client.health()           # free
print(status.is_healthy)

result = client.query("Analyze BTC sentiment")   # pays $1 USDC
print(result.text)
```

### Async

```python
import asyncio
from neurobro_client import NeurobroClient

async def main():
    client = NeurobroClient()
    result = await client.query_async("What are the top DeFi protocols?")
    print(result.text)

asyncio.run(main())
```

### One-liners

```python
# No wallet needed for a health check
from neurobro_client import check_health
print(check_health().is_healthy)

# Minimal paid query
import asyncio
from neurobro_client import quick_query
print(asyncio.run(quick_query("What is Bitcoin?")))
```

---

## Reading the responses

Every call returns a typed dataclass.

### `HealthStatus`

| Field | Type | Description |
|-------|------|-------------|
| `status` | `str` | `"healthy"` when the API is up |
| `version` | `str` | Service version, e.g. `"1.0.0"` |
| `service` | `str` | `"neurobro-x402"` |
| `is_healthy` | `bool` (property) | Shortcut for `status == "healthy"` |

### `QueryResult`

| Field | Type | Description |
|-------|------|-------------|
| `text` | `str` | The full AI-generated response |
| `model` | `str` | Model that served your request |
| `request_id` | `str` | Unique identifier — include it in any support ticket |

---

## Troubleshooting

**`Private key required`**
Add `WALLET_PRIVATE_KEY=0x...` to `.env` or export it in your shell.

**Payment fails after the 402 step**
Your wallet needs USDC on Base mainnet. Bridge in or buy on a
Base-supported exchange.

**Connection error / timeout**
Run `python 01_health_check.py` first. If that fails, check your network.
If only paid queries fail, try `07_custom_config.py` with a longer timeout.

**Something else broken?**
Include your `request_id` when contacting us:

- Email: [support@neurobro.ai](mailto:support@neurobro.ai)
- Telegram: [@neurobro_support](https://t.me/neurobro_support)
- GitHub: [axioma-ai-labs/x402-neurobro/issues](https://github.com/axioma-ai-labs/x402-neurobro/issues)
