/**
 * Example: Using x402-fetch to interact with Neurobro x402 API
 * 
 * This is an example file demonstrating how to use the x402-fetch package
 * to make paid API calls to the Neurobro service.
 * 
 * For a complete list of available endpoints, see: x402-neurobro-endpoints.yaml
 * All endpoints require payment via x402 protocol on Base mainnet.
 */

import { config } from "dotenv";
import { decodeXPaymentResponse, wrapFetchWithPayment, createSigner } from "x402-fetch";

config();

const privateKey = process.env.WALLET_PRIVATE_KEY;
const baseURL = "https://x402.neurobro.ai/api/v1/public/bull-market-indicators";

/**
 * This example shows how to use the x402-fetch package to make a request to Neurobro x402 API.
 */
async function main() {
  const signer = await createSigner("base", privateKey);
  const fetchWithPayment = wrapFetchWithPayment(fetch, signer);

  const response = await fetchWithPayment(baseURL, { method: "GET" });
  const body = await response.json();
  console.log(body);

  const paymentResponse = decodeXPaymentResponse(response.headers.get("x-payment-response"));
  console.log(paymentResponse);
}

main().catch(error => {
  console.error(error?.response?.data?.error ?? error);
  process.exit(1);
});
