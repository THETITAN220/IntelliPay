require("dotenv").config(); // Import environment variables
const express = require("express");
const { ethers } = require("ethers");

const app = express();
app.use(express.json());

// Initialize provider and wallet from environment variables
const provider = new ethers.providers.JsonRpcProvider(process.env.INFURA_URL);
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

// Contract details
const contractAddress = process.env.CONTRACT_ADDRESS; // Add contract address in .env
const abi = [
  // Replace this with your actual contract ABI
];
const contract = new ethers.Contract(contractAddress, abi, wallet);

// Transfer endpoint
app.post("/transfer", async (req, res) => {
  const { to, amount } = req.body;
  try {
    const tx = await contract.transfer(to, { value: ethers.utils.parseEther(amount) });
    await tx.wait(); // Wait for the transaction to be mined
    res.send({ success: true, txHash: tx.hash });
  } catch (err) {
    res.status(500).send({ success: false, error: err.message });
  }
});

// Wallet connection endpoint
app.post("/connectwallet", async (req, res) => {
  const { address, signature, nonce } = req.body;
  try {
    const recoveredAddress = ethers.utils.verifyMessage(nonce, signature);
    if (recoveredAddress.toLowerCase() === address.toLowerCase()) {
      res.send({ success: true, message: "Wallet connected!" });
    } else {
      res.status(400).send({ success: false, message: "Invalid signature!" });
    }
  } catch (err) {
    res.status(500).send({ success: false, error: err.message });
  }
});

// Start the server
app.listen(3000, () => console.log("Server running on port 3000"));
