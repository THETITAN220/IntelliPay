const hre = require("hardhat");

async function main() {
  // Compile contracts (optional if already compiled)
  await hre.run("compile");

  // Get the contract factory for Lock
  const Lock = await hre.ethers.getContractFactory("Lock");

  console.log("Deploying contracts...");

  // Define the unlockTime value (in Unix timestamp format)
  const unlockTime = Math.floor(Date.now() / 1000) + 60 * 60; // Unlock after 1 hour

  // Deploy the contract with the unlockTime as a constructor argument
  const lock = await Lock.deploy(unlockTime, {
    value: hre.ethers.utils.parseEther("0.1"), // Sending some Ether with the contract deployment
  });

  // Wait for the contract to be deployed
  await lock.deployed();

  console.log("Contract deployed to:", lock.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
