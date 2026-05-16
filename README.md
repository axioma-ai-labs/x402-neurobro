# Neurobro x402 Cookbook

Python examples for the **Neurobro x402 API** — pay-per-call crypto
intelligence with automatic USDC micropayments.

![Neurobro Logo][neurobro-img]

[neurobro-img]: ./assets/neurobro.png

> **No API keys. No signup. No subscription.**
> Point a wallet at `https://x402.neurobro.ai`, pay $1 USDC per call, get
> a crypto-aware answer back. Built for Python devs shipping AI agents,
> trading firms, hedge funds, quants, and anyone who wants an on-demand
> crypto research endpoint.

**Production API:** https://x402.neurobro.ai

---

## Coming soon: NeuroAPI

The full **NeuroAPI** — Neurobro's complete agentic crypto intelligence
platform — is launching soon. This cookbook is the x402 on-ramp you can
build against today. Email
[support@neurobro.ai](mailto:support@neurobro.ai) for early access or
release updates.

Want to build against the key-based NeuroAPI surface? See the companion
[NeuroAPI Cookbook](https://github.com/axioma-ai-labs/neuroapi-cookbook) —
runnable recipes for `/agent/ask`, streaming, retries, and structured
output.

---

## TL;DR

```bash
# 1. Install the client
pip install -r examples/requirements.txt

# 2. Add your wallet key (must hold USDC on Base mainnet)
cp examples/.env.example examples/.env
# edit: WALLET_PRIVATE_KEY=0x...

# 3. Check the API is up (free)
python examples/01_health_check.py

# 4. Ask a question (pays $1 USDC via x402)
python examples/03_cli_query.py "What is Ethereum?"
```

If step 4 prints an answer, you're done.

---

## What you get

- **On-demand crypto analysis** — markets, tokens, sentiment, onchain
  context — behind a single `POST /api/v1/query`.
- **Wallet-native auth** — no accounts to provision, no keys to rotate.
  Your wallet *is* the authentication.
- **Drop-in Python client** — sync, async, batch, and retry helpers with
  typed responses.

---

## How x402 works

[x402](https://x402.org) is an open payment protocol that resurrects the
long-dormant HTTP `402 Payment Required` status code. Instead of signing up
for an API key, you pay per request with USDC.

```
┌─────────┐                              ┌────────────────────┐
│ Client  │ ──── POST /api/v1/query ──►  │   Neurobro x402    │
└─────────┘                              └────────────────────┘
     ▲                                              │
     │ ◄──── 402 Payment Required (details) ────────┘
     │
     │  Client wallet signs a USDC transfer,
     │  settled on Base via an x402 facilitator
     ▼
┌─────────┐  POST /api/v1/query + X-PAYMENT  ┌────────────────┐
│ Client  │ ───────────────────────────────► │ Neurobro x402  │
└─────────┘                                  └────────────────┘
     ▲                                              │
     │ ◄──── 200 OK with the AI response ───────────┘
```

1. Client sends a request with no payment.
2. Server replies `402 Payment Required` with payment details.
3. Client signs a USDC transfer with its wallet.
4. Client retries with an `X-PAYMENT` header.
5. Server verifies the payment on Base, runs the query, returns the answer.

The Python client hides steps 1–4 — you just call `client.query(...)`.
If you want to build your own integration, the full spec lives at
[x402.org](https://x402.org).

---

## Pricing

Flat rate. No tiers. No minimums.

| Endpoint | Method | Cost |
|----------|--------|------|
| `/api/v1/health` | `GET` | Free |
| `/api/v1/query` | `POST` | **$1 USDC** per request, on Base mainnet |

You pay **only for successful calls**. Failed payments and errored
requests don't draw from your wallet.

---

## Prerequisites

- **Python 3.10+**
- **An EVM wallet** with its private key accessible — a dedicated hot
  wallet is recommended (don't reuse a treasury key).
- **USDC on Base mainnet** — any amount above $1 is enough to start.

New to this? See [Get started in 5 minutes](#get-started-in-5-minutes) below.

---

## Get started in 5 minutes

### 1. Clone and install

```bash
git clone https://github.com/axioma-ai-labs/x402-neurobro.git
cd x402-neurobro
pip install -r examples/requirements.txt
```

### 2. Prepare a wallet

Any EVM wallet works. Two common paths:

- **Existing wallet** — export the private key from MetaMask, Rabby, or
  any EVM wallet. Use a burner / hot wallet you reserve for agents —
  not your main holdings.
- **New wallet** — generate one in Python:

  ```python
  from eth_account import Account
  acct = Account.create()
  print("address:", acct.address)
  print("private key:", acct.key.hex())
  ```

  Save the private key somewhere safe.

### 3. Fund it with USDC on Base

You need USDC (not ETH) on Base mainnet. Any of:

- Bridge from Ethereum mainnet via the [Base Bridge](https://bridge.base.org/).
- Buy USDC on a Base-supported exchange (Coinbase supports direct
  Base withdrawals) and send to your wallet.
- Swap into USDC on-Base with any Base DEX.

Around **$2–$5 USDC** is plenty to try a handful of queries. The USDC
contract on Base is `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`.

### 4. Configure `.env`

```bash
cp examples/.env.example examples/.env
# open examples/.env and set WALLET_PRIVATE_KEY=0x...
```

### 5. Run your first queries

```bash
# Free — verifies the API is reachable
python examples/01_health_check.py

# Paid — pays $1 USDC and prints the answer
python examples/03_cli_query.py "What is Ethereum?"
```

If the paid call prints a response, you're integrated.

---

## Use as a library

```python
from neurobro_client import NeurobroClient

client = NeurobroClient()      # reads WALLET_PRIVATE_KEY from .env

# Free
status = client.health()
print(status.is_healthy)

# Paid — handles the 402 → sign → retry flow automatically
result = client.query("Analyze ETH price action this week")
print(result.text)
```

### Async

```python
import asyncio
from neurobro_client import NeurobroClient

async def main():
    client = NeurobroClient()
    result = await client.query_async("Top 3 DeFi narratives right now?")
    print(result.text)

asyncio.run(main())
```

### One-liner

```python
import asyncio
from neurobro_client import quick_query

answer = asyncio.run(quick_query("What is a rollup?"))
```

---

## Examples

Every file ends with an **example output** block so you see what to
expect before running it.

| File | Purpose | Paid? | Best for |
|------|---------|-------|----------|
| [`01_health_check.py`](./examples/01_health_check.py) | Verify the API is online | Free | First run, CI probes |
| [`02_simple_query.py`](./examples/02_simple_query.py) | Smallest working paid integration | Paid | Minimal reference |
| [`03_cli_query.py`](./examples/03_cli_query.py) | Ask anything from the terminal | Paid | Quick manual checks |
| [`04_async_usage.py`](./examples/04_async_usage.py) | Full async workflow | Paid | Agents, FastAPI, event loops |
| [`05_error_handling.py`](./examples/05_error_handling.py) | Handle every failure mode | Mixed | Production clients |
| [`06_batch_queries.py`](./examples/06_batch_queries.py) | Sequential + concurrent batches | Paid | Research, backtests |
| [`07_custom_config.py`](./examples/07_custom_config.py) | Custom URL / timeout / env vars | Free | Staging, self-hosted |
| [`08_retry_logic.py`](./examples/08_retry_logic.py) | Exponential backoff on transient failures | Paid | Long-running bots |

See [`examples/README.md`](./examples/README.md) for run notes and a
per-example funding checklist.

---

## Common use cases

- **Trading firms & desks** — enrich signal pipelines with on-demand
  commentary. You pay only for the calls your strategy makes — no monthly
  floor, no seat licenses.
- **Quant & research teams** — sweep a symbol universe with
  `06_batch_queries.py`; total cost is exactly `$1 × prompts`.
- **Agent builders** — drop `NeurobroClient` into a LangChain tool, a
  custom agent loop, or a crewai worker. The wallet is the API key, so
  there's nothing to rotate when a new agent process spins up.
- **Individual traders** — `03_cli_query.py "what's moving today?"`
  from the terminal whenever you want a second opinion.

---

## FAQ

**Do I need an API key?**
No. Your wallet is your identity. There's nothing to register.

**Is my private key sent to the server?**
No. The client signs payments locally; only a signed `X-PAYMENT` header
is transmitted. Your key never leaves your machine.

**What happens if my wallet runs out of USDC mid-call?**
The server returns `402` and the client raises `httpx.HTTPStatusError`.
Top up and retry — no partial charge, no lost funds.

**Can I use a testnet?**
The production API runs on Base mainnet. If you need a sandbox for a
specific integration, email us.

**What model is behind it?**
A frontier LLM augmented with crypto-specific tooling. The `model` field
on every response tells you which model served your request.

**How fast are responses?**
Typically a few seconds. The client's default timeout is 60s; raise it
in `07_custom_config.py` if you're on a slow link.

**Can I use this from Node, Go, Rust?**
Yes — x402 is protocol-level. This repo is Python, but any x402 client
library will work. See the
[x402 docs](https://docs.cdp.coinbase.com/x402/quickstart-for-buyers) for
clients in other languages.

**Is the API rate-limited?**
There's no per-key tier (there are no keys). Abuse protection exists at
the network layer, but normal usage — including batch runs — is fine.

---

## Support

Stuck, hit a bug, or want a feature?

- **Bugs & feature requests** → [GitHub Issues](https://github.com/axioma-ai-labs/x402-neurobro/issues)
- **Direct support** → [support@neurobro.ai](mailto:support@neurobro.ai)
- **Chat** → Telegram [@neurobro_support](https://t.me/neurobro_support)

When reporting an issue with a specific query, include the `request_id`
the server returned — it makes debugging much faster.

---

## Links

- [NeuroAPI Cookbook](https://github.com/axioma-ai-labs/neuroapi-cookbook)
- [x402 protocol](https://x402.org)
- [x402 Python package](https://pypi.org/project/x402/)
- [Coinbase x402 quickstart for buyers](https://docs.cdp.coinbase.com/x402/quickstart-for-buyers)
- [Base network](https://base.org/)
- [USDC on Base (Circle)](https://www.circle.com/en/usdc-multichain/base)

## License

MIT
