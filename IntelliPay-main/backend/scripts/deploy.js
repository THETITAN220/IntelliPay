const hre = require("hardhat");

async function main() {
  const AssetTransfer = await hre.ethers.getContractFactory("AssetTransfer");
  const assetTransfer = await AssetTransfer.deploy();

  await assetTransfer.deployed();

  console.log(AssetTransfer deployed to: ${assetTransfer.address});
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });