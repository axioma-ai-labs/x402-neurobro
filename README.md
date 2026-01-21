# Neurobro x402 API Cookbook

A practical guide to interacting with the **Neurobro API** using the **x402 protocol** for seamless, on-chain micropayments.

![Neurobro Logo][neurobro-img]

[neurobro-img]: ./assets/neurobro.png

## Overview

This repository provides **working Python examples** for calling the Neurobro x402 API. The API offers AI-powered crypto analysis with automatic USDC payments via the x402 protocol.

**Production API:** https://x402.neurobro.ai

---

## What is x402?

**x402** is an open payment protocol for APIs. It enables **pay-per-request** using crypto (USDC on Base) with:

- No account creation
- No API keys
- No sessions or cookies
- Automatic payment handling

Simple flow: **HTTP Request -> 402 Payment Required -> Pay -> Response**

Learn more: [x402.org](https://x402.org)

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **Wallet with USDC** on Base mainnet
- **Private key** for signing payments

### Installation

```bash
cd examples
pip install -r requirements.txt
```

### Configuration

```bash
cp examples/.env.example examples/.env
```

Edit `examples/.env` and add your private key:

```env
WALLET_PRIVATE_KEY=0x_your_private_key_here
```

**Security:** Never share your private key or commit your `.env` file.

---

## Usage

### Check API Health (Free)

```bash
cd examples
python health_check.py
```

### Send a Query (Paid)

```bash
python quick_query.py "What is the current Bitcoin market sentiment?"
```

### Full Example

```bash
python basic_usage.py
```

### Use as a Library

```python
from client import NeurobroClient

client = NeurobroClient()  # reads WALLET_PRIVATE_KEY from env

# Free health check
health = client.health()
print(f"API Status: {health.status}")

# Paid query
result = client.query("Analyze Ethereum price action this week")
print(result.response)
```

See [`examples/README.md`](./examples/README.md) for more detailed documentation.

---

## API Endpoints

| Endpoint | Method | Description | Cost |
|----------|--------|-------------|------|
| `/api/v1/health` | GET | Health check | Free |
| `/api/v1/query` | POST | AI crypto analysis | USDC per query |

### Query Request

```json
POST /api/v1/query
Content-Type: application/json

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
  "request_id": "unique-request-id"
}
```

---

## How x402 Payments Work

```
1. Client sends request to /api/v1/query
       |
       v
2. Server returns 402 Payment Required
   (includes payment details in headers)
       |
       v
3. x402 library automatically:
   - Reads payment requirements
   - Signs USDC payment authorization
   - Retries request with X-PAYMENT header
       |
       v
4. Server verifies payment, processes query
       |
       v
5. Client receives AI response
```

All payments are USDC on Base mainnet. The x402 Python library handles the entire flow automatically.

---

## Troubleshooting

### Missing private key

Ensure `WALLET_PRIVATE_KEY` is set in your `.env` file.

### Payment fails

- Check your wallet has USDC on **Base mainnet**
- Verify your private key matches the funded wallet

### Connection issues

Run `health_check.py` to verify the API is online.

---

## Links

- **x402 Protocol:** [https://x402.org](https://x402.org)
- **Coinbase x402 Guide:** [https://docs.cdp.coinbase.com/x402/quickstart-for-buyers](https://docs.cdp.coinbase.com/x402/quickstart-for-buyers)
- **x402 Python Package:** [https://pypi.org/project/x402/](https://pypi.org/project/x402/)

---

## License

MIT
