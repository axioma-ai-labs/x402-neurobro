/**
 * Example: Using x402-axios to interact with Neurobro x402 API
 * 
 * This is an example file demonstrating how to use the x402-axios package
 * to make paid API calls to the Neurobro service.
 * 
 * For a complete list of available endpoints, see: x402-neurobro-endpoints.yaml
 * All endpoints require payment via x402 protocol on Base mainnet.
 */

import { config } from "dotenv";
import { withPaymentInterceptor, decodeXPaymentResponse } from "x402-axios";
import axios from "axios";
import { privateKeyToAccount } from "viem/accounts";

config();

const privateKey = process.env.WALLET_PRIVATE_KEY;
const baseURL = "https://x402.neurobro.ai";
const endpointPath = "/api/v1/public/bull-market-indicators";

if (!privateKey) {
  console.error("Missing required environment variable: WALLET_PRIVATE_KEY");
  process.exit(1);
}

// Create a wallet
const account = privateKeyToAccount(privateKey);

// Create an Axios instance with payment
const api = withPaymentInterceptor(
  axios.create({
    baseURL,
  }),
  account,
);

api
  .get(endpointPath)
  .then(response => {
    console.log("Response data:", response.data);

    const paymentResponse = decodeXPaymentResponse(response.headers["x-payment-response"]);
    console.log("Payment response:", paymentResponse);
  })
  .catch(error => {
    console.error("Error:", error.response?.data?.error ?? error.message);
    process.exit(1);
  });