# x402-neurobro

Examples for interacting with the Neurobro API using x402 protocol for payment handling.

## Overview

This repository contains working examples of how to use the x402 protocol to make paid API calls to the Neurobro API. The Neurobro API provides financial data including bull market indicators, macro indicators, and transfer data.

## Quick Start

### Prerequisites

- Node.js installed
- A wallet with USDC on Base mainnet
- Your Ethereum private key

### Setup

1. Install dependencies:
```bash
pnpm install
```

2. Create your environment file:
```bash
cp .env.example .env
```

3. Edit `.env` and add your wallet private key:
```
WALLET_PRIVATE_KEY=0x_your_private_key_here
```

### Run Examples

```bash
# Using axios
node examples/axios-example.js

# Using fetch
node examples/fetch-example.js
```

## Available Endpoints

See [x402-neurobro-endpoints.yaml](./x402-neurobro-endpoints.yaml) for detailed documentation.

- `/api/v1/public/bull-market-indicators` - $1.00 USDC
- `/api/v1/public/macro-indicators` - $1.00 USDC
- `/api/v1/public/transfers` - $1.00 USDC
- `/api/v1/public/health` - $0.001 USDC

## How It Works

1. The example makes a request to a Neurobro API endpoint
2. If the endpoint requires payment (402 Payment Required), the x402 client automatically:
   - Detects the payment requirement
   - Creates a payment authorization
   - Signs the payment with your wallet
   - Retries the request with payment proof
3. You receive the response data along with payment details

## Troubleshooting

**Error: Cannot find module**
- Make sure you're running commands from the project root directory
- Verify all dependencies are installed: `pnpm install`

**Error: Missing environment variable**
- Ensure `.env` exists: `cp .env.example .env`
- Add your `WALLET_PRIVATE_KEY` to `.env`

**Payment errors**
- Verify you have USDC on Base mainnet in your wallet
- Check your private key is correct

## Security

⚠️ Never commit `.env` or private keys to version control.

## References

- [x402 Documentation](https://x402.org/docs)
- [x402-fetch npm](https://www.npmjs.com/package/x402-fetch)
- [x402-axios npm](https://www.npmjs.com/package/x402-axios)
