require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.28",
  networks: {
    sepolia: {
      url: "https://sepolia.infura.io/v3/a4ce2d986f46429db51f1a2f60549dbd",
      accounts: ["ace96ea462f1ad1f8105c0751bcde2ee3c59539acb8692265128fac345fa5c50"],
    },
  },
};
