# Neurobro x402 API Cookbook

A practical guide to interacting with the **Neurobro API** using the **x402 protocol** for seamless, on-chain payments.

![Neurobro Logo][neurobro-img]

[neurobro-img]: ./assets/neurobro.png

## Overview

This repository includes **fully working examples** that show how to call Neurobro’s paid API endpoints using x402.  
The Neurobro API provides real-time financial analytics such as:

- Bull market indicators
- Macro & global liquidity signals
- Institutional transfer monitoring

With x402, each request **automatically handles the payment**—no registration, OAuth, or complicated wallet flows required.

---

## What is x402?

**x402** is an open payment protocol designed for APIs. It allows users to **pay per request** using crypto (e.g., USDC on Base) with:

✅ No account creation  
✅ No API keys  
✅ No cookies or sessions  
✅ No signature pop-ups

Just a simple **HTTP request → Payment → Response** workflow.

➡️ Learn more here: [x402 docs](https://x402.org)

---

## Quick Start

### ✅ Prerequisites

Before running the examples, you will need:

- **Node.js** installed
- A wallet funded with **USDC on Base mainnet**
- Your **Ethereum private key** (used to sign payments locally)

---

### Install Dependencies

```bash
pnpm install
```

### Environment Setup

```bash
cp .env.example .env
```

Edit the `.env` file and add your private key:

```env
WALLET_PRIVATE_KEY=0x_your_private_key_here
```

> **Security Note:** Never share your private key or commit your `.env` file.
> It is already excluded in `.gitignore` for safety.

---

## Run Example Scripts

```bash
# Axios client example
node examples/axios-example.js

# Fetch client example
node examples/fetch-example.js
```

Each script will:

✅ Detect payment requirements
✅ Approve and sign the payment via x402
✅ Retry the request automatically
✅ Return valid response data

---

## Available Paid Endpoints

| Endpoint                                | Description                        | Price       |
| --------------------------------------- | ---------------------------------- | ----------- |
| `/api/v1/public/bull-market-indicators` | Global bull market signal analysis | $1.00 USDC  |
| `/api/v1/public/macro-indicators`       | Macro & liquidity trackers         | $1.00 USDC  |
| `/api/v1/public/transfers`              | Institutional flows monitoring     | $1.00 USDC  |
| `/api/v1/public/health`                 | Status check                       | $0.001 USDC |

See full spec here:
➡️ [`x402-neurobro-endpoints.yaml`](./x402-neurobro-endpoints.yaml)

**Note**: We're currently preparing the release of 100+ more proprietary endpoints to Neurobro x402 API!

---

## 🧠 How x402 Payments Work?

Behind the scenes:

1. Your script sends a request to a Neurobro x402 API endpoint
2. Server returns `402 Payment Required` (if needed)
3. The x402 client library:
   * Reads payment metadata from headers
   * Creates a payment authorization
   * Signs the order with your wallet
   * Resends the request with proof of payment
4. You get the final API response ✅

All payment operations are transparent onchain to the user.

---

## 🛠 Troubleshooting

#### 1. Module not found

* Ensure you are in the repo root
* Reinstall deps:

```bash
pnpm install
```

#### 2. Missing `WALLET_PRIVATE_KEY`

* Ensure `.env` exists and the key is valid

#### 3. Payment fails

* Check your wallet balance (USDC on **Base mainnet**)
* Confirm your private key matches the wallet holding USDC

---

## Security Best Practices

* **NEVER** commit `.env` or private keys
* Prefer a **dedicated wallet** for testing
* Rotate API usage keys regularly if needed

---

## 📚 Useful Links

* x402 Official Docs: [https://x402.org](https://x402.org)
* Quickstart for Buyers: [https://x402.gitbook.io/x402/getting-started/quickstart-for-buyers](https://x402.gitbook.io/x402/getting-started/quickstart-for-buyers)
* Coinbase Buyer Guide: [https://docs.cdp.coinbase.com/x402/quickstart-for-buyers](https://docs.cdp.coinbase.com/x402/quickstart-for-buyers)
* npm packages:

  * [https://www.npmjs.com/package/x402-fetch](https://www.npmjs.com/package/x402-fetch)
  * [https://www.npmjs.com/package/x402-axios](https://www.npmjs.com/package/x402-axios)
