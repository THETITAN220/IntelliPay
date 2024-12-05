const { expect } = require("chai");

describe("AssetTransfer", function () {
    it("Should transfer Ether between accounts", async function () {
        const [sender, recipient] = await ethers.getSigners();
        const Transfer = await ethers.getContractFactory("AssetTransfer");
        const contract = await Transfer.deploy();

        await contract.deployed();
        await sender.sendTransaction({
            to: contract.address,
            value: ethers.utils.parseEther("1"),
        });

        expect(await ethers.provider.getBalance(contract.address)).to.equal(ethers.utils.parseEther("1"));
    });
});
