const hre = require("hardhat");

async function main() {
  // Ensure the contracts are compiled
  await hre.run("compile");

  // Get the contract factory for AssetTransfer
  const AssetTransfer = await hre.ethers.getContractFactory("AssetTransfer");

  console.log("Deploying contracts...");

  // Deploy the contract
  const contract = await AssetTransfer.deploy({
    gasLimit: 5000000,  // Set a gas limit
  });

  // Log the contract object to understand its structure
  console.log("Contract object:", contract);

  // Wait for the contract to be mined
  try {
    const tx = await contract.deployTransaction.wait();
    console.log("Contract deployed!");
    console.log("Transaction hash:", tx.transactionHash);
    console.log("Contract address:", contract.address);
  } catch (error) {
    console.error("Error while waiting for deployment:", error);
  }
}

// Run the script
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
